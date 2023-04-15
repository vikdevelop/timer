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
# Portugalese (Brazil)
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=pt_BR.UTF-8':
    lang = 'pt_BR.json'
# Arabic
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=ar_SA.UTF-8':
    lang = 'ar.json'
# Hungarian
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=hu_HU.UTF-8':
    lang = 'hu.json'
# Persian
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=fa_IR.UTF-8':
    lang = 'fa.json'
# English
else:
    lang = 'en.json'
    
locale = open(f"/app/translations/{lang}")
# Load JSON local file
jT = json.load(locale)
        
# import main file - source code
import src.main
