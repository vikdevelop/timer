import time
import datetime
import os
from pathlib import Path
import locale
import json
import gi
from gi.repository import Gio

# Load system language
p_lang = locale.getlocale()[0]
if p_lang == 'pt_BR':
    r_lang = 'pt_BR'
elif p_lang == 'nb_NO':
    r_lang = 'nb_NO'
else:
    r_lang = p_lang[:-3]
    
locale = open(f"/app/translations/{r_lang}.json")
_ = json.load(locale)

settings = Gio.Settings.new_with_path("com.github.vikdevelop.timer", "/com/github/vikdevelop/timer/")
DATA = f"{Path.home()}/.var/app/com.github.vikdevelop.timer/data"
 
# Create class that acts as a countdown
def countdown(h, m, s):
 
    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s
 
    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
 
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds = total_seconds)
        
        # Prints the time left on the timer
        print(timer, end="\r")
 
        # Delays the program one second
        time.sleep(1)
 
        # Reduces total time by one second
        total_seconds -= 1
 
    if settings["action"] == "default":
        os.system("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        if settings["notification-text"] == "":
            text = _["timing_finished"]
        else:
            text = settings["notification-text"]
        if settings["show-appname"] == True:
            appname = _["timer_title"]
        else:
            appname = " "
        if settings["show-notification-icon"] == True:
            icon = "-i com.github.vikdevelop.timer"
        else:
            icon = "-i d"
        os.system(f"notify-send '{appname}' '{text}' {icon}")
    elif settings["action"] == "Reboot":
        os.system("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Reboot" boolean:true')
    elif settings["action"] == "Shut Down":
        os.system("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.PowerOff" boolean:true')
    elif settings["action"] == "Suspend":
        os.system("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Suspend" boolean:true')
    else:
        import alarm_notification
 
# Inputs for hours, minutes, seconds on timer
h = settings["hours"]
m = settings["mins"]
s = settings["seconds"]
countdown(int(h), int(m), int(s))
