@echo off
setlocal enabledelayedexpansion

REM Liste des adresses IP à tester
set addresses=8.8.8.8 8.8.4.4 1.1.1.1 99.99.99.99

REM Effectuer le ping pour chaque adresse IP
for %%i in (%addresses%) do (
    ping -n 1 %%i >nul
    if !errorlevel! == 0 (
        echo %%i - OK
    ) else (
        echo %%i - KO
    )
)

pause
