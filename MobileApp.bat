@echo off
echo ======================================================
echo          DIGITAL AUDIO LIBRARY - MOBILE VERSION
echo ======================================================
echo.
echo 1. Kompyuterda ochish: http://localhost:8080/mobile/
echo 2. Telefonda ochish (WiFi bir xil bo'lishi kerak):
echo    http://172.30.3.81:8080/mobile/
echo.
echo Serverni to'xtatish uchun ushbu oynani yoping.
echo.
echo ======================================================
start "" "http://localhost:8080/mobile/"
python -m http.server 8080
pause
