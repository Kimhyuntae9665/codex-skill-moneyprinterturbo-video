[CmdletBinding()]
param(
    [string]$Output = '',
    [Parameter(Mandatory = $true)]
    [string]$MptNarratedSource,
    [double]$Duration = 58.5
)

$ErrorActionPreference = 'Stop'
$exampleRoot = Split-Path -Parent $PSScriptRoot
$skillRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
if (-not $Output) {
    $Output = Join-Path $exampleRoot 'generated\MCD_v8_research_applied.mp4'
}
$outputFull = [System.IO.Path]::GetFullPath($Output)
$outputDir = Split-Path -Parent $outputFull
if (-not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}
$outputStem = [System.IO.Path]::GetFileNameWithoutExtension($outputFull)
$master = Join-Path $outputDir "$outputStem.visual-master.mp4"
$muxed = Join-Path $outputDir "$outputStem.mpt-narrated.mp4"
$subtitle = Join-Path $exampleRoot 'subtitle.v8.srt'
if (-not (Test-Path -LiteralPath $subtitle)) {
    $subtitle = Join-Path $exampleRoot 'subtitle.v6.srt'
}
$fontDir = Join-Path $skillRoot 'assets\fonts'
$burner = Join-Path $skillRoot 'scripts\burn_subtitles.py'

if (-not (Test-Path -LiteralPath $MptNarratedSource)) {
    throw "MPT narrated source not found: $MptNarratedSource"
}

python -X utf8 (Join-Path $PSScriptRoot 'mcd_short_v8.py') --output $master
if ($LASTEXITCODE -ne 0) { throw 'v8 visual render failed' }

ffmpeg -y -hide_banner -loglevel error -i $master -i $MptNarratedSource `
    -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -t $Duration -movflags +faststart $muxed
if ($LASTEXITCODE -ne 0) { throw 'MPT narration mux failed' }

python -X utf8 $burner --video $muxed --subtitle $subtitle --output $outputFull `
    --font-dir $fontDir --font-name 'Noto Sans KR' --font-size 12 --margin-v 28 --overwrite
if ($LASTEXITCODE -ne 0) { throw 'reviewed subtitle burn failed' }

Write-Output $outputFull
