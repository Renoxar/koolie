@echo off
rem Koolie - Starter fuer Windows (D-362, CR-2026-140).
rem
rem Sucht ein Python ab 3.8 und ruft den Dialog .koolie\core\install_dialog.py auf.
rem Die Installationslogik steht in install.py; dieser Starter enthaelt keine.
rem
rem BEWUSST OHNE SPRUNGMARKEN (goto, call :marke): Das Release-Archiv liefert diese
rem Datei mit LF-Zeilenenden aus, und cmd.exe findet Sprungmarken in einer LF-Datei
rem nicht zuverlaessig. Eine Sonde haelt das fest.
rem
rem Pfade stehen innerhalb von Klammerbloecken immer in Anfuehrungszeichen: Ein Pfad
rem wie "C:\Program Files (x86)\..." schloesse den Block sonst an seiner Klammer.
rem
rem Der Store-Platzhalter WindowsApps\python.exe startet kein Python; er faellt an der
rem Versionsprobe durch wie jeder andere Kandidat, der nicht antwortet.
setlocal
set "KOOLIE_KERN=%~dp0.koolie\core"
set "KOOLIE_PY="
if not exist "%KOOLIE_KERN%\install_dialog.py" (
    echo FEHLER: install_dialog.py fehlt unter "%KOOLIE_KERN%".
    echo Dieser Starter gehoert in die Wurzel des entpackten Frameworks.
) else (
    for %%K in ("py -3" "python3" "python") do (
        if not defined KOOLIE_PY (
            %%~K -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1 && set "KOOLIE_PY=%%~K"
        )
    )
)
if exist "%KOOLIE_KERN%\install_dialog.py" if not defined KOOLIE_PY (
    echo Koolie braucht Python 3.8 oder neuer - gefunden wurde keines.
    echo.
    echo Installieren, zum Beispiel:
    echo   winget install Python.Python.3.12
    echo oder von python.org - dort "Add python.exe to PATH" waehlen.
    echo Danach ein NEUES Fenster oeffnen und diesen Starter erneut aufrufen.
)
set "KOOLIE_RC=1"
if defined KOOLIE_PY (
    %KOOLIE_PY% "%KOOLIE_KERN%\install_dialog.py"
)
if defined KOOLIE_PY set "KOOLIE_RC=%ERRORLEVEL%"
echo.
if not defined KOOLIE_KEINE_PAUSE pause
endlocal & exit /b %KOOLIE_RC%
