$py = "C:\msys64\ucrt64\bin\python3.exe"
if (-not (Test-Path $py)) { $py = "python" }
& $py (Join-Path $PSScriptRoot "run.py") @args
exit $LASTEXITCODE
