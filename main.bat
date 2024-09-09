@echo off
REM Cambia alla directory in cui si trova il file batch
cd /d "%~dp0"

REM Esegui il file main.exe
start main.exe

REM Attendi un tasto per chiudere il terminale (opzionale)
pause