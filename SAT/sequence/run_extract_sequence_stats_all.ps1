param(
    [string]$PythonExe = "",
    [string]$OutputCsv = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$extractor = Join-Path $scriptDir "extract_sequence_stats.py"

if (-not (Test-Path -LiteralPath $extractor)) {
    throw "Extractor not found: $extractor"
}

if ([string]::IsNullOrWhiteSpace($OutputCsv)) {
    $OutputCsv = Join-Path $scriptDir "results\sequence_stats_all.csv"
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
$sourceCodeRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

$candidateDirs = @(
    (Join-Path $sourceCodeRoot "Result_python\no_pre_processing\SAT\PSE"),
    (Join-Path $sourceCodeRoot "Result_python\pre_processing\SAT\PSE"),
    (Join-Path $scriptDir "results\preprocessing")
)

$inputDirs = @()
foreach ($dir in $candidateDirs) {
    if (Test-Path -LiteralPath $dir) {
        $inputDirs += $dir
    }
}

if ($inputDirs.Count -eq 0) {
    throw "No sequence log directories found."
}

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
