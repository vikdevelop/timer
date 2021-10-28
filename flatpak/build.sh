#/bin/sh

install -D -t /app/bin timer.sh
install -D -t /app src/timer.py
install -D -t /app/share/applications flatpak/com.github.vikdevelop.timer.desktop
install -D -t /app/share/icons/hicolor/128x128/apps flatpak/icons/com.github.vikdevelop.timer.png
install -D -t /app/share/metainfo flatpak/com.github.vikdevelop.timer.metainfo.xml
