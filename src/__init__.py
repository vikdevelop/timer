import json, locale, gi
from gi.repository import GLib

# Path for config files
CACHE = GLib.get_user_cache_dir() + "/tmp"
CONFIG = GLib.get_user_config_dir()
DATA = GLib.get_user_data_dir()

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

try:
    locale = open(f"/app/translations/{r_lang}.json")
except:
    locale = open(f"/app/translations/en.json")
    
jT = json.load(locale)
