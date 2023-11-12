import subprocess
import json
import os
import locale
from urllib.request import urlopen
from pathlib import Path
BASE_URL = 'https://raw.githubusercontent.com/vikdevelop/timer/main/translations/json'
# Load system language
p_lang = locale.getlocale()[0]
if p_lang == 'pt_BR':
    r_lang = 'pt_BR'
elif p_lang == 'nb_NO':
    r_lang = 'nb_NO'
elif 'zh' in p_lang:
    r_lang = 'zh_Hans'
else:
    r_lang = p_lang[:-3]
    
locale = open(f"/app/translations/{r_lang}.json")
# Load JSON local file
jT = json.load(locale)
        
# import main file - source code
import src.main
