import subprocess
# Czech
if subprocess.getoutput("locale") == 'LANG=cs_CZ.UTF-8\nLC_CTYPE="cs_CZ.UTF-8"\nLC_NUMERIC="cs_CZ.UTF-8"\nLC_TIME="cs_CZ.UTF-8"\nLC_COLLATE="cs_CZ.UTF-8"\nLC_MONETARY="cs_CZ.UTF-8"\nLC_MESSAGES="cs_CZ.UTF-8"\nLC_PAPER="cs_CZ.UTF-8"\nLC_NAME="cs_CZ.UTF-8"\nLC_ADDRESS="cs_CZ.UTF-8"\nLC_TELEPHONE="cs_CZ.UTF-8"\nLC_MEASUREMENT="cs_CZ.UTF-8"\nLC_IDENTIFICATION="cs_CZ.UTF-8"\nLC_ALL=':
    from translations.cs import *
    import src.main
# Italian
elif subprocess.getoutput("locale") == 'LANG=it_IT.UTF-8\nLC_CTYPE="it_IT.UTF-8"\nLC_NUMERIC="it_IT.UTF-8"\nLC_TIME="it_IT.UTF-8"\nLC_COLLATE="it_IT.UTF-8"\nLC_MONETARY="it_IT.UTF-8"\nLC_MESSAGES="it_IT.UTF-8"\nLC_PAPER="it_IT.UTF-8"\nLC_NAME="it_IT.UTF-8"\nLC_ADDRESS="it_IT.UTF-8"\nLC_TELEPHONE="it_IT.UTF-8"\nLC_MEASUREMENT="it_IT.UTF-8"\nLC_IDENTIFICATION="it_IT.UTF-8"\nLC_ALL=':
    from translations.it import *
    import src.main
# Deutsch
elif subprocess.getoutput("locale") == 'LANG=de_DE.UTF-8\nLC_CTYPE="de_DE.UTF-8"\nLC_NUMERIC="de_DE.UTF-8"\nLC_TIME="de_DE.UTF-8"\nLC_COLLATE="de_DE.UTF-8"\nLC_MONETARY="de_DE.UTF-8"\nLC_MESSAGES="de_DE.UTF-8"\nLC_PAPER="de_DE.UTF-8"\nLC_NAME="de_DE.UTF-8"\nLC_ADDRESS="de_DE.UTF-8"\nLC_TELEPHONE="de_DE.UTF-8"\nLC_MEASUREMENT="de_DE.UTF-8"\nLC_IDENTIFICATION="de_DE.UTF-8"\nLC_ALL=':
    from translations.de import *
    import src.main
# English
else:
    from translations.en import *
    import src.main
