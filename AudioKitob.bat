@echo off
title Digital Audio Library
cd /d "%~dp0"
echo Dastur ishga tushmoqda...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo Dasturda xatolik yuz berdi.
    pause
)
