import subprocess
import sys
import json
import os
import time
from datetime import timedelta
sys.path.append('/app')
from timer import *
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, Adw, Gio

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

CONFIG = os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data'

print(jT["timer_running"])
# Timer Application window
class TimerWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable()
        self.set_default_size(360, 360)
        self.set_size_request(360,360)
        self.application = kwargs.get('application')
        self.style_manager = self.application.get_style_manager()
        self.theme()
        self.set_title(title=jT["timer_title"])
        self.headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=self.headerbar)
        
        # Gtk.Box() layout
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.mainBox.set_margin_start(20)
        self.mainBox.set_margin_end(20)
        self.set_child(self.mainBox)
        
        # App menu
        menu_button_model = Gio.Menu()
        #menu_button_model.append(jT["preferences"], 'app.settings')
        menu_button_model.append(jT["about_app"], 'app.about')
        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        self.headerbar.pack_end(child=menu_button)
        
        self.timingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Spinner
        self.spinner = Gtk.Spinner()
        self.spinner_size()
        
        self.b_label = Gtk.Label.new(str="\n\n\n")
        self.mainBox.append(self.b_label)
        
        self.label = Gtk.Label()
        self.label_action = Gtk.Label()
        
        # Entry
        self.make_timer_box()
        
        # Properities
        self.properities()
        
        # Start timer button
        self.buttonStart = Gtk.Button.new()
        self.buttonStart.set_icon_name("media-playback-start-symbolic")
        self.buttonStart.connect("clicked", self.on_buttonStart_clicked)
        self.button1_style_context = self.buttonStart.get_style_context()
        self.button1_style_context.add_class('suggested-action')
        self.button1_style_context.add_class(class_name='circular')
        self.headerbar.pack_start(self.buttonStart)
        self.click_events = []

        self.timeout_id = None
        self.connect("destroy", self.on_SpinnerWindow_destroy)
    
    # Entries of seconds, minutes and hours
    def make_timer_box(self):
        # Load counter.json (config file with time counter values)
        if os.path.exists(f'{CONFIG}/counter.json'):
            with open(f'{CONFIG}/counter.json') as jc:
                jC = json.load(jc)
            hour_e = jC["hour"]
            min_e = jC["minutes"]
            sec_e = jC["seconds"]
        else:
            hour_e = "0"
            min_e = "1"
            sec_e = "0"
        # Layout
        self.timerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        self.timerBox.set_margin_start(0)
        self.timerBox.set_margin_end(0)
        
        self.lbox = Gtk.ListBox.new()
        self.lbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.lbox.get_style_context().add_class(class_name='boxed-list')
        
        # Hour entry and label
        self.hour_entry = Adw.EntryRow()
        self.hour_entry.set_text(hour_e)
        self.hour_entry.set_title(jT["hours"])
        self.hour_entry.set_alignment(xalign=1)
        self.timerBox.append(self.hour_entry)
        
        # Minute entry and label
        self.minute_entry = Adw.EntryRow()
        self.minute_entry.set_text(min_e)
        self.minute_entry.set_title(jT["mins"])
        self.minute_entry.set_alignment(xalign=1)
        self.timerBox.append(self.minute_entry)
        
        # Second entry and label
        self.secs_entry = Adw.EntryRow()
        self.secs_entry.set_text(sec_e)
        self.secs_entry.set_title(jT["secs"])
        self.secs_entry.set_alignment(xalign=1)
        self.timerBox.append(self.secs_entry)
        
        self.adw_action_row_time = Adw.ActionRow.new()
        self.adw_action_row_time.set_icon_name(icon_name='com.github.vikdevelop.timer')
        #self.adw_action_row_time.set_title(title="Time")
        self.adw_action_row_time.add_suffix(widget=self.timerBox)
        self.lbox.append(child=self.adw_action_row_time)
        
        #self.lbox.append(self.timerBox)
        self.mainBox.append(self.lbox)
        
    def properities(self):
        self.adw_expander_row = Adw.ExpanderRow.new()
        self.adw_expander_row.set_title(title=jT["preferences"])
        self.adw_expander_row.set_subtitle(subtitle="Preferences Descritpion")
        self.lbox.append(child=self.adw_expander_row)
        
        # ComboBox - spinner size
        sizes = Gtk.StringList.new(strings=[
            '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60 (%s)' % jT["default"], '65', '70', '75', '80'
        ])
        
        adw_action_row_00 = Adw.ComboRow.new()
        adw_action_row_00.set_icon_name(icon_name='content-loading-symbolic')
        adw_action_row_00.set_title(title=jT["spinner"])
        adw_action_row_00.set_model(model=sizes)
        adw_action_row_00.set_subtitle(subtitle=jT["spinner_size_desc"])
        adw_action_row_00.set_subtitle_lines(2)
        adw_action_row_00.connect('notify::selected-item', self.on_combo_box_text_changed)
        self.adw_expander_row.add_row(child=adw_action_row_00)
        
        if os.path.exists(f'{CONFIG}/spinner.json'):
            with open(f'{CONFIG}/spinner.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["spinner-size"]
            if combobox_s == "5":
                adw_action_row_00.set_selected(0)
            elif combobox_s == "10":
                adw_action_row_00.set_selected(1)
            elif combobox_s == "15":
                adw_action_row_00.set_selected(2)
            elif combobox_s == "20":
                adw_action_row_00.set_selected(3)
            elif combobox_s == "25":
                adw_action_row_00.set_selected(4)
            elif combobox_s == "30":
                adw_action_row_00.set_selected(5)
            elif combobox_s == "35":
                adw_action_row_00.set_selected(6)
            elif combobox_s == "40":
                adw_action_row_00.set_selected(7)
            elif combobox_s == "45":
                adw_action_row_00.set_selected(8)
            elif combobox_s == "50":
                adw_action_row_00.set_selected(9)
            elif combobox_s == "55":
                adw_action_row_00.set_selected(10)
            elif combobox_s == '60 (%s)' % jT["default"]:
                adw_action_row_00.set_selected(11)
            elif combobox_s == "65":
                adw_action_row_00.set_selected(12)
            elif combobox_s == "70":
                adw_action_row_00.set_selected(13)
            elif combobox_s == "75":
                adw_action_row_00.set_selected(14)
            elif combobox_s == "80":
                adw_action_row_00.set_selected(15)
        else:
            adw_action_row_00.set_selected(11)
        
        # ComboBox - Actions
        actions = Gtk.StringList.new(strings=[
            jT["default"], jT["shut_down"], jT["reboot"], jT["suspend"]
        ])
        
        adw_action_row_01 = Adw.ComboRow.new()
        adw_action_row_01.set_icon_name(icon_name='timer-symbolic')
        adw_action_row_01.set_title(title=jT["action_after_timing"])
        adw_action_row_01.set_title_lines(2)
        adw_action_row_01.set_model(model=actions)
        adw_action_row_01.connect('notify::selected-item', self.on_combo_box_text_s_changed)
        self.adw_expander_row.add_row(child=adw_action_row_01)
        
        if os.path.exists(f'{CONFIG}/actions.json'):
            with open(f'{CONFIG}/actions.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["action"]
            if combobox_s == jT["default"]:
                adw_action_row_01.set_selected(0)
            elif combobox_s == jT["shut_down"]:
                adw_action_row_01.set_selected(1)
            elif combobox_s == jT["reboot"]:
                adw_action_row_01.set_selected(2)
            elif combobox_s == jT["suspend"]:
                adw_action_row_01.set_selected(3)
        else:
            adw_action_row_01.set_selected(0)
        
        # Adw ActionRow - Theme configuration
        ## Gtk.Switch
        switch_01 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/theme.json'):
            with open(f'{CONFIG}/theme.json') as r:
                jR = json.load(r)
            dark = jR["theme"]
            if dark == "dark":
                switch_01.set_active(True)
        switch_01.set_valign(align=Gtk.Align.CENTER)
        switch_01.connect('notify::active', self.on_switch_01_toggled)
        
        ## Adw.ActionRow
        adw_action_row_02 = Adw.ActionRow.new()
        adw_action_row_02.set_icon_name(icon_name='weather-clear-night-symbolic')
        adw_action_row_02.set_title(title=jT["dark_theme"])
        adw_action_row_02.set_subtitle(subtitle=jT["theme_desc"])
        adw_action_row_02.add_suffix(widget=switch_01)
        self.adw_expander_row.add_row(child=adw_action_row_02)
        
        # Adw ActionRow - Resizable of Window configuration
        ## Gtk.Switch
        switch_02 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/window.json'):
            with open(f'{CONFIG}/window.json') as r:
                jR = json.load(r)
            resizable = jR["resizable"]
            if resizable == "true":
                switch_02.set_active(True)
        switch_02.set_valign(align=Gtk.Align.CENTER)
        switch_02.connect('notify::active', self.on_switch_02_toggled)
        
        ## Adw.ActionRow
        adw_action_row_03 = Adw.ActionRow.new()
        adw_action_row_03.set_icon_name(icon_name='window-maximize-symbolic')
        adw_action_row_03.set_title(title=jT["resizable_of_window"])
        #adw_action_row_03.set_subtitle(subtitle=resizable_of_window)
        adw_action_row_03.add_suffix(widget=switch_02)
        adw_action_row_03.set_activatable_widget(widget=switch_02)
        self.adw_expander_row.add_row(child=adw_action_row_03)
        
        # Adw ActionRow - custom notification
        ## Adw.EntryRow
        self.entry = Adw.EntryRow()
        self.apply_entry_text()
        self.entry.set_show_apply_button(True)
        self.entry.set_enable_emoji_completion(True)
        self.entry.connect('changed', self.on_entry_text_changed)
        
        ## Adw.ActionRow
        
        adw_action_row_04 = Adw.ActionRow.new()
        adw_action_row_04.set_icon_name(icon_name='notification-symbolic')
        adw_action_row_04.set_title(title=jT["custom_notification"])
        adw_action_row_04.set_title_lines(2)
        adw_action_row_04.add_suffix(widget=self.entry)
        adw_action_row_04.set_activatable_widget(widget=self.entry)
        self.adw_expander_row.add_row(child=adw_action_row_04)
        
        # Adw ActionRow - play beep
        ## Gtk.Switch
        switch_03 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/beep.json'):
            with open(f'{CONFIG}/beep.json') as r:
                jR = json.load(r)
            beep = jR["play-beep"]
            if beep == "false":
                switch_03.set_active(False)
            else:
                switch_03.set_active(True)
        else:
            switch_03.set_active(True)
        switch_03.set_valign(align=Gtk.Align.CENTER)
        switch_03.connect('notify::active', self.on_switch_03_toggled)
        
        ## Adw.ActionRow
        adw_action_row_05 = Adw.ActionRow.new()
        adw_action_row_05.set_icon_name(icon_name='folder-music-symbolic')
        adw_action_row_05.set_title(title=jT["play_beep"])
        #adw_action_row_05.set_subtitle(subtitle=)
        adw_action_row_05.add_suffix(widget=switch_03)
        adw_action_row_05.set_activatable_widget(widget=switch_03)
        self.adw_expander_row.add_row(child=adw_action_row_05)
    
    # Save app theme configuration
    def on_switch_01_toggled(self, switch01, GParamBoolean):
        if switch01.get_active():
            with open(f'{CONFIG}/theme.json', 'w') as t:
                t.write('{\n "theme": "dark"\n}')
            self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.PREFER_DARK
                )
        else:
            with open(f'{CONFIG}/theme.json', 'w') as t:
                t.write('{\n "theme": "system"\n}')
            self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.FORCE_LIGHT
                )

    # Save entry text (custom notification text)
    def on_entry_text_changed(self, entry):
        entry = self.entry.get_text()
        with open(f'{CONFIG}/notification.json', 'w') as n:
            n.write('{\n "custom-notification": "true",\n "text": "%s"\n}' % entry)
    
    # Apply entry text (custom notification text)
    def apply_entry_text(self):
        if os.path.exists(f'{CONFIG}/notification.json'):
            with open(f'{CONFIG}/notification.json') as n:
                jN = json.load(n)
            text = jN["text"]
            self.entry.set_text(text)
    
    # Save resizable window configuration
    def on_switch_02_toggled(self, switch02, GParamBoolean):
        if switch02.get_active():
            with open(f'{CONFIG}/window.json', 'w') as w:
                w.write('{\n "resizable": "true"\n}')
                self.set_resizable(True)
        else:
            os.remove(f'{CONFIG}/window.json')
            self.set_resizable(False)
    
    # Save playing beep configuration
    def on_switch_03_toggled(self, switch03, GParamBoolean):
        if switch03.get_active():
            with open(f'{CONFIG}/beep.json', 'w') as t:
                t.write('{\n "play-beep": "true"\n}')
        else:
            with open(f'{CONFIG}/beep.json', 'w') as t:
                t.write('{\n "play-beep": "false"\n}')
    
    # Save Combobox (actions) configuration
    def on_combo_box_text_s_changed(self, comborow, GParamObject):
        selected_item_02 = comborow.get_selected_item()
        with open(f'{CONFIG}/actions.json', 'w') as a:
            a.write('{\n "action": "%s"\n}' % selected_item_02.get_string())
    
    # Save Combobox (spinner size) configuration
    def on_combo_box_text_changed(self, comborow, GParamObject):
        selected_item = comborow.get_selected_item()
        with open(f'{CONFIG}/spinner.json', 'w') as s:
            s.write('{\n "spinner-size": "%s"\n}' % selected_item.get_string())
        try:
            self.spinner.set_size_request(int(selected_item.get_string()), int(selected_item.get_string()))
        except ValueError:
            self.spinner.set_size_request(60,60)
            
    # Theme setup
    def theme(self):
        if os.path.exists(f'{CONFIG}/theme.json'):
            with open(f'{CONFIG}/theme.json') as jt:
                t = json.load(jt)
            theme = t["theme"]
            if theme == "dark":
                self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.PREFER_DARK
                )
                
    # Resizable of Window
    def resizable(self):
        if os.path.exists(f'{CONFIG}/window.json'):
            with open(f'{CONFIG}/window.json') as jr:
                rezisable = json.load(jr)
            if rezisable == "true":
                self.set_resizable(True)
        else:
            self.set_resizable(False)
    
    # Spinner size
    def spinner_size(self):
        if os.path.exists(f'{CONFIG}/spinner.json'):
            with open(f'{CONFIG}/spinner.json') as j:
                jsonObject = json.load(j)
            spinner = jsonObject["spinner-size"]
            if spinner == "5":
                self.spinner.set_size_request(5,5)
            if spinner == "10":
                self.spinner.set_size_request(10,10)
            if spinner == "15":
                self.spinner.set_size_request(15,15)
            if spinner == "20":
                self.spinner.set_size_request(20,20)
            if spinner == "25":
                self.spinner.set_size_request(25,25)
            if spinner == "30":
                self.spinner.set_size_request(30,30)
            if spinner == "35":
                self.spinner.set_size_request(35,35)
            if spinner == "40":
                self.spinner.set_size_request(40,40)
            if spinner == "45":
                self.spinner.set_size_request(45,45)
            if spinner == "50":
                self.spinner.set_size_request(50,50)
            if spinner == "55":
                self.spinner.set_size_request(55,55)
            if spinner == '60 (%s)' % jT["default"]:
                self.spinner.set_size_request(60,60)
            if spinner == "65":
                self.spinner.set_size_request(65,65)
            if spinner == "70":
                self.spinner.set_size_request(70,70)
            if spinner == "75":
                self.spinner.set_size_request(75,75)
            if spinner == "80":
                self.spinner.set_size_request(80,80)
        else:
            self.spinner.set_size_request(60,60)
    
    # Start button action
    def on_buttonStart_clicked(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.start_timer()
        return True
    
    # Stop button action
    def on_buttonStop_clicked(self, widget, *args):
        """ button "clicked" in event buttonStop. """
        self.stop_timer()
        self.stopped_toast()
        print(jT["timing_ended"])

    def on_SpinnerWindow_destroy(self, widget, *args):
        """ procesing closing window """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()
    
    # On timeout function
    tick_counter = timedelta(milliseconds = 250) # static object so we don't recreate the object every time
    zero_counter = timedelta()
    def on_timeout(self, *args, **kwargs):
        self.counter -= self.tick_counter
        if self.counter <= self.zero_counter:
            self.stop_timer()
            #self.label.set_markup("<b>" + jT["timing_finished"]+ "</b>")
            self.session()
            print(jT["timing_finished"])
            return False
        self.label.set_markup("<big><b>{}</b></big>".format(
            strfdelta(self.counter, "{hours} %s {minutes} %s {seconds} %s" % (jT["hours"], jT["mins"], jT["secs"]))
        ))
        return True
    
    # Start timer function
    def start_timer(self):
        """ Run Timer. """
        self.check_and_save()
        # Stop timer button
        self.buttonStop = Gtk.Button.new()
        self.buttonStop.set_icon_name("media-playback-stop-symbolic")
        self.button2_style_context = self.buttonStop.get_style_context()
        self.button2_style_context.add_class('destructive-action')
        self.button2_style_context.add_class(class_name='circular')
        self.buttonStop.connect("clicked", self.on_buttonStop_clicked)
        self.headerbar.pack_start(self.buttonStop)
        self.headerbar.remove(self.buttonStart)
        self.mainBox.remove(self.lbox)
        self.non_activated_session()
        self.counter = timedelta(hours = int(self.hour_entry.get_text()), minutes = int(self.minute_entry.get_text()), seconds = int(self.secs_entry.get_text()))
        #self.play_beep()
        self.label.set_markup("<big><b>{}</b></big>".format(
            strfdelta(self.counter, "{hours} %s {minutes} %s {seconds} %s" % (jT["hours"], jT["mins"], jT["secs"]))
        ))
        self.spinner.start()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)
        
    # Stop timer function
    def stop_timer(self):
        """ Stop Timer """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.headerbar.remove(self.buttonStop)
        self.headerbar.pack_start(self.buttonStart)
        self.mainBox.append(self.lbox)
        self.b_label.set_text("\n\n\n")
        self.mainBox.remove(self.timingBox)
        #self.label.set_label(alabeltext)
        #self.play_beep()
        
    def add_toast(self):
        self.toast_overlay = Adw.ToastOverlay.new()
        self.toast_overlay.set_margin_top(margin=12)
        self.toast_overlay.set_margin_end(margin=12)
        self.toast_overlay.set_margin_bottom(margin=12)
        self.toast_overlay.set_margin_start(margin=12)
        self.mainBox.append(self.toast_overlay)
        
        self.toast_finished = Adw.Toast.new(title='')
        self.toast_finished.set_title(title=jT["timing_finished"])
        self.toast_finished.connect('dismissed', self.on_toast_dismissed)
        self.toast_overlay.add_toast(self.toast_finished)
        
    def stopped_toast(self):
        self.toast_overlay_02 = Adw.ToastOverlay.new()
        self.toast_overlay_02.set_margin_top(margin=12)
        self.toast_overlay_02.set_margin_end(margin=12)
        self.toast_overlay_02.set_margin_bottom(margin=12)
        self.toast_overlay_02.set_margin_start(margin=12)
        self.mainBox.append(self.toast_overlay_02)
        
        self.toast_stopped = Adw.Toast.new(title='')
        self.toast_stopped.set_title(title=jT["timing_ended"])
        self.toast_stopped.connect('dismissed', self.on_toast_dismissed)
        self.toast_overlay_02.add_toast(self.toast_stopped)
        
    def on_toast_dismissed(self, toast):
        try:
            self.mainBox.remove(self.toast_overlay)
        except AttributeError:
            self.mainBox.remove(self.toast_overlay_02)
    
    def non_activated_session(self):
        self.b_label.set_text("\n")
        self.timingBox.append(self.spinner)
        self.timingBox.append(self.label_action)
        self.timingBox.append(self.label)
        self.mainBox.append(self.timingBox)
        if os.path.exists(f'{CONFIG}/actions.json'):
            with open(f'{CONFIG}/actions.json') as a:
                jA = json.load(a)
            action = jA["action"]
            if action == jT["default"]:
                self.label_action.set_text(jT["notification_desc"])
            elif action == jT["shut_down"]:
                self.label_action.set_text(jT["shut_down_desc"])
            elif action == jT["reboot"]:
                self.label_action.set_text(jT["reboot_desc"])
            elif action == jT["suspend"]:
                self.label_action.set_text(jT["suspend_desc"])
        else:
            self.label_action.set_text(jT["notification_desc"])
    
    # Session
    def session(self):
        if os.path.exists(f'{CONFIG}/actions.json'):
            with open(f'{CONFIG}/actions.json') as a:
                jA = json.load(a)
            action = jA["action"]
            if action == jT["default"]:
                self.play_beep()
                self.add_toast()
                self.notification()
            elif action == jT["shut_down"]:
                self.play_beep()
                time.sleep(2)
                os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.PowerOff" boolean:true')
            elif action == jT["reboot"]:
                self.play_beep()
                time.sleep(2)
                os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Reboot" boolean:true')
            elif action == jT["suspend"]:
                self.play_beep()
                time.sleep(2)
                os.system('dbus-send --system --print-reply \
        --dest=org.freedesktop.login1 /org/freedesktop/login1 \
        "org.freedesktop.login1.Manager.Suspend" boolean:true')
        else:
            self.play_beep()
            self.add_toast()
            self.notification()
    
    # Notification function
    def notification(self):
        if os.path.exists(f'{CONFIG}/notification.json'):
            with open(f'{CONFIG}/notification.json') as r:
                jR = json.load(r)
            notification = jR["text"]
            if notification == "":
                subprocess.call(['notify-send',jT["timer_title"],jT["timing_finished"],'-i','com.github.vikdevelop.timer'])
            else:
                subprocess.call(['notify-send',jT["timer_title"],notification,'-i','com.github.vikdevelop.timer'])
        else:
            subprocess.call(['notify-send',jT["timer_title"],jT["timing_finished"],'-i','com.github.vikdevelop.timer'])
    
    # Checking whether the entered values are correct and then saving them
    def check_and_save(self):
        if self.hour_entry.get_text() == "":
            self.hour_entry.set_text('0')
        elif self.minute_entry.get_text() == "":
            self.minute_entry.set_text('0')
        elif self.secs_entry.get_text() == "":
            self.secs_entry.set_text('0')
        # Save time counter values
        with open(f'{CONFIG}/counter.json', 'w') as c:
            c.write('{\n' + f' "hour": "{self.hour_entry.get_text()}",\n'+ f' "minutes": "{self.minute_entry.get_text()}",\n' + f' "seconds": "{self.secs_entry.get_text()}"' + '\n}')
            
    # Play beep          
    def play_beep(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json') as r:
                jR = json.load(r)
            beep = jR["play-beep"]
            if beep == "false":
                print("")
            else:
                os.popen("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        else:
            os.popen("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        
# Adw Application class
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.create_action('about', self.on_about_action)
        self.create_action('settings', self.on_settings_action)
    
    # Run About dialog
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name(jT["timer_title"])
        dialog.set_version("2.6")
        dialog.set_developer_name("vikdevelop")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/timer")
        dialog.set_issue_url("https://github.com/vikdevelop/timer/issues")
        dialog.add_credit_section(jT["contributors"], ["Albano Battistella https://github.com/albanobattistella", "Allan Nordhøy https://hosted.weblate.org/user/kingu/", "J. Lavoie https://hosted.weblate.org/user/Edanas", "rene-coty https://github.com/rene-coty", "KenyC https://github.com/KenyC", "ViktorOn https://github.com/ViktorOn"])
        dialog.set_translator_credits(jT["translator_credits"])
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("com.github.vikdevelop.timer")
        dialog.show()
    
    # Run settings dialog
    def on_settings_action(self, action, param):
        self.dialog = Dialog_settings(self)

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
print(jT["timer_quit"])
