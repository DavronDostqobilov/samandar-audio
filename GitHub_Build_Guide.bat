@echo off
echo ======================================================
echo       GITHUB ORQALI ANDROID VA IOS QURISH (Cloud)
echo ======================================================
echo.
echo 1. Kodni GitHub'ga yuboring (Push qiling):
echo.
echo    git add .
echo    git commit -m "Build for Android and iOS"
echo    git push origin main
echo.
echo 2. GitHub dagi "Actions" bo'limiga o'ting.
echo 3. "Build Mobile Apps" ishga tushadi.
echo    - Android: ~5-7 daqiqa
echo    - iOS: ~10-15 daqiqa (macOS sekinroq ishlaydi)
echo.
echo 4. Tugagach, "Artifacts" bo'limida 2 ta fayl paydo bo'ladi:
echo    - AudioKitob-Android (ichida .apk bor)
echo    - AudioKitob-iOS (ichida .app bor)
echo.
echo 5. YUKLAB OLISH VA OCHISH:
echo    - Fayl .zip bo'lib tushadi. 
echo    - O'ng tugmani bosib "Extract All" (Izvlech) qiling.
echo    - Ichidan haqiqiy APK faylni olasiz.
echo.
echo DIQQAT: iOS versiyasi uchun Apple Developer akkaunti bo'lmasa,
echo uni haqiqiy telefonga o'rnatish qiyin bo'lishi mumkin.
echo Android versiyasi hammada ishlaydi.
echo ======================================================
pause
