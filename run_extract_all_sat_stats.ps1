param(
    [string]$PythonExe = "",
    [string]$OutputDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$forwardScript = Join-Path $PSScriptRoot "stats_csv\tools\run_extract_all_sat_stats.ps1"

if (-not (Test-Path -LiteralPath $forwardScript)) {
    throw "Forward target not found: $forwardScript"
}

& powershell -ExecutionPolicy Bypass -File $forwardScript -PythonExe $PythonExe -OutputDir $OutputDir
exit $LASTEXITCODE
