import subprocess
import sys
sys.path.append('/app')
from timer import *
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, Adw, Gio

print(timer_running)
class TimerWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(300, 300)
        self.set_size_request(300,300)
        self.set_resizable(False)
        self.set_title(title=timer_title)
        headerbar = Gtk.HeaderBar.new()
        
        self.set_titlebar(titlebar=headerbar)
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_child(self.mainBox)
        menu_button_model = Gio.Menu()
        menu_button_model.append(about_app, 'app.about')
        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)
        self.spinner = Gtk.Spinner()
        self.mainBox.append(self.spinner)

        self.label = Gtk.Label()
        self.mainBox.append(self.label)

        self.entry = Gtk.Entry()
        self.entry.set_text("10")
        self.mainBox.append(self.entry)

        self.buttonStart = Gtk.Button(label=run_timer)
        self.buttonStart.connect("clicked", self.on_buttonStart_clicked)
        self.mainBox.append(self.buttonStart)

        self.buttonStop = Gtk.Button(label=stop_timer)
        self.buttonStop.set_sensitive(False)
        self.buttonStop.connect("clicked", self.on_buttonStop_clicked)
        self.mainBox.append(self.buttonStop)

        self.timeout_id = None
        self.connect("destroy", self.on_SpinnerWindow_destroy)

    def on_buttonStart_clicked(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.start_timer()

    def on_buttonStop_clicked(self, widget, *args):
        """ button "clicked" in event buttonStop. """
        self.stop_timer(timing_ended)

    def on_SpinnerWindow_destroy(self, widget, *args):
        """ procesing closing window """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()

    def on_timeout(self, *args, **kwargs):
        """ Features timer limit.
        """

        self.counter -= 1
        if self.counter <= 0:
            self.stop_timer(timing_finished)
            print('\a')
            subprocess.call(['notify-send',timer_title,timing_finished])
            print(timing_finished)
            return False
        self.label.set_label(time_text + str(int(self.counter / 4)) + " s")
        return True


    def start_timer(self):
        """ Run Timer. """
        self.buttonStart.set_sensitive(False)
        self.buttonStop.set_sensitive(True)
        print('\a')
        self.counter = 4 * int(self.entry.get_text())
        self.label.set_label(time_text + str(int(self.counter / 4)) + " s")
        self.spinner.start()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)

    def stop_timer(self, alabeltext):
        """ Stop Timer """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.buttonStart.set_sensitive(True)
        self.buttonStop.set_sensitive(False)
        self.label.set_label(alabeltext)
        print('\a')
        print(timing_ended)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.create_action('about', self.on_about_action)

    def on_about_action(self, action, param):
        dialog = Gtk.AboutDialog()
        dialog.set_title(about)
        dialog.set_name(timer_title)
        dialog.set_version("1.9")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments(simple_timer)
        dialog.set_website("https://github.com/vikdevelop/timer")
        dialog.set_website_label(source_code)
        dialog.set_authors(["vikdevelop <https://github.com/vikdevelop>"])
        dialog.set_translator_credits(translator_credits)
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_logo_icon_name("com.github.vikdevelop.timer")
        dialog.show()
    
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
    
    def on_activate(self, app):
        self.win = TimerWindow(application=app)
        self.win.present()
app = MyApp(application_id="com.github.vikdevelop.timer")
app.run(sys.argv)
print(timer_quit)
