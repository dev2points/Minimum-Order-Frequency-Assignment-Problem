param(
    [string]$PythonExe = "",
    [string]$OutputCsv = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$extractor = Join-Path $scriptDir "extract_maxsat_stats.py"
$resultsDir = Join-Path $scriptDir "results"

if (-not (Test-Path -LiteralPath $extractor)) {
    throw "Extractor not found: $extractor"
}

if (-not (Test-Path -LiteralPath $resultsDir)) {
    throw "Results directory not found: $resultsDir"
}

if ([string]::IsNullOrWhiteSpace($OutputCsv)) {
    $OutputCsv = Join-Path $resultsDir "maxsat_stats_all.csv"
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
$inputDirs = Get-ChildItem -Directory $resultsDir | ForEach-Object { $_.FullName }

Write-Host "Using Python: $python"
Write-Host "Extractor: $extractor"
Write-Host "Output: $OutputCsv"
Write-Host "Inputs:"
$inputDirs | ForEach-Object { Write-Host "  - $_" }

& $python $extractor @inputDirs --output $OutputCsv
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Done. CSV written to: $OutputCsv"
