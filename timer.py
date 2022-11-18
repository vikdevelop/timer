import subprocess
import json
# Czech
if subprocess.getoutput("locale | grep 'LANG'") == 'LANG=cs_CZ.UTF-8':
    with open('/app/translations/cs.json') as t:
        jT = json.load(t)
# Italian
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=it_IT.UTF-8':
    with open('/app/translations/it.json') as t:
        jT = json.load(t)
# Deutsch
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=de_DE.UTF-8':
    with open('/app/translations/de.json') as t:
        jT = json.load(t)
# Russian
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=ru_RU.UTF-8':
    with open('/app/translations/ru.json') as t:
        jT = json.load(t)
# Finnish
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=fi_FI.UTF-8':
    with open('/app/translations/fi.json') as t:
        jT = json.load(t)
# French
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=fr_FR.UTF-8':
    with open('/app/translations/fr.json') as t:
        jT = json.load(t)
# Norwegian (Bokmål)
elif subprocess.getoutput("locale | grep 'LANG'") == 'LANG=nb_NO.UTF-8':
    with open('/app/translations/nb_NO.json') as t:
        jT = json.load(t)
# English
else:
    with open('/app/translations/en.json') as t:
        jT = json.load(t)

# import main file - source code
import src.main
