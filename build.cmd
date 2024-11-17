del ./dist

echo %RANDOM% > build.txt

py -m PyInstaller main.py ^
--add-data "./res;res" ^
--add-data "./res/images;res/images" ^
--add-data "./res/sounds;res/sounds" ^
--add-data "./version.txt;." ^
--add-data "./build.txt;." ^
--splash ./res/images/SPLASH.png ^
--onefile ^
-y ^
-n "MechaLeague Match Manager" ^
-i ./res/images/APPICON.ico