param(
  [switch]$Strict,
  [string]$ArtifactDir = "",
  [int]$TimeoutSeconds = 35
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$HelperProject = Join-Path $RepoRoot "resources\win-uia-helper\WinChronicle.UiaHelper.csproj"
$HelperDll = Join-Path $RepoRoot "resources\win-uia-helper\bin\Debug\net8.0-windows\win-uia-helper.dll"
$CodeCommand = Get-Command code.cmd -ErrorAction SilentlyContinue

if (-not $CodeCommand) {
  throw "code.cmd was not found on PATH"
}
if (-not $ArtifactDir) {
  $ArtifactDir = Join-Path ([IO.Path]::GetTempPath()) ("winchronicle-uia-vscode-" + [guid]::NewGuid().ToString("N"))
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
  Get-CimInstance Win32_Process -Filter "Name = 'Code.exe'" |
    Where-Object { $_.CommandLine -like "*$Token*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}

$marker = "WINCHRONICLE_VSCODE_EDITOR_SMOKE_" + [guid]::NewGuid().ToString("N")
$root = Join-Path ([IO.Path]::GetTempPath()) ("winchronicle-vscode-" + [guid]::NewGuid().ToString("N"))
$userData = Join-Path $root "user-data"
$extensions = Join-Path $root "extensions"
$settingsDir = Join-Path $userData "User"
$file = Join-Path $root "winchronicle_vscode_smoke.txt"
$artifact = Join-Path $ArtifactDir "vscode-capture.json"

try {
  New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
  New-Item -ItemType Directory -Path $extensions -Force | Out-Null
  Set-Content -LiteralPath (Join-Path $settingsDir "settings.json") -Value '{ "editor.accessibilitySupport": "on", "telemetry.telemetryLevel": "off" }' -Encoding UTF8
  Set-Content -LiteralPath $file -Value $marker -Encoding UTF8
  $goto = "${file}:1:1"
  $process = Start-Process -FilePath $CodeCommand.Source -ArgumentList @(
    "--disable-extensions",
    "--disable-workspace-trust",
    "--skip-welcome",
    "--new-window",
    "--user-data-dir",
    $userData,
    "--extensions-dir",
    $extensions,
    "--goto",
    $goto
  ) -PassThru -WindowStyle Normal

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  $capture = $null
  while ((Get-Date) -lt $deadline) {
    $capture = Invoke-HarnessHelper -HelperArgs @(
      "capture",
      "--harness",
      "--process-name",
      "Code.exe",
      "--window-title-regex",
      "winchronicle_vscode_smoke|Visual Studio Code",
      "--depth",
      "80",
      "--time-budget-ms",
      "5000",
      "--no-store"
    ) -ArtifactPath $artifact

    if ($capture -ne $null) {
      $metadata = @(
        $capture.window.app_name,
        $capture.window.process_name,
        $capture.window.title
      ) -join " "
      if ($metadata -like "*Visual Studio Code*" -or $metadata -like "*Code.exe*") {
        break
      }
    }
    Start-Sleep -Milliseconds 700
  }

  if ($capture -eq $null) {
    throw "VS Code capture did not produce JSON; artifact: $artifact"
  }
  $metadata = @($capture.window.app_name, $capture.window.process_name, $capture.window.title) -join " "
  if ($metadata -notlike "*Visual Studio Code*" -and $metadata -notlike "*Code.exe*") {
    throw "VS Code metadata hard gate failed; artifact: $artifact"
  }
  if ($capture.capture_target.kind -ne "process_name_window_title_regex" -or $capture.capture_target.harness_only -ne $true) {
    throw "VS Code capture did not use harness-only process/title target; artifact: $artifact"
  }

  $observed = @(
    $capture.visible_text,
    $capture.focused_element.text,
    $capture.focused_element.value
  ) -join "`n"
  if ($observed -like "*$marker*") {
    Write-Host "PASS: VS Code UIA targeted smoke passed; artifact: $artifact"
  } elseif ($Strict) {
    throw "VS Code editor marker was not exposed through UIA strict mode; artifact: $artifact"
  } else {
    Write-Host "WARN: VS Code metadata smoke passed, but editor marker was not exposed through UIA; artifact: $artifact"
  }
} finally {
  Stop-SmokeProcesses -Token $userData
  if ($process -and -not $process.HasExited) {
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
  }
  Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
