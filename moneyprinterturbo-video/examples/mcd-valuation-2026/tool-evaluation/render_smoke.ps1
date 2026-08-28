$ErrorActionPreference = 'Stop'

$projectRoot = $PSScriptRoot
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$mediaDir = Join-Path $projectRoot 'render-cache'
$outputDir = Join-Path $projectRoot 'output'
$outputFile = Join-Path $outputDir 'mcd-valuation-smoke.mp4'

if (-not (Test-Path -LiteralPath $python)) {
    throw "Local Manim interpreter not found: $python. Create it with: uv venv --python 3.13 .venv"
}

New-Item -ItemType Directory -Force -Path $mediaDir, $outputDir | Out-Null

$timer = [System.Diagnostics.Stopwatch]::StartNew()
& $python -m manim render `
    --renderer=cairo `
    --media_dir $mediaDir `
    --disable_caching `
    --flush_cache `
    --resolution 1080,1920 `
    --frame_rate 30 `
    --format mp4 `
    --output_file mcd-valuation-smoke `
    (Join-Path $projectRoot 'manim_smoke.py') `
    MCDValuationSmoke

if ($LASTEXITCODE -ne 0) {
    throw "Manim render failed with exit code $LASTEXITCODE"
}
$timer.Stop()

$rendered = Get-ChildItem -LiteralPath $mediaDir -Recurse -File -Filter 'mcd-valuation-smoke.mp4' |
    Select-Object -First 1
if ($null -eq $rendered) {
    throw "Manim completed but no MP4 was found below $mediaDir"
}

Copy-Item -LiteralPath $rendered.FullName -Destination $outputFile -Force
Write-Output ("Render elapsed: {0:n2} s" -f $timer.Elapsed.TotalSeconds)
Write-Output "Smoke MP4: $outputFile"
Write-Output "Rendered source: $($rendered.FullName)"
