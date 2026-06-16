param(
    [string]$PythonExe = "",
    [string]$OutputCsv = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$extractor = Join-Path $scriptDir "extract_evalmaxsat_stats.py"
$noPreLogs = Join-Path $scriptDir "results\no_preprocessing\pipeline"
$preLogs = Join-Path $scriptDir "results\processing\pipeline"

if (-not (Test-Path -LiteralPath $extractor)) {
    throw "Extractor not found: $extractor"
}

if ([string]::IsNullOrWhiteSpace($OutputCsv)) {
    $OutputCsv = Join-Path $scriptDir "results\evalmaxsat_stats_all.csv"
}

function Resolve-PythonExe {
    param([string]$Requested)

    if (-not [string]::IsNullOrWhiteSpace($Requested)) {
        return $Requested
    }

    $candidates = @(
        "C:\Users\ADMIN\AppData\Local\Programs\Python\Python312\python.exe",
        "python"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }

        $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($cmd) {
            return $candidate
        }
    }

    throw "Cannot find a usable Python interpreter. Pass -PythonExe explicitly."
}

$python = Resolve-PythonExe -Requested $PythonExe

Write-Host "Using Python: $python"
Write-Host "Extractor: $extractor"
Write-Host "Inputs:"
Write-Host "  - $noPreLogs"
Write-Host "  - $preLogs"
Write-Host "Output: $OutputCsv"

& $python $extractor $noPreLogs $preLogs --output $OutputCsv
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Done. CSV written to: $OutputCsv"
