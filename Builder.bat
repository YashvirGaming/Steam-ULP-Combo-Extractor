@echo off
set SCRIPT_NAME=steam_combo_extractor.py
set ICON=icon.ico

echo ======================================
echo   Building Steam Combo Extractor EXE
echo ======================================

python -m nuitka ^
 --standalone ^
 --onefile ^
 --enable-plugin=tk-inter ^
 --include-module=customtkinter ^
 --windows-icon-from-ico=%ICON% ^
 --windows-console-mode=disable ^
 --jobs=12 ^
 --output-dir=. ^
 %SCRIPT_NAME%

echo ======================================
echo  Build complete! EXE: %~nSCRIPT_NAME%.exe
echo ======================================
pause
