param(
  [string]$ArtifactDir = "",
  [int]$TimeoutSeconds = 20
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$HelperProject = Join-Path $RepoRoot "resources\win-uia-helper\WinChronicle.UiaHelper.csproj"
$HelperDll = Join-Path $RepoRoot "resources\win-uia-helper\bin\Debug\net8.0-windows\win-uia-helper.dll"

if (-not $ArtifactDir) {
  $ArtifactDir = Join-Path ([IO.Path]::GetTempPath()) ("winchronicle-uia-notepad-" + [guid]::NewGuid().ToString("N"))
}
New-Item -ItemType Directory -Path $ArtifactDir -Force | Out-Null

if (-not (Test-Path -LiteralPath $HelperDll)) {
  dotnet build $HelperProject --nologo | Out-Host
}

if (-not ("WinChronicleSmokeNotepadWindows" -as [type])) {
  Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class WinChronicleSmokeNotepadWindows {
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc callback, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out int processId);
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int maxCount);
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowTextLength(IntPtr hWnd);
}
'@
}

function Get-WindowTitle([IntPtr]$Hwnd) {
  $length = [WinChronicleSmokeNotepadWindows]::GetWindowTextLength($Hwnd)
  if ($length -le 0) { return "" }
  $builder = [Text.StringBuilder]::new($length + 1)
  [void][WinChronicleSmokeNotepadWindows]::GetWindowText($Hwnd, $builder, $builder.Capacity)
  return $builder.ToString()
}

function Find-TopLevelWindowByProcessAndTitle([string]$ExpectedProcessName, [string]$TitleRegex, [int]$TimeoutSeconds) {
  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while ((Get-Date) -lt $deadline) {
    $script:FoundHwnd = [IntPtr]::Zero
    [WinChronicleSmokeNotepadWindows]::EnumWindows({
      param([IntPtr]$Hwnd, [IntPtr]$Param)
      if (-not [WinChronicleSmokeNotepadWindows]::IsWindowVisible($Hwnd)) { return $true }
      $windowPid = 0
      [void][WinChronicleSmokeNotepadWindows]::GetWindowThreadProcessId($Hwnd, [ref]$windowPid)
      $windowProcessName = (Get-Process -Id $windowPid -ErrorAction SilentlyContinue).ProcessName
      if ($windowProcessName -ne $ExpectedProcessName) { return $true }
      $title = Get-WindowTitle $Hwnd
      if ($title -match $TitleRegex) {
        $script:FoundHwnd = $Hwnd
        return $false
      }
      return $true
    }, [IntPtr]::Zero) | Out-Null

    if ($script:FoundHwnd -ne [IntPtr]::Zero) {
      return $script:FoundHwnd
    }
    Start-Sleep -Milliseconds 300
  }
  throw "No visible Notepad top-level window matched process/title."
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
    throw "UIA helper failed; artifact: $ArtifactPath"
  }
  return Get-Content -LiteralPath $ArtifactPath -Raw | ConvertFrom-Json
}

$marker = "WINCHRONICLE_NOTEPAD_SMOKE_" + [guid]::NewGuid().ToString("N")
$tempFile = Join-Path ([IO.Path]::GetTempPath()) ("winchronicle-notepad-" + [guid]::NewGuid().ToString("N") + ".txt")
$process = $null

try {
  Set-Content -LiteralPath $tempFile -Value $marker -Encoding UTF8
  $process = Start-Process -FilePath "notepad.exe" -ArgumentList $tempFile -PassThru -WindowStyle Normal
  $titleRegex = [regex]::Escape((Split-Path $tempFile -Leaf))
  $hwnd = Find-TopLevelWindowByProcessAndTitle -ExpectedProcessName "Notepad" -TitleRegex $titleRegex -TimeoutSeconds $TimeoutSeconds
  $hwndText = "0x{0:X16}" -f $hwnd.ToInt64()
  $artifact = Join-Path $ArtifactDir "notepad-capture.json"
  $capture = Invoke-HarnessHelper -HelperArgs @(
    "capture",
    "--harness",
    "--hwnd",
    $hwndText,
    "--depth",
    "80",
    "--no-store"
  ) -ArtifactPath $artifact

  $observed = @(
    $capture.visible_text,
    $capture.focused_element.text,
    $capture.focused_element.value
  ) -join "`n"
  if ($observed -notlike "*$marker*") {
    throw "Notepad marker was not captured; artifact: $artifact"
  }
  if ($capture.capture_target.kind -ne "hwnd" -or $capture.capture_target.harness_only -ne $true) {
    throw "Notepad capture did not use harness-only hwnd target; artifact: $artifact"
  }

  Write-Host "PASS: Notepad UIA targeted smoke passed; artifact: $artifact"
} finally {
  if ($process -and -not $process.HasExited) {
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
  }
  Remove-Item -LiteralPath $tempFile -Force -ErrorAction SilentlyContinue
}
