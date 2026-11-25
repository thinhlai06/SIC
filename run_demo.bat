@echo off
setlocal
cd /d "%~dp0"
title DR grading demo

rem Look for the M1 checkpoint (the model used in the report)
set "CKPT=model\m1_s0_best.pt"
if not exist "%CKPT%" set "CKPT=logs\_old_5ep\_ckpt5\m1_s0_best.pt"
if not exist "%CKPT%" (
    echo [ERROR] Model file not found.
    echo Put m1_s0_best.pt into the folder "model" next to this file.
    pause
    exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo Loading the model, please wait about 30-60 seconds ...
echo The browser opens automatically. Press Ctrl+C in this window to stop.
echo Sample images: code\demo\samples
echo.
python code\demo\app.py --ckpt "%CKPT%" --port 7890 --open
pause
