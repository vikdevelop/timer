#/bin/sh

install -Dm755 -t /app/bin flatpak/run.sh
install -Dm755 -t /app/src src/timer.py
install -Dm755 -t /app/share/applications flatpak/com.github.vikdevelop.timer.desktop
install -Dm755 -t /app/share/icons/hicolor/128x128/apps flatpak/icons/com.github.vikdevelop.timer.png
install -Dm644 -t /app/share/metainfo flatpak/com.github.vikdevelop.timer.metainfo.xml
