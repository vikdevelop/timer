
# Copyright 2021 vikdevelop <super-vik1@protonmail.com>
# Tento program je svobodný Software. Můžete jej dále šířit a nebo upravovat za podmínek licence GNU General Public License,
# vydané Free Software Foundation.

# Tento program je šířen bez JAKÉKOLIV ZÁRUKY;
# Licenci by jste měli obdržet spolu s tímto programem. 
# Pokud ne, <https://gnu.org/licences>

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class CasovacWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, title="Časovač")
        self.set_border_width(40)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(mainBox)

        self.spinner = Gtk.Spinner()
        mainBox.pack_start(self.spinner, True, True, 0)

        self.label = Gtk.Label()
        mainBox.pack_start(self.label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text("10")
        mainBox.pack_start(self.entry, True, True, 0)
# tlačítka pro spuštění a zastavení času
        self.buttonStart = Gtk.Button(label="Spustit časovač")
        self.buttonStart.connect("clicked", self.on_buttonStart_clicked)
        mainBox.pack_start(self.buttonStart, True, True, 0)

        self.buttonStop = Gtk.Button(label="Zastavit časovač")
        self.buttonStop.set_sensitive(False)
        self.buttonStop.connect("clicked", self.on_buttonStop_clicked)
        mainBox.pack_start(self.buttonStop, True, True, 0)

        self.timeout_id = None
        self.connect("destroy", self.on_SpinnerWindow_destroy)

    def on_buttonStart_clicked(self, widget, *args):
        """ tlacitko "clicked" v udalosti buttonStart. """
        self.start_timer()
# událost, která oznamuje, že byl zastaven časovač uživatelem
    def on_buttonStop_clicked(self, widget, *args):
        """ tlacitko "clicked" v udalosti buttonStop. """
        self.stop_timer("Časovač byl zastaven")

    def on_SpinnerWindow_destroy(self, widget, *args):
        """ zpracovavam udalost pro zavreni okna """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()

    def on_timeout(self, *args, **kwargs):
        """ Funkce casoveho limitu.
        """
# Událost, která oznamuje, že Časování proběhlo úspěšně
        self.counter -= 1
        if self.counter <= 0:
            self.stop_timer("Časování bylo dokončeno!")
            return False
        self.label.set_label("Čas: " + str(int(self.counter / 4)))
        return True
# Události pro tlačétka výše
    def start_timer(self):
        """ Spustit časovač. """
        self.buttonStart.set_sensitive(False)
        self.buttonStop.set_sensitive(True)
        self.counter = 4 * int(self.entry.get_text())
        self.label.set_label("Čas: " + str(int(self.counter / 4)))
        self.spinner.start()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)

    def stop_timer(self, alabeltext):
        """ Zastavit časovač """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.buttonStart.set_sensitive(True)
        self.buttonStop.set_sensitive(False)
        self.label.set_label(alabeltext)

# únikový kód
win = CasovacWindow()
win.show_all()
Gtk.main()
