@echo off
title PVC ID Automator
echo ==========================================
echo    PVC ID Automator - One-Click Setup
echo ==========================================
echo.

:: 1. Isolate the environment using your exact Windows Python path
if not exist ".venv\Scripts\activate" (
    echo [1/4] Creating a clean, isolated Python environment...
    "C:\Users\Aldrich\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venv
) else (
    echo [1/4] Environment already verified.
)

:: 2. Activate the environment
call .venv\Scripts\activate

:: 3. Install requirements quietly
echo [2/4] Verifying libraries (Pillow)...
python -m pip install --upgrade pip -q
python -m pip install Pillow -q

:: 4. Run the rename/sorting script
echo [3/4] Sorting and renaming files from names.csv...
python "batch rename.py"

:: 5. Run the hole puncher
echo [4/4] Punching transparent holes in all IDs...
python mask.py

echo.
echo ==========================================
echo    SUCCESS! All IDs are fully processed.
echo ==========================================
pause