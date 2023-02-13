import subprocess
import json
import os
from urllib.request import urlopen
from pathlib import Path
BASE_URL = 'https://raw.githubusercontent.com/vikdevelop/timer/main/translations/json'
# Czech
if subprocess.getoutput("locale | grep 'LANG'") == 'LANG=cs_CZ.UTF-8':
    lang = 'cs.json'
# Italian
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=it_IT.UTF-8':
    lang = 'it.json'
# Deutsch
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=de_DE.UTF-8':
    lang = 'de.json'
# Russian
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=ru_RU.UTF-8':
    lang = 'ru.json'
# Finnish
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=fi_FI.UTF-8':
    lang = 'fi.json'
# French
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=fr_FR.UTF-8':
    lang = 'fr.json'
# Norwegian (Bokmål)
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=nb_NO.UTF-8':
    lang = 'nb_NO.json'
# Ukrainian
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=uk_UA.UTF-8':
    lang = 'uk.json'
# Spanish
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=es_ES.UTF-8':
    lang = 'es.json'
# Turkish
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=tr_TR.UTF-8':
    lang = 'tr.json'
# Dutch
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=nl_NL.UTF-8':
    lang = 'nl.json'
# English
else:
    lang = 'en.json'

"""
if os.path.exists("{}/.var/app/com.github.vikdevelop.timer/cache/{}".format(Path.home(), lang)):
    try:
        locale = open("{}/.var/app/com.github.vikdevelop.timer/cache/{}".format(Path.home(), lang))
    except KeyError:
        locale = open(f"/app/translations/{lang}")
else:
    locale = open(f"/app/translations/{lang}")
"""
try:
    with open(f"/app/translations/{lang}") as l:
        # Load JSON local file
        jT = json.load(l)
except:
    jT["advanced"] = "More settings",
    jT["go_to_more_settings"] = "Go to More settings",
    jT["go_to_notification_settings"] = "Go to Notification settings",
    jT["alternative_key"] = "The alternative keyboard shortcut is: {}",
    jT["vertical_text"] = "Vertical text in countdown page",
    jT["vertical_text_desc"] = "Displays vertical text that counts down the time on the countdown page",
    jT["save_expander_row_state"] = "Expand Preferences dropdown row",
    jT["save_expander_row_state_desc"] = "When you start the Timer application, the Preferences drop-down row will automatically expand.",
    jT["show_appicon"] = "Show application icon in notification",
    jT["show_appname"] = "Show application name in notification",
    jT["notification_text"] = "<b>Notification</b>",
    jT["alarm_clock_dialog_text"] = "<b>Alarm clock dialog</b>",

# import main file - source code
import src.main
