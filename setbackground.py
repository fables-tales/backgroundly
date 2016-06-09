import subprocess, sys, os
import ctypes
import commands
import platform
import Image

#constant for windows wallpaper setting
SPI_SETDESKWALLPAPER = 20 
 
#some applescript to set the users background
Script = """/usr/bin/osascript<<END
tell application "Finder"
    set desktop picture to POSIX file "%s"
end tell
END"""
 
#Public: Sets the desktop background for a mac 
#filename - the file to set the desktop background to
def set_background_mac(filename):
    subprocess.Popen(Script%filename,shell=True)

#Public: Sets the desktop background for windows 
#filename - the file to set the desktop background to
def set_background_windows(filename):
   if (filename.endswith("bmp") != 1):
      img = Image.open(filename)
      newimage = "C:\Documents and Settings\All Users\Documents\My Pictures\Sample Pictures\pybackground.bmp"
      img.save(newimage)
      ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, newimage , 0) 
   else:
      ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, filename , 0) 

#Public: Sets the desktop background for linux
#filename - the file to set the desktop background to
def set_background_linux(filename):
    desktop = os.environ.pop("DESKTOP_SESSION")
    if (desktop == "gnome"):
        command = "gconftool-2 --set /desktop/gnome/background/picture_filename --type string '" + filename + "'"
        status, output = commands.getstatusoutput(command)  # status=0 if success
    elif (desktop == "xfce"):
        displaylist = commands.getoutput("xfconf-query -c xfce4-desktop -l | grep image-path").splitlines()
        for display in displaylist:
            command = "xfconf-query -c xfce4-desktop -p " + display + " -s " + filename
            status, output = commands.getstatusoutput(command)  # status=0 if success
            
if __name__ == "__main__":
    #get the current operating system, and set background based on it
    system = platform.system()
    if (system == "Darwin"):
        set_background_mac(sys.argv[1])
    elif (system == "Linux"):
        set_background_linux(sys.argv[1])
    else:
        set_background_windows(sys.argv[1])


