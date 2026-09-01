param(
    [string]$MediaDirectory = (Join-Path $env:TEMP "mcd-valuation-motion"),
    [ValidateSet("l", "m", "h", "p", "k")]
    [string]$Quality = "h"
)

$ErrorActionPreference = "Stop"
$motionDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$scenePath = Join-Path $motionDirectory "mcd_short.py"

uv run --project $motionDirectory manim "-q$Quality" --format mp4 --media_dir $MediaDirectory $scenePath MCDValuationShort
if ($LASTEXITCODE -ne 0) {
    throw "Manim render failed with exit code $LASTEXITCODE"
}

$rendered = Get-ChildItem -LiteralPath $MediaDirectory -Recurse -Filter "MCDValuationShort.mp4" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
if (-not $rendered) {
    throw "Manim completed without the expected MP4"
}

Write-Output $rendered.FullName
