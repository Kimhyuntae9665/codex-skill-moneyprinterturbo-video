# Portable Windows tool setup

This distribution does not assume that the author's Python, Node, Blender,
Kokoro, or GPU environment exists on your computer. Resolve scripts relative to
this skill directory. Use your own virtual environment and verify commands:

```powershell
Get-Command python, uv, git, ffmpeg, ffprobe -ErrorAction SilentlyContinue
python --version
```

For Python helpers, Python 3.11 or newer is recommended; renderer-specific
requirements remain in the individual workflow. Install declared dependencies
into a virtual environment, then invoke its actual Python executable. Avoid the
Windows Store alias. Node/npm, Blender, Inkscape, GPU drivers and model weights
are optional and must be installed only for the route you select. Discover
Blender with `Get-Command blender` or supply your installed executable path;
do not assume a particular Blender version or device was tested here.

If a running shell predates an installation, refresh its PATH:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:Path
```

Set up remote compute with your own authorized host/profile. Credentials,
connection details and generated outputs are not part of this package.
Installing this bundle does not enable publishing or prove a production render
passed visual or listening review. See the repository installation guide and
run the MoneyPrinterTurbo environment check before production.
