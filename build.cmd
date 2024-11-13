py -m PyInstaller main.py ^
--add-data "./res;res" ^
--add-data "./res/images;res/images" ^
--add-data "./res/sounds;res/sounds" ^
--splash ./res/images/SPLASH.png ^
--onefile ^
-y ^
-n "MechaLeague Match Manager" ^
-i ./res/images/APPICON.ico 