@echo off
rem Koolie - der Befehl koolie fuer Windows aus einem entpackten Release-Archiv
rem (CR-2026-168, D-520). Scoop legt einen Shim auf diese Datei.
rem
rem Sucht ein Python ab 3.8 und reicht alle Argumente an koolie_befehl.py weiter. Anders
rem als install.cmd haelt er am Ende nicht an: Er wird aus einem offenen Terminal
rem aufgerufen, nicht per Doppelklick.
rem
rem BEWUSST OHNE SPRUNGMARKEN wie install.cmd: Das Release-Archiv liefert LF-Zeilenenden.
setlocal
set "KOOLIE_PY="
for %%K in ("py -3" "python3" "python") do (
    if not defined KOOLIE_PY (
        %%~K -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1 && set "KOOLIE_PY=%%~K"
    )
)
if not defined KOOLIE_PY (
    echo Koolie braucht Python 3.8 oder neuer - gefunden wurde keines.
    echo Installieren, zum Beispiel: winget install Python.Python.3.12
    endlocal & exit /b 9009
)
%KOOLIE_PY% "%~dp0koolie_befehl.py" %*
endlocal & exit /b %ERRORLEVEL%
