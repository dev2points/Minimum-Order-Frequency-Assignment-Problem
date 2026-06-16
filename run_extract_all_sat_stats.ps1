param(
    [string]$PythonExe = "",
    [string]$OutputDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$pairwiseWrapper = Join-Path $scriptDir "SAT\pairwise\run_extract_pairwise_stats_all.ps1"
$sequenceWrapper = Join-Path $scriptDir "SAT\sequence\run_extract_sequence_stats_all.ps1"
$maxsatWrapper = Join-Path $scriptDir "MaxSAT\run_extract_maxsat_stats_all.ps1"
$evalmaxsatWrapper = Join-Path $scriptDir "evalmaxsat\run_extract_evalmaxsat_stats_all.ps1"

foreach ($wrapper in @($pairwiseWrapper, $sequenceWrapper, $maxsatWrapper, $evalmaxsatWrapper)) {
    if (-not (Test-Path -LiteralPath $wrapper)) {
        throw "Wrapper not found: $wrapper"
    }
}

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $OutputDir = Join-Path $scriptDir "stats_csv"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

Write-Host "Output directory: $OutputDir"

$commonArgs = @()
if (-not [string]::IsNullOrWhiteSpace($PythonExe)) {
    $commonArgs += @("-PythonExe", $PythonExe)
}

& powershell -ExecutionPolicy Bypass -File $pairwiseWrapper @commonArgs -OutputCsv (Join-Path $OutputDir "pairwise_stats_all.csv")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File $sequenceWrapper @commonArgs -OutputCsv (Join-Path $OutputDir "sequence_stats_all.csv")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File $maxsatWrapper @commonArgs -OutputCsv (Join-Path $OutputDir "maxsat_stats_all.csv")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File $evalmaxsatWrapper @commonArgs -OutputCsv (Join-Path $OutputDir "evalmaxsat_stats_all.csv")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Done. All SAT stats CSV files are in: $OutputDir"
