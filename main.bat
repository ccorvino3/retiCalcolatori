@echo off
REM Cambia alla directory in cui si trova il file batch
cd /d "%~dp0"

REM Esegui il file compiler/main.py utilizzando l'interprete Python
"%~dp0python.exe" main.py

REM Attendi un tasto per chiudere il terminale (opzionale)
pause
