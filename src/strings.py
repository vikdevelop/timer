from timer import *
import json
import sys
sys.path.append('/app')

if jT["timer_title"] == "":
    title = "Timer"

if jT["timer_running"] == "":
    running = "Timer is running ..."
    
if jT["run_timer"] == "":
    start = "Start timer"
    
if jT["stop_timer"] == "":
    stop = "Stop timer"
    
if jT["timing_finished"] == "":
    finished = "Timing has been finished!"
    
if jT["timing_ended"] == "":
    ended = "Timing was stopped"
    
if jT["timer_quit"] == "":
    quit = "Timer was ended"
    
if jT["about_app"] == "":
    about = "About app"
 
if jT["simple_timer"] == "":
    simple_timer = "simple_timer"

if jT["preferences"] == "":
    preferences = "Preferences"

if jT["close"] == "":
    close = "_Close"

if jT["spinner"] == "":
    spinner = "Spinner"
    
if jT["spinner_size_desc"] == "":
    spinner_d = "Select size of spinner:"
    
if jT["select"] == "":
    select = "Select"
    
if jT["resizable_of_window"] == "":
    resizable = "Resizable of Window"

if jT["default"] == "":
    default = "default"
    
if jT["preferences_saved"] == "":
    saved = "Preferences saved."

if jT["theme_desc"] == "":
    theme_desc = "Use this if the timer doesn't follow the system theme."

if jT["dark_theme"] == "":
    dark = "Dark theme"

if jT["contributors"] == "":
    contributors = "Contributors"

if jT["hours"] == "":
    hours = "h"

if jT["mins"] == "":
    mins = "m"

if jT["secs"] == "":
    secs = "s"

if jT["shut_down"] == "":
    shut_down = "Shut down"
    
if jT["reboot"] == "":
    reboot = "reboot"

if jT["action_after_timing"] == "":
    action_after_timing = "Action after finished timer"
    
if jT["blank_value"] == "":
    blank_value = "You have entered blank values!"

if jT["blank_values_desc"] == "":
    blank_values_desc = "Please fill them in."

if jT["custom_notification"] == "":
    custom_notification = "Custom notification text"

if jT["mute_volume"] == "":
    mute_volume = "Mute volume"

if jT["play_beep"] == "":
    play_beep = "Play beep"

if jT["suspend"] == "":
    suspend = "Suspend"
    
if jT["translator_credits"] == "":
    translator_credits = "Unknown translator"
