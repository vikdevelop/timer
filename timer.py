import subprocess
import json
import fileinput
import sys
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
            
# Properties for Shortcuts Window
property_01 = '                <property name="title" translatable="true" context="shortcut window">Show Keyboard shortcuts</property>'
property_02 = '                <property name="title" translatable="true" context="shortcut window">Start timing</property>'
property_03 = '                <property name="title" translatable="true" context="shortcut window">Stop timing</property>'
property_04 = '                <property name="title" translatable="true" context="shortcut window">Quit</property>'
for line in fileinput.input('/home/viktor/Stažené/Timer_design-Beta/src/ui/shortcuts.ui', inplace=1):
    if property_01 in line:
        line = line.replace(property_01,f'                <property name="title" translatable="true" context="shortcut window">{jT["keyboard_shortcuts"]}</property>')
    sys.stdout.write(line)
    
for line in fileinput.input('/app/src/ui/shortcuts.ui', inplace=2):
    if property_02 in line:
        line = line.replace(property_02,f'                <property name="title" translatable="true" context="shortcut window">{jT["run_timer"]}</property>')
    sys.stdout.write(line)
    
for line in fileinput.input('/app/src/ui/shortcuts.ui', inplace=3):
    if property_03 in line:
        line = line.replace(property_03,f'                <property name="title" translatable="true" context="shortcut window">{jT["stop_timer"]}</property>')
    sys.stdout.write(line)

for line in fileinput.input('/app/src/ui/shortcuts.ui', inplace=4):
    if property_04 in line:
        line = line.replace(property_04,f'                <property name="title" translatable="true" context="shortcut window">{jT["close"]}</property>')
    sys.stdout.write(line)

# import main file - source code
import src.main
