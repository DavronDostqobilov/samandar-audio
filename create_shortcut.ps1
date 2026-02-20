$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\Davron\Desktop\Digital Audio Library.lnk")
$Shortcut.TargetPath = "C:\Users\Davron\Desktop\samandar\AudioKitob.bat"
$Shortcut.WorkingDirectory = "C:\Users\Davron\Desktop\samandar"
$Shortcut.WindowStyle = 1
$Shortcut.Save()
