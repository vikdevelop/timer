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

# Units of day, minute, hour and second
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

# Path for config files
CONFIG = os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data'
# Print about timer status
print(jT["timer_running"])

# Reset all timer settings dialog
class Dialog_reset(Adw.MessageDialog):
    def __init__(self, parent, **kwargs):
        super().__init__(transient_for=app.get_active_window(), **kwargs)

        self.set_heading(heading=jT["dialog_remove_warning"])
        self.add_response('no', jT["no"])
        self.add_response('yes', jT["yes"])
        self.set_response_appearance(
            response='yes',
            appearance=Adw.ResponseAppearance.SUGGESTED
        )
        self.connect('response', self.dialog_response)
        self.show()

    def dialog_response(self, dialog, response):
        if response == 'yes':
            os.popen(f'rm {CONFIG}/*')
            app = sys.executable
            os.execl(app, app, *sys.argv)

# Keyboard shortcuts dialog
class Dialog_keys(Gtk.Dialog):
    def __init__(self, parent, **kwargs):
        super().__init__(use_header_bar=True, transient_for=app.get_active_window())

        self.set_title(title=jT["keyboard_shortcuts"])
        self.use_header_bar = True
        self.set_modal(modal=True)
        self.set_resizable(False)
        self.connect('response', self.dialog_response)
        self.set_default_size(340, 300)
        
        # Layout
        content_area = self.get_content_area()
        content_area.set_orientation(orientation=Gtk.Orientation.VERTICAL)
        content_area.set_spacing(spacing=12)
        content_area.set_margin_top(margin=25)
        content_area.set_margin_end(margin=50)
        content_area.set_margin_bottom(margin=25)
        content_area.set_margin_start(margin=50)
        content_area.set_halign(Gtk.Align.CENTER)
        content_area.set_valign(Gtk.Align.CENTER)
        
        # Ctrl+S shortcut
        box_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        button_sc = Gtk.Button.new_with_label("Ctrl")
        box_1.append(button_sc)
        
        label_plus = Gtk.Label.new(str="+")
        box_1.append(label_plus)
        
        button_s = Gtk.Button.new_with_label("S")
        box_1.append(button_s)
        
        label_start = Gtk.Label.new(str=jT["run_timer"])
        box_1.append(label_start)
        
        # Ctrl+C shortcut
        box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        button_tc = Gtk.Button.new_with_label("Ctrl")
        box_2.append(button_tc)
        
        label_plus = Gtk.Label.new(str="+")
        box_2.append(label_plus)
        
        button_t = Gtk.Button.new_with_label("C")
        box_2.append(button_t)
        
        label_stop = Gtk.Label.new(str=jT["stop_timer"])
        box_2.append(label_stop)
        
        # Ctrl+Q shortcut
        box_3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        button = Gtk.Button.new_with_label("Ctrl")
        box_3.append(button)
        
        label_plus = Gtk.Label.new(str="+")
        box_3.append(label_plus)
        
        button_q = Gtk.Button.new_with_label("Q")
        box_3.append(button_q)
        
        label_quit = Gtk.Label.new(str=jT["quit"])
        box_3.append(label_quit)
        
        # Ctrl+? shortcut
        box_4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        button_hc = Gtk.Button.new_with_label("Ctrl")
        box_4.append(button_hc)
        
        label_plus = Gtk.Label.new(str="+")
        box_4.append(label_plus)
        
        button_h = Gtk.Button.new_with_label("?")
        box_4.append(button_h)
        
        label_shortcuts = Gtk.Label.new(str=jT["show"])
        box_4.append(label_shortcuts)
        
        # Ctrl+R shortcut
        box_5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        button_rc = Gtk.Button.new_with_label("Ctrl")
        box_5.append(button_rc)
        
        label_plus = Gtk.Label.new(str="+")
        box_5.append(label_plus)
        
        button_r = Gtk.Button.new_with_label("R")
        box_5.append(button_r)
        
        label_reset = Gtk.Label.new(str=jT["reset"])
        box_5.append(label_reset)
        
        # Ctrl+D shortcut
        box_6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        button_dc = Gtk.Button.new_with_label("Ctrl")
        box_6.append(button_dc)
        
        label_plus = Gtk.Label.new(str="+")
        box_6.append(label_plus)
        
        button_d = Gtk.Button.new_with_label("D")
        box_6.append(button_d)
        
        label_dark = Gtk.Label.new(str=jT["activate_dark_theme"])
        box_6.append(label_dark)
        
        # Ctrl+L shortcut
        box_7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        button_lc = Gtk.Button.new_with_label("Ctrl")
        box_7.append(button_lc)
        
        label_plus = Gtk.Label.new(str="+")
        box_7.append(label_plus)
        
        button_l = Gtk.Button.new_with_label("L")
        box_7.append(button_l)
        
        label_light = Gtk.Label.new(str=jT["activate_light_theme"])
        box_7.append(label_light)
        
        content_area.append(box_1)
        content_area.append(box_2)
        content_area.append(box_3)
        content_area.append(box_4)
        content_area.append(box_5)
        content_area.append(box_6)
        content_area.append(box_7)
        
        self.show()
    # Close button clicked action
    def dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.CANCEL:
            dialog.close()

# Timer Application window
class TimerWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_resizable_w()
        self.set_default_size(400, 400)
        self.set_size_request(400, 400)
        self.application = kwargs.get('application')
        self.style_manager = self.application.get_style_manager()
        self.set_theme()
        self.set_title(title=jT["timer_title"])
        self.headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=self.headerbar)
        
        # Set up keyboard shortcuts
        keycont = Gtk.EventControllerKey()
        keycont.connect('key-pressed', self.keys, self)
        self.add_controller(keycont)

        # Gtk.Box() layout
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.mainBox.set_halign(Gtk.Align.CENTER)
        self.mainBox.set_valign(Gtk.Align.CENTER)
        self.mainBox.set_margin_start(44)
        self.mainBox.set_margin_end(44)
        self.set_child(self.mainBox)
        
        # App menu
        self.menu_button_model = Gio.Menu()
        self.menu_button_model.append(jT["delete_timer_settings"], 'app.reset_settings')
        self.menu_button_model.append(jT["keyboard_shortcuts"], 'app.shortcuts')
        self.menu_button_model.append(jT["about_app"], 'app.about')
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.menu_button_model)
        self.headerbar.pack_end(child=self.menu_button)
        
        # Gtk Box layout for timing page
        self.timingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Spinner
        self.spinner = Gtk.Spinner()
        self.set_spinner_size()
        
        # Label for countdown timing and Label for describing the action in progress
        self.label = Gtk.Label()
        self.label_action = Gtk.Label()
        self.label_action.set_wrap(True)
        self.label_action.set_justify(Gtk.Justification.CENTER)
        
        # Entry
        self.make_timer_box()
        
        # Properities
        self.properties()
        
        # Start timer button
        self.buttonStart = Gtk.Button.new()
        self.start_button_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.start_button_box.set_halign(Gtk.Align.CENTER)
        self.start_button_box.append(Gtk.Image.new_from_icon_name( \
            'media-playback-start-symbolic'))
        self.start_button_box.append(Gtk.Label.new(jT["start"]))
        self.buttonStart.set_child(self.start_button_box)
        self.buttonStart.add_css_class('suggested-action')
        self.buttonStart.set_can_focus(False)
        self.buttonStart.connect('clicked', self.on_buttonStart_clicked)
        self.headerbar.pack_start(self.buttonStart)
        
        # Reset timer button
        self.buttonReset = Gtk.Button.new()
        self.reset_button_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.reset_button_box.set_halign(Gtk.Align.CENTER)
        self.reset_button_box.append(Gtk.Image.new_from_icon_name( \
            'view-refresh-symbolic'))
        self.buttonReset.set_tooltip_text(jT["reset"])
        self.buttonReset.set_child(self.reset_button_box)
        self.buttonReset.add_css_class('flat')
        self.buttonReset.set_can_focus(False)
        self.buttonReset.connect('clicked', self.on_buttonReset_clicked)
        self.headerbar.pack_end(self.buttonReset)
        
        # Stop timer button
        self.buttonStop = Gtk.Button.new()
        self.stop_button_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.stop_button_box.append(Gtk.Image.new_from_icon_name( \
            'media-playback-stop-symbolic'))
        self.stop_button_box.append(Gtk.Label.new(jT["stop"]))
        self.buttonStop.set_child(self.stop_button_box)
        self.buttonStop.set_can_focus(True)
        self.buttonStop.add_css_class('destructive-action')
        self.buttonStop.connect("clicked", self.on_buttonStop_clicked)
        
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
        self.adw_action_row_time.add_suffix(widget=self.timerBox)
        self.lbox.append(child=self.adw_action_row_time)
        
        self.mainBox.append(self.lbox)
    
    # Properties
    def properties(self):
        self.adw_expander_row = Adw.ExpanderRow.new()
        self.adw_expander_row.set_title(title=jT["preferences"])
        self.adw_expander_row.set_subtitle(subtitle=jT["preferences_desc"])
        self.lbox.append(child=self.adw_expander_row)
        
        # Adw.ComboRow - spinner size
        sizes = Gtk.StringList.new(strings=[
            '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60 (%s)' % jT["default"], '65', '70', '75', '80'
        ])
        
        self.adw_action_row_00 = Adw.ComboRow.new()
        self.adw_action_row_00.set_icon_name(icon_name='content-loading-symbolic')
        self.adw_action_row_00.set_title(title=jT["spinner"])
        self.adw_action_row_00.set_model(model=sizes)
        self.adw_action_row_00.set_subtitle(subtitle=jT["spinner_size_desc"])
        self.adw_action_row_00.set_subtitle_lines(2)
        self.adw_action_row_00.connect('notify::selected-item', self.on_combo_box_text_changed)
        self.adw_expander_row.add_row(child=self.adw_action_row_00)
        
        if os.path.exists(f'{CONFIG}/spinner.json'):
            with open(f'{CONFIG}/spinner.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["spinner-size"]
            if combobox_s == "5":
                self.adw_action_row_00.set_selected(0)
            elif combobox_s == "10":
                self.adw_action_row_00.set_selected(1)
            elif combobox_s == "15":
                self.adw_action_row_00.set_selected(2)
            elif combobox_s == "20":
                self.adw_action_row_00.set_selected(3)
            elif combobox_s == "25":
                self.adw_action_row_00.set_selected(4)
            elif combobox_s == "30":
                self.adw_action_row_00.set_selected(5)
            elif combobox_s == "35":
                self.adw_action_row_00.set_selected(6)
            elif combobox_s == "40":
                self.adw_action_row_00.set_selected(7)
            elif combobox_s == "45":
                self.adw_action_row_00.set_selected(8)
            elif combobox_s == "50":
                self.adw_action_row_00.set_selected(9)
            elif combobox_s == "55":
                self.adw_action_row_00.set_selected(10)
            elif combobox_s == '60 (%s)' % jT["default"]:
                self.adw_action_row_00.set_selected(11)
            elif combobox_s == "65":
                self.adw_action_row_00.set_selected(12)
            elif combobox_s == "70":
                self.adw_action_row_00.set_selected(13)
            elif combobox_s == "75":
                self.adw_action_row_00.set_selected(14)
            elif combobox_s == "80":
                self.adw_action_row_00.set_selected(15)
        else:
            self.adw_action_row_00.set_selected(11)
        
        # Adw.ComboRow - Actions
        actions = Gtk.StringList.new(strings=[
            jT["default"], jT["shut_down"], jT["reboot"], jT["suspend"], jT["play_alarm_clock"]
        ])
        
        self.adw_action_row_01 = Adw.ComboRow.new()
        self.adw_action_row_01.set_icon_name(icon_name='timer-symbolic')
        self.adw_action_row_01.set_title(title=jT["action_after_timing"])
        self.adw_action_row_01.set_title_lines(2)
        self.adw_action_row_01.set_model(model=actions)
        self.adw_action_row_01.connect('notify::selected-item', self.on_combo_box_text_s_changed)
        self.adw_expander_row.add_row(child=self.adw_action_row_01)
        
        if os.path.exists(f'{CONFIG}/actions.json'):
            with open(f'{CONFIG}/actions.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["action"]
            if combobox_s == jT["default"]:
                self.adw_action_row_01.set_selected(0)
            elif combobox_s == jT["shut_down"]:
                self.adw_action_row_01.set_selected(1)
            elif combobox_s == jT["reboot"]:
                self.adw_action_row_01.set_selected(2)
            elif combobox_s == jT["suspend"]:
                self.adw_action_row_01.set_selected(3)
            elif combobox_s == jT["play_alarm_clock"]:
                self.adw_action_row_01.set_selected(4)
        else:
            self.adw_action_row_01.set_selected(0)
        
        # Adw ActionRow - Theme configuration
        ## Gtk.Switch
        self.switch_01 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/theme.json'):
            with open(f'{CONFIG}/theme.json') as r:
                jR = json.load(r)
            dark = jR["theme"]
            if dark == "dark":
                self.switch_01.set_active(True)
        self.switch_01.set_valign(align=Gtk.Align.CENTER)
        self.switch_01.connect('notify::active', self.on_switch_01_toggled)
        
        ## Adw.ActionRow
        self.adw_action_row_02 = Adw.ActionRow.new()
        self.adw_action_row_02.set_icon_name(icon_name='weather-clear-night-symbolic')
        self.adw_action_row_02.set_title(title=jT["dark_theme"])
        self.adw_action_row_02.set_subtitle(subtitle=jT["theme_desc"])
        self.adw_action_row_02.add_suffix(widget=self.switch_01)
        self.adw_expander_row.add_row(child=self.adw_action_row_02)
        
        # Adw ActionRow - Resizable of Window configuration
        ## Gtk.Switch
        self.switch_02 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/window.json'):
            with open(f'{CONFIG}/window.json') as r:
                jR = json.load(r)
            resizable = jR["resizable"]
            if resizable == "true":
                self.switch_02.set_active(True)
        self.switch_02.set_valign(align=Gtk.Align.CENTER)
        self.switch_02.connect('notify::active', self.on_switch_02_toggled)
        
        ## Adw.ActionRow
        self.adw_action_row_03 = Adw.ActionRow.new()
        self.adw_action_row_03.set_icon_name(icon_name='window-maximize-symbolic')
        self.adw_action_row_03.set_title(title=jT["resizable_of_window"])
        self.adw_action_row_03.add_suffix(widget=self.switch_02)
        self.adw_action_row_03.set_activatable_widget(widget=self.switch_02)
        self.adw_expander_row.add_row(child=self.adw_action_row_03)
        
        # Adw ActionRow - custom notification
        ## Adw.EntryRow
        self.entry = Adw.EntryRow()
        self.apply_entry_text()
        self.entry.set_show_apply_button(True)
        self.entry.set_enable_emoji_completion(True)
        self.entry.connect('changed', self.on_entry_text_changed)
        
        ## Adw.ActionRow
        self.adw_action_row_04 = Adw.ActionRow.new()
        self.adw_action_row_04.set_icon_name(icon_name='notification-symbolic')
        self.adw_action_row_04.set_title(title=jT["custom_notification"])
        self.adw_action_row_04.set_title_lines(2)
        self.adw_action_row_04.add_suffix(widget=self.entry)
        self.adw_action_row_04.set_activatable_widget(widget=self.entry)
        self.adw_expander_row.add_row(child=self.adw_action_row_04)
        
        # Adw ActionRow - play beep
        ## Gtk.Switch
        self.switch_03 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/beep.json'):
            with open(f'{CONFIG}/beep.json') as r:
                jR = json.load(r)
            beep = jR["play-beep"]
            if beep == "false":
                self.switch_03.set_active(False)
            else:
                self.switch_03.set_active(True)
        else:
            self.switch_03.set_active(True)
        self.switch_03.set_valign(align=Gtk.Align.CENTER)
        self.switch_03.connect('notify::active', self.on_switch_03_toggled)
        
        ## Adw.ActionRow
        self.adw_action_row_05 = Adw.ActionRow.new()
        self.adw_action_row_05.set_icon_name(icon_name='folder-music-symbolic')
        self.adw_action_row_05.set_title(title=jT["play_beep"])
        #self.adw_action_row_05.set_subtitle(subtitle=)
        self.adw_action_row_05.add_suffix(widget=self.switch_03)
        self.adw_expander_row.add_row(child=self.adw_action_row_05)
    
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
    
    # Apply entry text from file (custom notification text)
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
            
    # After launching
    ## Set selected theme
    def set_theme(self):
        if os.path.exists(f'{CONFIG}/theme.json'):
            with open(f'{CONFIG}/theme.json') as jt:
                t = json.load(jt)
            theme = t["theme"]
            if theme == "dark":
                self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.PREFER_DARK
                )
            elif theme == "light":
                self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.FORCE_LIGHT
                )
                
    ## Set resizable of window configuration
    def set_resizable_w(self):
        if os.path.exists(f'{CONFIG}/window.json'):
            with open(f'{CONFIG}/window.json') as jr:
                rezisable = json.load(jr)
            if rezisable == "true":
                self.set_resizable(True)
        else:
            self.set_resizable(False)
    
    ## Set selected spinner size
    def set_spinner_size(self):
        if os.path.exists(f'{CONFIG}/spinner.json'):
            with open(f'{CONFIG}/spinner.json') as j:
                jsonObject = json.load(j)
            spinner = jsonObject["spinner-size"]
            try:
                self.spinner.set_size_request(int(spinner), int(spinner))
            except ValueError:
                self.spinner.set_size_request(60,60)
        else:
            self.spinner.set_size_request(60,60)
    
    # Button actions
    ## Start button action
    def on_buttonStart_clicked(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.menu_button.set_can_focus(True)
        self.menu_button.do_focus(self.menu_button, True)
        self.start_timer()
        return True
    
    ## Stop button action
    def on_buttonStop_clicked(self, widget, *args):
        """ button "clicked" in event buttonStop. """
        self.menu_button.set_can_focus(True)
        self.menu_button.do_focus(self.menu_button, True)
        self.stop_timer()
        print(jT["timing_ended"])
    
    ## Reset button action
    def on_buttonReset_clicked(self, widget, *args):
        self.reset_timer()
    
    def on_SpinnerWindow_destroy(self, widget, *args):
        """ procesing closing window """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()
    
    # Timer actions
    ## On timeout function
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
        self.label.set_markup("<big>{}</big>".format(
            strfdelta(self.counter, "<b>{hours}</b> %s <b>{minutes}</b> %s <b>{seconds}</b> %s" % (jT["hours"], jT["mins"], jT["secs"]))
        ))
        return True
    
    ## Start timer function
    def start_timer(self):
        """ Run Timer. """
        self.check_and_save()
        self.headerbar.pack_start(self.buttonStop)
        self.headerbar.remove(self.buttonStart)
        self.headerbar.remove(self.buttonReset)
        self.mainBox.remove(self.lbox)
        self.non_activated_session()
        self.counter = timedelta(hours = int(self.hour_entry.get_text()), minutes = int(self.minute_entry.get_text()), seconds = int(self.secs_entry.get_text()))
        #self.play_beep()
        self.label.set_markup("<big>{}</big>".format(
            strfdelta(self.counter, "<b>{hours}</b> %s <b>{minutes}</b> %s <b>{seconds}</b> %s" % (jT["hours"], jT["mins"], jT["secs"]))
        ))
        self.spinner.start()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)
        
    ## Stop timer function
    def stop_timer(self):
        """ Stop Timer """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.headerbar.remove(self.buttonStop)
        self.headerbar.pack_start(self.buttonStart)
        self.headerbar.pack_end(self.buttonReset)
        self.mainBox.append(self.lbox)
        self.mainBox.remove(self.timingBox)
        #self.label.set_label(alabeltext)
        #self.play_beep()
    
    ## Reset time counter values action
    def reset_timer(self):
        self.hour_entry.set_text('0')
        self.minute_entry.set_text('0')
        self.secs_entry.set_text('0')
    
    # Function, that allocates labels in the current timing
    def non_activated_session(self):
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
            elif action == jT["play_alarm_clock"]:
                self.label_action.set_text(jT["play_alarm_clock_desc"])
        else:
            self.label_action.set_text(jT["notification_desc"])
    
    # After finished timer
    ## Function, that allocates actions after finished timer (e.g. shut down/reboot/suspend system)
    def session(self):
        if os.path.exists(f'{CONFIG}/actions.json'):
            with open(f'{CONFIG}/actions.json') as a:
                jA = json.load(a)
            action = jA["action"]
            if action == jT["default"]:
                self.play_beep()
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
                os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Suspend" boolean:true')
            elif action == jT["play_alarm_clock"]:
                self.alarm_clock()
        else:
            self.play_beep()
            self.notification()
            
    ## Play alarm clock
    def alarm_clock(self):
        dialogRingstone = Adw.MessageDialog.new(self, jT["timing_finished"], None)
        rBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        rImage = Gtk.Image.new_from_icon_name("history")
        rImage.set_pixel_size(40)
        rBox.append(rImage)
        rLabel = Gtk.Label.new()
        rLabel.set_markup("{} {} {} {} {} {}".format(self.hour_entry.get_text(), jT["hours"], self.minute_entry.get_text(), jT["mins"], self.secs_entry.get_text(), jT["secs"]))
        rBox.append(rLabel)
        dialogRingstone.set_extra_child(rBox)
        dialogRingstone.add_response('cancel', jT["cancel"])
        dialogRingstone.add_response('start', jT["start_again"])
        dialogRingstone.set_response_appearance('start', Adw.ResponseAppearance.SUGGESTED)
        dialogRingstone.connect('response', self.start_again)
        dialogRingstone.show()
        os.popen("ffplay -nodisp -autoexit /app/share/beeps/Oxygen-Im-Phone-Ring.ogg > /dev/null 2>&1 \
        && ffplay -nodisp -autoexit /app/share/beeps/Oxygen-Im-Phone-Ring.ogg > /dev/null 2>&1 \
        && ffplay -nodisp -autoexit /app/share/beeps/Oxygen-Im-Phone-Ring.ogg > /dev/null 2>&1 \
        && ffplay -nodisp -autoexit /app/share/beeps/Oxygen-Im-Phone-Ring.ogg > /dev/null 2>&1 \
        && ffplay -nodisp -autoexit /app/share/beeps/Oxygen-Im-Phone-Ring.ogg > /dev/null 2>&1 && \
        ffplay -nodisp -autoexit /app/share/beeps/Oxygen-Im-Phone-Ring.ogg > /dev/null 2>&1 && \
        ffplay -nodisp -autoexit /app/share/beeps/Oxygen-Im-Phone-Ring.ogg > /dev/null 2>&1")
        
    def start_again(self, w, response):
        if response == 'start':
            self.start_timer()
            os.popen('pkill -15 ffplay')
        elif response == 'cancel':
            os.popen('pkill -15 ffplay')
    
    ## Send notification after finished timer (if this action is selected in actions.json config file)
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
    
    ## Play beep after finished timer
    def play_beep(self):
        if os.path.exists(f'{CONFIG}/beep.json'):
            with open(f'{CONFIG}/beep.json') as r:
                jR = json.load(r)
            beep = jR["play-beep"]
            if beep == "false":
                print("")
            else:
                os.popen("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        else:
            os.popen("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
    
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
    
    # Keyboard shortcuts action
    def keys(self, keyval, keycode, state, user_data, win):
        if keycode == ord('q'):
            win.close()
        if keycode == ord('?'):
            self.keys = Dialog_keys(self)
        if keycode == ord('s'):
            self.menu_button.set_can_focus(True)
            self.menu_button.do_focus(self.menu_button, True)
            self.start_timer()
            return True
        if keycode == ord('c'):
            self.stop_timer()
        if keycode == ord('r'):
            self.reset_timer()
        if keycode == ord('d'):
            self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.PREFER_DARK
                )
            with open(f'{CONFIG}/theme.json', 'w') as kT:
                kT.write('{\n "theme": "dark"\n}')
        if keycode == ord('l'):
            self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.FORCE_LIGHT
                )
            with open(f'{CONFIG}/theme.json', 'w') as kT:
                kT.write('{\n "theme": "light"\n}')
        
# Adw Application class
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.create_action('shortcuts', self.on_shortcuts_action)
        self.create_action('about', self.on_about_action)
        self.create_action('reset_settings', self.on_reset_settings_action)
    
    # Run Keyboard shortcuts dialog
    def on_shortcuts_action(self, action, param):
        self.keys = Dialog_keys(self)
    
    # Run About dialog
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name(jT["timer_title"])
        dialog.set_version("2.6")
        dialog.set_developer_name("vikdevelop")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/timer")
        dialog.set_issue_url("https://github.com/vikdevelop/timer/issues")
        dialog.add_credit_section(jT["contributors"], ["Albano Battistella https://github.com/albanobattistella", "Allan Nordhøy https://hosted.weblate.org/user/kingu/", "haggen88 https://github.com/haggen88","J. Lavoie https://hosted.weblate.org/user/Edanas", "Kefir2105 https://github.com/Kefir2105", "KenyC https://github.com/KenyC", "linuxmasterclub https://hosted.weblate.org/user/linuxmasterclub/", "rene-coty https://github.com/rene-coty", "Vin https://hosted.weblate.org/user/VinLin", "ViktorOn https://github.com/ViktorOn"])
        dialog.set_translator_credits(jT["translator_credits"])
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("com.github.vikdevelop.timer")
        dialog.show()
        
    def on_reset_settings_action(self, action, param):
        self.dialog_reset = Dialog_reset(self)
        
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
