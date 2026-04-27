param(
  [string]$ArtifactDir = "",
  [int]$TimeoutSeconds = 30
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$HelperProject = Join-Path $RepoRoot "resources\win-uia-helper\WinChronicle.UiaHelper.csproj"
$HelperDll = Join-Path $RepoRoot "resources\win-uia-helper\bin\Debug\net8.0-windows\win-uia-helper.dll"
$EdgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if (-not (Test-Path -LiteralPath $EdgePath)) {
  throw "Microsoft Edge was not found at $EdgePath"
}
if (-not $ArtifactDir) {
  $ArtifactDir = Join-Path ([IO.Path]::GetTempPath()) ("winchronicle-uia-edge-" + [guid]::NewGuid().ToString("N"))
}
New-Item -ItemType Directory -Path $ArtifactDir -Force | Out-Null

if (-not (Test-Path -LiteralPath $HelperDll)) {
  dotnet build $HelperProject --nologo | Out-Host
}

function Invoke-HarnessHelper([string[]]$HelperArgs, [string]$ArtifactPath) {
  $previous = $env:WINCHRONICLE_HARNESS
  $previousErrorAction = $ErrorActionPreference
  try {
    $env:WINCHRONICLE_HARNESS = "1"
    $ErrorActionPreference = "Continue"
    $output = & dotnet $HelperDll @HelperArgs 2>&1
    $exitCode = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $previousErrorAction
    if ($null -eq $previous) {
      Remove-Item Env:\WINCHRONICLE_HARNESS -ErrorAction SilentlyContinue
    } else {
      $env:WINCHRONICLE_HARNESS = $previous
    }
  }

  $output | Set-Content -LiteralPath $ArtifactPath -Encoding UTF8
  if ($exitCode -ne 0) {
    return $null
  }
  return Get-Content -LiteralPath $ArtifactPath -Raw | ConvertFrom-Json
}

function Stop-SmokeProcesses([string]$Token) {
  Get-CimInstance Win32_Process -Filter "Name = 'msedge.exe'" |
    Where-Object { $_.CommandLine -like "*$Token*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}

$marker = "WINCHRONICLE_EDGE_BODY_SMOKE_" + [guid]::NewGuid().ToString("N")
$root = Join-Path ([IO.Path]::GetTempPath()) ("winchronicle-edge-" + [guid]::NewGuid().ToString("N"))
$profile = Join-Path $root "profile"
$html = Join-Path $root "openchronicle-smoke.html"
$artifact = Join-Path $ArtifactDir "edge-capture.json"

try {
  New-Item -ItemType Directory -Path $profile -Force | Out-Null
  $document = @"
<!doctype html>
<html>
  <head><title>OpenChronicle Smoke $marker</title></head>
  <body>
    <main>
      <h1>OpenChronicle</h1>
      <p>$marker</p>
    </main>
  </body>
</html>
"@
  Set-Content -LiteralPath $html -Value $document -Encoding UTF8
  $uri = ([Uri]$html).AbsoluteUri
  $process = Start-Process -FilePath $EdgePath -ArgumentList @(
    "--new-window",
    "--no-first-run",
    "--disable-background-networking",
    "--force-renderer-accessibility",
    "--user-data-dir=$profile",
    $uri
  ) -PassThru -WindowStyle Normal

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  $capture = $null
  while ((Get-Date) -lt $deadline) {
    $capture = Invoke-HarnessHelper -HelperArgs @(
      "capture",
      "--harness",
      "--process-name",
      "msedge.exe",
      "--window-title-regex",
      "Microsoft.*Edge|OpenChronicle|file://",
      "--depth",
      "80",
      "--time-budget-ms",
      "5000",
      "--no-store"
    ) -ArtifactPath $artifact

    if ($capture -ne $null) {
      $observed = @(
        $capture.visible_text,
        $capture.focused_element.text,
        $capture.focused_element.value
      ) -join "`n"
      if ($observed -like "*$marker*") {
        break
      }
    }
    Start-Sleep -Milliseconds 600
  }

  if ($capture -eq $null) {
    throw "Edge capture did not produce JSON; artifact: $artifact"
  }
  $observed = @($capture.visible_text, $capture.focused_element.text, $capture.focused_element.value) -join "`n"
  if ($observed -notlike "*$marker*") {
    throw "Edge body marker was not captured; artifact: $artifact"
  }
  if ($capture.capture_target.kind -ne "process_name_window_title_regex" -or $capture.capture_target.harness_only -ne $true) {
    throw "Edge capture did not use harness-only process/title target; artifact: $artifact"
  }

  Write-Host "PASS: Edge UIA targeted smoke passed; artifact: $artifact"
} finally {
  Stop-SmokeProcesses -Token $profile
  if ($process -and -not $process.HasExited) {
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
  }
  Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
