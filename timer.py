import subprocess

if subprocess.getoutput("locale") == 'LANG=cs_CZ.UTF-8\nLC_CTYPE="cs_CZ.UTF-8"\nLC_NUMERIC="cs_CZ.UTF-8"\nLC_TIME="cs_CZ.UTF-8"\nLC_COLLATE="cs_CZ.UTF-8"\nLC_MONETARY="cs_CZ.UTF-8"\nLC_MESSAGES="cs_CZ.UTF-8"\nLC_PAPER="cs_CZ.UTF-8"\nLC_NAME="cs_CZ.UTF-8"\nLC_ADDRESS="cs_CZ.UTF-8"\nLC_TELEPHONE="cs_CZ.UTF-8"\nLC_MEASUREMENT="cs_CZ.UTF-8"\nLC_IDENTIFICATION="cs_CZ.UTF-8"\nLC_ALL=':
    from translations.cs import *
    import src.main
else:
    from translations.en import *
    import src.main
