$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\Davron\Desktop\Digital Audio Library.lnk")
$Shortcut.TargetPath = "C:\Users\Davron\Desktop\samandar\DigitalAudioLibrary.exe"
$Shortcut.WorkingDirectory = "C:\Users\Davron\Desktop\samandar"
$Shortcut.IconLocation = "C:\Users\Davron\Desktop\samandar\DigitalAudioLibrary.exe,0"
$Shortcut.Save()
