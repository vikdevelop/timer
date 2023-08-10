import gi
import sys
import os
import locale
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gio, Gtk, Adw

# Load system language
p_lang = locale.getlocale()[0]
if p_lang == 'pt_BR':
    r_lang = 'pt_BR'
elif p_lang == 'nb_NO':
    r_lang = 'nb_NO'
else:
    r_lang = p_lang[:-3]
    
locale = open(f"/app/translations/{r_lang}.json")
_ = json.load(locale)

class ShowAlarmclock(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(100,100)
        self.application = kwargs.get('application')
        self.headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=self.headerbar)
        self.connect("close-request", self.on_close)
        self.set_title("")
        
        self.openButton = Gtk.Button.new_with_label(_["start_again"])
        self.openButton.connect("clicked", self.start_again)
        self.openButton.add_css_class("suggested-action")
        self.headerbar.pack_start(self.openButton)
        
        self.settings = Gio.Settings.new_with_path("com.github.vikdevelop.timer", "/com/github/vikdevelop/timer/")
        
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_valign(Gtk.Align.CENTER)
        self.box.set_halign(Gtk.Align.CENTER)
        self.box.set_margin_bottom(25)
        self.box.set_margin_top(25)
        self.box.set_margin_start(25)
        self.box.set_margin_end(25)
        self.set_child(self.box)
        
        if self.settings["notification-text"] == "":
            text = f'{jT["timing_finished"]}'
        else:
            text = f'{self.settings["notification-text"]}'
        if self.settings["use-in-alarm-clock"] == True:
            title = f'{text}'
        else:
            title = _["timing_finished"]
        
        self.titleLabel = Gtk.Label.new(str=f"<big><b>{title}</b></big>")
        self.titleLabel.set_use_markup(True)
        self.box.append(self.titleLabel)
        
        self.image = Gtk.Image.new_from_icon_name("history")
        self.image.set_pixel_size(128)
        self.box.append(self.image)
        
        self.label = Gtk.Label.new(str=f'<span size="17500">{self.settings["hours"]} {_["hours"]} {self.settings["mins"]} {_["mins"]} {self.settings["seconds"]} {_["secs"]}</span>')
        self.label.set_use_markup(True)
        self.box.append(self.label)
        
        os.popen("bash /app/src/alarm.sh")
        
    def start_again(self, w):
        self.close()
        os.popen("pkill -15 bash && pkill -15 ffplay")
        os.popen("python3 /app/src/main.py")
    
    def on_close(self, widget, *args):
        os.popen("pkill -15 bash && pkill -15 ffplay")

class App(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)

    def on_activate(self, app):
        self.win = ShowAlarmclock(application=app)
        self.win.present()

app = App()
app.run(sys.argv)
