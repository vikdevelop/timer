import sys
sys.path.append('/app')
from timer import *
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, Adw

print(timer_running)
class TimerWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(250, 250)
        self.set_title(timer_title)
        
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.set_child(self.mainBox)

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
            print(timing_finished)
            return False
        self.label.set_label(time_text + str(int(self.counter / 4)) + " s")
        return True


    def start_timer(self):
        """ Run Timer. """
        self.buttonStart.set_sensitive(False)
        self.buttonStop.set_sensitive(True)
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
        print(timing_ended)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        self.win = TimerWindow(application=app)
        self.win.present()
app = MyApp(application_id="com.github.vikdevelop.timer")
app.run(sys.argv)
print(timer_quit)
