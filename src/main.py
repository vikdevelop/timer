import subprocess
import sys
import json
import os
import time
from datetime import timedelta
sys.path.append('/app')
from timer import *
from src.CHANGELOG import *
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

        self.set_heading(heading=jT["delete_timer_settings"])
        self.set_body(body=jT["dialog_remove_warning"])
        self.add_response('no', jT["cancel"])
        self.add_response('yes', jT["reset"])
        self.set_response_appearance(
            response='yes',
            appearance=Adw.ResponseAppearance.DESTRUCTIVE
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
        content_area.set_margin_top(margin=12)
        content_area.set_margin_end(margin=12)
        content_area.set_margin_bottom(margin=12)
        content_area.set_margin_start(margin=12)
        
        listbox = Gtk.ListBox.new()
        listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        listbox.get_style_context().add_class(class_name='boxed-list')
        content_area.append(child=listbox)
        
        # Ctrl+S shortcut
        box_sTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_sTimer.set_margin_top(10)
        box_sTimer.set_margin_bottom(10)
        
        button_sc = Gtk.Button.new_with_label("Ctrl")
        box_sTimer.append(button_sc)
        
        label_plus = Gtk.Label.new(str="+")
        box_sTimer.append(label_plus)
        
        button_s = Gtk.Button.new_with_label("S")
        box_sTimer.append(button_s)
        
        adw_action_row_start = Adw.ActionRow()
        adw_action_row_start.set_title(jT["run_timer"])
        adw_action_row_start.set_title_lines(3)
        adw_action_row_start.add_prefix(box_sTimer)
        listbox.append(adw_action_row_start)
        
        # Ctrl+C shortcut
        box_cTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_cTimer.set_margin_top(10)
        box_cTimer.set_margin_bottom(10)
        
        button_tc = Gtk.Button.new_with_label("Ctrl")
        box_cTimer.append(button_tc)
        
        label_plus = Gtk.Label.new(str="+")
        box_cTimer.append(label_plus)
        
        button_t = Gtk.Button.new_with_label("C")
        box_cTimer.append(button_t)
        
        adw_action_row_stop = Adw.ActionRow()
        adw_action_row_stop.set_title(jT["stop_timer"])
        adw_action_row_stop.set_title_lines(3)
        adw_action_row_stop.set_tooltip_text(jT["alternative_key"].format("EsC"))
        adw_action_row_stop.add_prefix(box_cTimer)
        listbox.append(adw_action_row_stop)
        
        # Ctrl+Q shortcut
        box_qTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_qTimer.set_margin_top(10)
        box_qTimer.set_margin_bottom(10)
        
        button = Gtk.Button.new_with_label("Ctrl")
        box_qTimer.append(button)
        
        label_plus = Gtk.Label.new(str="+")
        box_qTimer.append(label_plus)
        
        button_q = Gtk.Button.new_with_label("Q")
        box_qTimer.append(button_q)
        
        adw_action_row_quit = Adw.ActionRow()
        adw_action_row_quit.set_title(jT["quit"])
        adw_action_row_quit.set_title_lines(3)
        adw_action_row_quit.set_tooltip_text(jT["alternative_key"].format("Alt+F4"))
        adw_action_row_quit.add_prefix(box_qTimer)
        listbox.append(adw_action_row_quit)
        
        # Ctrl+? shortcut
        box_kTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_kTimer.set_margin_top(10)
        box_kTimer.set_margin_bottom(10)
        
        button_hc = Gtk.Button.new_with_label("Ctrl")
        box_kTimer.append(button_hc)
        
        label_plus = Gtk.Label.new(str="+")
        box_kTimer.append(label_plus)
        
        button_h = Gtk.Button.new_with_label("?")
        box_kTimer.append(button_h)
        
        adw_action_row_key = Adw.ActionRow()
        adw_action_row_key.set_title(jT["show"])
        adw_action_row_key.set_title_lines(3)
        adw_action_row_key.add_prefix(box_kTimer)
        listbox.append(adw_action_row_key)
        
        # Ctrl+R shortcut
        box_rTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_rTimer.set_margin_top(10)
        box_rTimer.set_margin_bottom(10)
        
        button_rc = Gtk.Button.new_with_label("Ctrl")
        box_rTimer.append(button_rc)
        
        label_plus = Gtk.Label.new(str="+")
        box_rTimer.append(label_plus)
        
        button_r = Gtk.Button.new_with_label("R")
        box_rTimer.append(button_r)
        
        adw_action_row_reset = Adw.ActionRow()
        adw_action_row_reset.set_title(jT["reset_counter"])
        adw_action_row_reset.set_title_lines(3)
        adw_action_row_reset.add_prefix(box_rTimer)
        listbox.append(adw_action_row_reset)
        
        # Ctrl+P shortcut
        box_pTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_pTimer.set_margin_top(10)
        box_pTimer.set_margin_bottom(10)
        
        button_pc = Gtk.Button.new_with_label("Ctrl")
        box_pTimer.append(button_pc)
        
        label_plus = Gtk.Label.new(str="+")
        box_pTimer.append(label_plus)
        
        button_p = Gtk.Button.new_with_label("P")
        box_pTimer.append(button_p)
        
        adw_action_row_pause = Adw.ActionRow()
        adw_action_row_pause.set_title(jT["pause_timer"])
        adw_action_row_pause.set_title_lines(3)
        adw_action_row_pause.set_tooltip_text(jT["alternative_key"].format("(Left) Shift"))
        adw_action_row_pause.add_prefix(box_pTimer)
        listbox.append(adw_action_row_pause)
        
        # Ctrl+T shortcut
        box_coTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_coTimer.set_margin_top(10)
        box_coTimer.set_margin_bottom(10)
        
        button_tc = Gtk.Button.new_with_label("Ctrl")
        box_coTimer.append(button_tc)
        
        label_plus = Gtk.Label.new(str="+")
        box_coTimer.append(label_plus)
        
        button_t = Gtk.Button.new_with_label("T")
        box_coTimer.append(button_t)
        
        adw_action_row_cont = Adw.ActionRow()
        adw_action_row_cont.set_title(jT["continue_timer"])
        adw_action_row_cont.set_title_lines(3)
        adw_action_row_quit.set_tooltip_text(jT["alternative_key"].format("(Right) Shift"))
        adw_action_row_cont.add_prefix(box_coTimer)
        listbox.append(adw_action_row_cont)
        
        # F1 shortcut
        box_about = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_about.set_margin_top(10)
        box_about.set_margin_bottom(10)
        
        button_aTimer = Gtk.Button.new_with_label("F1")
        box_about.append(button_aTimer)
        
        adw_action_row_about = Adw.ActionRow()
        adw_action_row_about.set_title(jT["show_about_dialog"])
        adw_action_row_about.set_title_lines(3)
        adw_action_row_about.add_prefix(box_about)
        listbox.append(adw_action_row_about)
        
        # F2 shortcut
        box_dTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_dTimer.set_margin_top(10)
        box_dTimer.set_margin_bottom(10)
        
        button_d = Gtk.Button.new_with_label("F2")
        box_dTimer.append(button_d)
        
        adw_action_row_dark = Adw.ActionRow()
        adw_action_row_dark.set_title(jT["activate_dark_theme"])
        adw_action_row_dark.set_title_lines(3)
        adw_action_row_dark.add_prefix(box_dTimer)
        listbox.append(adw_action_row_dark)
        
        # F3 shortcut
        box_tTimer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_tTimer.set_margin_top(10)
        box_tTimer.set_margin_bottom(10)
        
        button_lc = Gtk.Button.new_with_label("F3")
        box_tTimer.append(button_lc)
        
        adw_action_row_system = Adw.ActionRow()
        adw_action_row_system.set_title(jT["activate_system_theme"])
        adw_action_row_system.set_title_lines(3)
        adw_action_row_system.add_prefix(box_tTimer)
        listbox.append(adw_action_row_system)
        
        # F5 shortcut
        box_delSetttings = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box_delSetttings.set_margin_top(10)
        box_delSetttings.set_margin_bottom(10)
        
        button_rTimer = Gtk.Button.new_with_label("F5")
        box_delSetttings.append(button_rTimer)
        
        adw_action_row_remove = Adw.ActionRow()
        adw_action_row_remove.set_title(jT["delete_timer_settings"])
        adw_action_row_remove.set_title_lines(3)
        adw_action_row_remove.add_prefix(box_delSetttings)
        listbox.append(adw_action_row_remove)
        
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
        self.set_w_size()
        self.connect('close-request', self.close_action, self)
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
        self.mainBox.set_margin_start(47)
        self.mainBox.set_margin_end(47)
        self.set_child(self.mainBox)
        
        # App menu
        self.menu_button_model = Gio.Menu()
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
        
        # Load latest translations from GitHub
        app.load_locales()
        
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
        ## Gio.Menu()
        self.ResetMenu = Gio.Menu.new()
        self.reset_item = Gio.MenuItem.new()
        self.reset_item.set_label(label=jT["delete_timer_settings"])
        self.reset_item.set_detailed_action(
            detailed_action='app.reset_settings',
        )
        self.ResetMenu.append_item(self.reset_item)
        
        ## Gtk.Popover()
        self.rPopover = Gtk.PopoverMenu.new_from_model(self.ResetMenu)
        
        ## Adw.SplitButton()
        self.buttonReset = Adw.SplitButton.new()
        self.buttonReset.set_popover(popover=self.rPopover)
        self.buttonReset.set_halign(align=Gtk.Align.CENTER)
        self.buttonReset.connect('clicked', self.on_buttonReset_clicked)
        self.headerbar.pack_end(child=self.buttonReset)
        
        ## Adw.ButtonContent()
        self.rButtonContent = Adw.ButtonContent.new()
        self.rButtonContent.set_icon_name(icon_name='view-refresh-symbolic')
        self.rButtonContent.set_tooltip_text(jT["reset_counter"])
        self.rButtonContent.set_use_underline(use_underline=True)
        self.buttonReset.set_child(self.rButtonContent)
        
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
        
        # Pause timer button
        self.buttonPause = Gtk.Button.new_from_icon_name("media-playback-pause-symbolic")
        self.buttonPause.add_css_class("circular")
        self.buttonPause.remove_css_class("flat")
        self.buttonPause.connect("clicked", self.on_buttonPause_clicked)
        
        # Continue timer button
        self.buttonCont = Gtk.Button.new_from_icon_name("media-playback-start-symbolic")
        self.buttonCont.add_css_class("circular")
        self.buttonCont.add_css_class("suggested-action")
        self.buttonCont.connect("clicked", self.on_buttonCont_clicked)
        
        self.timeout_id = None
        self.connect("destroy", self.on_SpinnerWindow_destroy)
    
    # Entries of seconds, minutes and hours
    def make_timer_box(self):
        # Load counter.json (config file with time counter values)
        if os.path.exists(f'{CONFIG}/counter.json'):
            with open(f'{CONFIG}/counter.json') as jc:
                jC = json.load(jc)
            self.hour_e = jC["hour"]
            self.min_e = jC["minutes"]
            self.sec_e = jC["seconds"]
        else:
            self.hour_e = "0"
            self.min_e = "1"
            self.sec_e = "0"
        # Layout
        self.timerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        self.timerBox.set_margin_start(0)
        self.timerBox.set_margin_end(0)
        
        self.lbox = Gtk.ListBox.new()
        self.lbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.lbox.get_style_context().add_class(class_name='boxed-list')
        
        # Hour entry and label
        self.hour_entry = Adw.EntryRow()
        self.hour_entry.set_text(self.hour_e)
        self.hour_entry.set_title(jT["hours"])
        self.hour_entry.set_alignment(xalign=1)
        self.timerBox.append(self.hour_entry)
        
        # Minute entry and label
        self.minute_entry = Adw.EntryRow()
        self.minute_entry.set_text(self.min_e)
        self.minute_entry.set_title(jT["mins"])
        self.minute_entry.set_alignment(xalign=1)
        self.timerBox.append(self.minute_entry)
        
        # Second entry and label
        self.secs_entry = Adw.EntryRow()
        self.secs_entry.set_text(self.sec_e)
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
        
        # Adw.ComboRow - Actions
        actions = Gtk.StringList.new(strings=[
            jT["default"], jT["shut_down"], jT["reboot"], jT["suspend"], jT["play_alarm_clock"]
        ])
        
        self.adw_action_row_timer = Adw.ComboRow.new()
        self.adw_action_row_timer.set_icon_name(icon_name='timer-symbolic')
        self.adw_action_row_timer.set_title(title=jT["action_after_timing"])
        self.adw_action_row_timer.set_title_lines(2)
        self.adw_action_row_timer.set_model(model=actions)
        self.adw_action_row_timer.connect('notify::selected-item', self.on_combo_box_text_s_changed)
        self.adw_expander_row.add_row(child=self.adw_action_row_timer)
        
        if os.path.exists(f'{CONFIG}/actions.json'):
            with open(f'{CONFIG}/actions.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["action"]
            if combobox_s == jT["default"]:
                self.adw_action_row_timer.set_selected(0)
            elif combobox_s == jT["shut_down"]:
                self.adw_action_row_timer.set_selected(1)
            elif combobox_s == jT["reboot"]:
                self.adw_action_row_timer.set_selected(2)
            elif combobox_s == jT["suspend"]:
                self.adw_action_row_timer.set_selected(3)
            elif combobox_s == jT["play_alarm_clock"]:
                self.adw_action_row_timer.set_selected(4)
        else:
            self.adw_action_row_timer.set_selected(0)
            
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
        self.adw_action_row_beep = Adw.ActionRow.new()
        self.adw_action_row_beep.set_icon_name(icon_name='folder-music-symbolic')
        self.adw_action_row_beep.set_title(title=jT["play_beep"])
        self.adw_action_row_beep.add_suffix(widget=self.switch_03)     
        self.adw_action_row_beep.set_activatable_widget(widget=self.switch_03)
        self.adw_expander_row.add_row(child=self.adw_action_row_beep)
        
        # Adw ActionRow - custom notification
        ## Gtk.Button
        self.setButton = Gtk.Button.new_from_icon_name('go-next-symbolic')
        self.setButton.add_css_class('circular')
        self.setButton.add_css_class('flat')
        self.setButton.connect('clicked', self.custom_notification)
        
        ## Adw.ActionRow
        self.adw_action_row_notification = Adw.ActionRow.new()
        self.adw_action_row_notification.set_icon_name(icon_name='notification-symbolic')
        self.adw_action_row_notification.set_title(title=jT["custom_notification"])
        self.adw_action_row_notification.set_title_lines(2)
        self.adw_action_row_notification.add_suffix(widget=self.setButton)
        self.adw_action_row_notification.set_activatable_widget(widget=self.setButton)
        self.adw_expander_row.add_row(child=self.adw_action_row_notification)
        
        # Adw.ActionRow - advanced settings
        ## Gtk.Button
        self.advButton = Gtk.Button.new_from_icon_name('go-next-symbolic')
        self.advButton.add_css_class('circular')
        self.advButton.add_css_class('flat')
        self.advButton.connect('clicked', self.advanced)
        
        ## Adw.ActionRow
        self.adw_action_row_adv = Adw.ActionRow.new()
        self.adw_action_row_adv.set_icon_name(icon_name='preferences-other-symbolic')
        self.adw_action_row_adv.set_title(title=jT["advanced"])
        self.adw_action_row_adv.set_title_lines(2)
        self.adw_action_row_adv.add_suffix(widget=self.advButton)
        self.adw_action_row_adv.set_activatable_widget(widget=self.advButton)
        self.adw_expander_row.add_row(child=self.adw_action_row_adv)
        
    ## Set custom notification text
    def custom_notification(self, widget, *args):
        self.mainBox.remove(self.lbox)
        self.mainBox.set_valign(Gtk.Align.START)
        self.mainBox.set_margin_top(15)
        self.headerbar.remove(self.buttonStart)
        
        # Back button
        self.backButton = Gtk.Button.new_from_icon_name('go-next-symbolic-rtl')
        self.backButton.connect('clicked', self.cancel_custom_notification)
        self.headerbar.pack_start(self.backButton)
        
        self.cbox = Gtk.ListBox.new()
        self.cbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.cbox.get_style_context().add_class(class_name='boxed-list')
        self.mainBox.append(self.cbox)
        
        # Adw.EntryRow
        self.entry = Adw.EntryRow()
        self.apply_entry_text()
        self.entry.set_title(jT["custom_notification"])
        self.entry.set_show_apply_button(True)
        self.entry.set_enable_emoji_completion(True)
        self.entry.connect('changed', self.on_entry_text_changed)
        self.cbox.append(self.entry)
        
        # Adw.ActionRow - use in notification
        ## Gtk.Switch
        self.switch_04 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/use_in_notification.json'):
            with open(f'{CONFIG}/use_in_notification.json') as n:
                jN = json.load(n)
            use_notification = jN["use_in_notification"]
            if use_notification == "false":
                self.switch_04.set_active(False)
            else:
                self.switch_04.set_active(True)
        else:
            self.switch_04.set_active(False)
        self.switch_04.set_valign(align=Gtk.Align.CENTER)
        self.switch_04.connect('notify::active', self.on_switch_04_toggled)
        
        ## Adw.ActionRow
        self.adw_action_row_06 = Adw.ActionRow.new()
        self.adw_action_row_06.set_title(title=jT["use_in_notification"])
        self.adw_action_row_06.add_suffix(widget=self.switch_04)
        self.adw_action_row_06.set_activatable_widget(widget=self.switch_04)
        self.cbox.append(self.adw_action_row_06)
        
        # Adw.ActionRow - use in alarm clock dialog
        ## Gtk.Switch
        self.switch_05 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/use_text_alarm.json'):
            with open(f'{CONFIG}/use_text_alarm.json') as a:
                jA = json.load(a)
            use_dialog = jA["use_in_alarm_clock_dialog"]
            if use_dialog == "true":
                self.switch_05.set_active(True)
            else:
                self.switch_05.set_active(False)
        else:
            self.switch_05.set_active(False)
        self.switch_05.set_valign(align=Gtk.Align.CENTER)
        self.switch_05.connect('notify::active', self.on_switch_05_toggled)
        
        ## Adw.ActionRow
        self.adw_action_row_07 = Adw.ActionRow.new()
        self.adw_action_row_07.set_title(title=jT["use_in_alarm_clock"])
        self.adw_action_row_07.add_suffix(widget=self.switch_05)
        self.adw_action_row_07.set_activatable_widget(widget=self.switch_05)
        self.cbox.append(self.adw_action_row_07)
        
    def cancel_custom_notification(self, widget, *args):
        self.mainBox.append(self.lbox)
        self.mainBox.remove(self.cbox)
        self.mainBox.set_valign(Gtk.Align.CENTER)
        self.mainBox.set_margin_top(0)
        self.headerbar.pack_start(self.buttonStart)
        self.headerbar.remove(self.backButton)
        
    ## Advanced settings section
    def advanced(self, widget, *args):
        self.mainBox.remove(self.lbox)
        self.mainBox.set_valign(Gtk.Align.START)
        self.mainBox.set_margin_top(15)
        self.headerbar.remove(self.buttonStart)
        self.set_title(jT["advanced"])
        
        # Back button
        self.backButton_A = Gtk.Button.new_from_icon_name('go-next-symbolic-rtl')
        self.backButton_A.connect('clicked', self.cancel_advanced)
        self.headerbar.pack_start(self.backButton_A)
        
        self.abox = Gtk.ListBox.new()
        self.abox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.abox.get_style_context().add_class(class_name='boxed-list')
        self.mainBox.append(self.abox)
        
        # Adw.ComboRow - spinner size
        sizes = Gtk.StringList.new(strings=[
            '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60 (%s)' % jT["default"], '65', '70', '75', '80'
        ])
        
        self.adw_action_row_spinner = Adw.ComboRow.new()
        self.adw_action_row_spinner.set_icon_name(icon_name='content-loading-symbolic')
        self.adw_action_row_spinner.set_title(title=jT["spinner"])
        self.adw_action_row_spinner.set_model(model=sizes)
        self.adw_action_row_spinner.set_subtitle(subtitle=jT["spinner_size_desc"])
        self.adw_action_row_spinner.set_subtitle_lines(2)
        self.adw_action_row_spinner.connect('notify::selected-item', self.on_combo_box_text_changed)
        self.abox.append(self.adw_action_row_spinner)
        
        if os.path.exists(f'{CONFIG}/spinner.json'):
            with open(f'{CONFIG}/spinner.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["spinner-size"]
            if combobox_s == "5":
                self.adw_action_row_spinner.set_selected(0)
            elif combobox_s == "10":
                self.adw_action_row_spinner.set_selected(1)
            elif combobox_s == "15":
                self.adw_action_row_spinner.set_selected(2)
            elif combobox_s == "20":
                self.adw_action_row_spinner.set_selected(3)
            elif combobox_s == "25":
                self.adw_action_row_spinner.set_selected(4)
            elif combobox_s == "30":
                self.adw_action_row_spinner.set_selected(5)
            elif combobox_s == "35":
                self.adw_action_row_spinner.set_selected(6)
            elif combobox_s == "40":
                self.adw_action_row_spinner.set_selected(7)
            elif combobox_s == "45":
                self.adw_action_row_spinner.set_selected(8)
            elif combobox_s == "50":
                self.adw_action_row_spinner.set_selected(9)
            elif combobox_s == "55":
                self.adw_action_row_spinner.set_selected(10)
            elif combobox_s == '60 (%s)' % jT["default"]:
                self.adw_action_row_spinner.set_selected(11)
            elif combobox_s == "65":
                self.adw_action_row_spinner.set_selected(12)
            elif combobox_s == "70":
                self.adw_action_row_spinner.set_selected(13)
            elif combobox_s == "75":
                self.adw_action_row_spinner.set_selected(14)
            elif combobox_s == "80":
                self.adw_action_row_spinner.set_selected(15)
        else:
            self.adw_action_row_spinner.set_selected(11)
            
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
        self.adw_action_row_theme = Adw.ActionRow.new()
        self.adw_action_row_theme.set_icon_name(icon_name='weather-clear-night-symbolic')
        self.adw_action_row_theme.set_title(title=jT["dark_theme"])
        self.adw_action_row_theme.set_subtitle(subtitle=jT["theme_desc"])
        self.adw_action_row_theme.add_suffix(widget=self.switch_01)
        self.abox.append(self.adw_action_row_theme)
        
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
        self.adw_action_row_window = Adw.ActionRow.new()
        self.adw_action_row_window.set_icon_name(icon_name='window-maximize-symbolic')
        self.adw_action_row_window.set_title(title=jT["resizable_of_window"])
        self.adw_action_row_window.add_suffix(widget=self.switch_02)
        self.adw_action_row_window.set_activatable_widget(widget=self.switch_02)
        self.abox.append(self.adw_action_row_window)
        
        ## Gtk.Switch
        self.switch_06 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/countdown.json'):
            with open(f'{CONFIG}/countdown.json') as r:
                jR = json.load(r)
            vertical = jR["vertical_time_text"]
            if vertical == "true":
                self.switch_06.set_active(True)
        self.switch_06.set_valign(align=Gtk.Align.CENTER)
        self.switch_06.connect('notify::active', self.on_switch_06_toggled)
        
        # Adw.ActionRow - show vertical countdown timer text
        ## Adw.ActionRow
        self.adw_action_row_verText = Adw.ActionRow.new()
        self.adw_action_row_verText.set_icon_name(icon_name='history-symbolic')
        self.adw_action_row_verText.set_title(title=jT["vertical_text"])
        self.adw_action_row_verText.add_suffix(widget=self.switch_06)
        self.adw_action_row_verText.set_activatable_widget(widget=self.switch_06)
        self.abox.append(self.adw_action_row_verText)
        
    def cancel_advanced(self, widget, *args):
        self.mainBox.append(self.lbox)
        self.mainBox.remove(self.abox)
        self.mainBox.set_valign(Gtk.Align.CENTER)
        self.mainBox.set_margin_top(0)
        self.headerbar.pack_start(self.buttonStart)
        self.headerbar.remove(self.backButton_A)
        self.set_title(jT["timer_title"])
    
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
    
    ## Set window size
    def set_w_size(self):
        if os.path.exists(f'{CONFIG}/window_size.json'):
            with open(f'{CONFIG}/window_size.json') as s:
                jS = json.load(s)
            width = jS["width"]
            height = jS["height"]
            self.set_default_size(int(width), int(height))
            self.set_size_request(425, 425)
        else:
            self.set_default_size(425, 425)
            self.set_size_request(425, 425)
    
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
        self.set_time_text()
        return True
    
    ## Start timer function
    def start_timer(self):
        """ Run Timer. """
        self.check_and_save()
        self.headerbar.pack_start(self.buttonStop)
        self.headerbar.pack_start(self.buttonPause)
        self.headerbar.remove(self.buttonStart)
        self.headerbar.remove(self.buttonReset)
        self.mainBox.remove(self.lbox)
        self.counter = timedelta(hours = int(self.hour_entry.get_text()), minutes = int(self.minute_entry.get_text()), seconds = int(self.secs_entry.get_text()))
        #self.play_beep()
        self.set_time_text()
        self.non_activated_session()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)
        
    ### Set time text function
    def set_time_text(self):
        if os.path.exists(f'{CONFIG}/countdown.json'):
            with open(f'{CONFIG}/countdown.json') as c:
                jC = json.load(c)
            self.vertical_text = jC["vertical_time_text"]
            if self.vertical_text == "true":
                self.label.set_markup("<span size='31200'>{}</span>".format(
                    strfdelta(self.counter, "<b>{hours}</b> %s \n<b>{minutes}</b> %s \n<b>{seconds}</b> %s" % (jT["hours"], jT["mins"], jT["secs"]))
                ))
            else:
                self.spinner.start()
                self.label.set_markup("<span size='20100'>{}</span>".format(
                    strfdelta(self.counter, "<b>{hours}</b> %s <b>{minutes}</b> %s <b>{seconds}</b> %s" % (jT["hours"], jT["mins"], jT["secs"]))
                ))
        else:
            self.spinner.start()
            self.label.set_markup("<span size='20100'>{}</span>".format(
                    strfdelta(self.counter, "<b>{hours}</b> %s <b>{minutes}</b> %s <b>{seconds}</b> %s" % (jT["hours"], jT["mins"], jT["secs"]))
                ))
        
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
        self.headerbar.remove(self.buttonPause)
        self.headerbar.remove(self.buttonCont)
        try:
            self.timingBox.remove(self.label_pause)
            self.timingBox.remove(self.label_paused_status)
        except AttributeError:
            print("")
        #self.label.set_label(alabeltext)
        #self.play_beep()
    
    ## Reset time counter values action
    def reset_timer(self):
        self.hour_entry.set_text('0')
        self.minute_entry.set_text('0')
        self.secs_entry.set_text('0')
        
    ## Pause timer
    def pause_timer(self):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.label_pause = Gtk.Label.new()
        self.label_paused_status = Gtk.Label.new(str=jT["paused"])
        self.timingBox.remove(self.label_action)
        self.timingBox.append(self.label_paused_status)
        if self.vertical_text == "true":
            self.label_pause.set_markup("<b><span size='31200'>{}</span></b>".format(self.label.get_text()))
        else:
            self.label_pause.set_markup("<b><span size='20100'>{}</span></b>".format(self.label.get_text()))
        self.timingBox.append(self.label_pause)
        self.timingBox.remove(self.label)
        self.headerbar.remove(self.buttonPause)
        self.headerbar.pack_start(self.buttonCont)
        
    ## Continue timer
    def continue_timer(self):
        #self.spinner.start()
        get_label_time = self.label.get_text()
        res = [int(i) for i in get_label_time.split() if i.isdigit()]
        print(str(res))
        self.hour_entry.set_text(str(res[0]))
        self.minute_entry.set_text(str(res[1]))
        self.secs_entry.set_text(str(res[2]))
        self.timingBox.remove(self.label_pause)
        self.timingBox.remove(self.label_paused_status)
        self.headerbar.pack_start(self.buttonPause)
        self.headerbar.remove(self.buttonCont)
        self.start_timer()
    
    # Function, that allocates labels in the current timing
    def non_activated_session(self):
        if self.vertical_text == "true":
            print("")
        else:
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
        self.dialogRingstone = Adw.MessageDialog.new(self)
        self.use_custom_text()
        rBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.adw_action_row_beep.add_suffix(widget=self.switch_03)      
        rImage = Gtk.Image.new_from_icon_name("history")
        rImage.set_pixel_size(40)
        rBox.append(rImage)
        rLabel = Gtk.Label.new()
        rLabel.set_markup("{} {} {} {} {} {}".format(self.hour_entry.get_text(), jT["hours"], self.minute_entry.get_text(), jT["mins"], self.secs_entry.get_text(), jT["secs"]))
        rBox.append(rLabel)
        self.dialogRingstone.set_extra_child(rBox)
        self.dialogRingstone.add_response('cancel', jT["cancel"])
        self.dialogRingstone.add_response('start', jT["start_again"])
        self.dialogRingstone.set_response_appearance('start', Adw.ResponseAppearance.SUGGESTED)
        self.dialogRingstone.connect('response', self.start_again)
        self.dialogRingstone.show()
        os.popen("bash /app/src/alarm.sh")
        
    def start_again(self, w, response):
        if response == 'start':
            self.start_timer()
            os.popen('pkill -15 bash && pkill -15 ffplay')
        elif response == 'cancel':
            os.popen('pkill -15 bash && pkill -15 ffplay')
        else:
            os.popen('pkill -15 bash && pkill -15 ffplay')
            
    def use_custom_text(self):
        if os.path.exists(f'{CONFIG}/notification.json'):
            with open(f'{CONFIG}/notification.json') as n:
                jN = json.load(n)
            text = jN["text"]
            if text == "":
                text = f'{jT["timing_finished"]}'
        else:
            text = f'{jT["timing_finished"]}'
        if os.path.exists(f'{CONFIG}/use_text_alarm.json'):
           with open(f'{CONFIG}/use_text_alarm.json') as a:
                jA = json.load(a)
                if jA["use_in_alarm_clock_dialog"] == "true":
                    self.dialogRingstone.set_heading(text)
                else:
                    self.dialogRingstone.set_heading(jT["timing_finished"])
        else:
            self.dialogRingstone.set_heading(text)
    
    ## Send notification after finished timer (if this action is selected in actions.json config file)
    def notification(self):
        if os.path.exists(f'{CONFIG}/use_in_notification.json'):
            with open(f'{CONFIG}/use_in_notification.json') as n:
                jN = json.load(n)
                if jN["use_in_notification"] == "true":
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
        else:
            try:
                subprocess.call(['notify-send',jT["timer_title"],notification,'-i','com.github.vikdevelop.timer'])
            except:
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
            print(jT["timing_ended"])
            self.stop_timer()
        if keycode == 0xFF1B: # Alternative key for stop timer (EsC)
            print(jT["timing_ended"])
            self.stop_timer()
        if keycode == ord('r'):
            self.reset_timer()
        if keycode == ord('p'):
            self.pause_timer()
        if keycode == 0xFFE1: # Left shift
            self.pause_timer()
        if keycode == 0xFFE2: # Right shift
            self.continue_timer()
        if keycode == ord('t'):
            try:
                self.timingBox.remove(label_pause)
            except:
                print("")
            self.continue_timer()
        if keycode == 0xFFBF:
            self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.PREFER_DARK
                )
            with open(f'{CONFIG}/theme.json', 'w') as kT:
                kT.write('{\n "theme": "dark"\n}')
            self.switch_01.set_active(True)
        if keycode == 0xFFC0:
            self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.FORCE_LIGHT
                )
            with open(f'{CONFIG}/theme.json', 'w') as kT:
                kT.write('{\n "theme": "system"\n}')
            self.switch_01.set_active(False)
        if keycode == 0xFFC2:
            self.dialog_reset = Dialog_reset(self)
    
    # Action after closing Timer window
    def close_action(self, widget, *args):
        # Save current window size
        if os.path.exists(f'{CONFIG}/window.json'):
            if self.get_allocation().width > 425:
                print("")
            if self.get_allocation().height > 425:
                print("")
            with open(f'{CONFIG}/window_size.json', 'w') as s:
                s.write('{\n "width": "%s",\n "height": "%s"\n}' % (self.get_allocation().width, self.get_allocation().height))
            
    # Button actions
    ## Start button action
    def on_buttonStart_clicked(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.menu_button.set_can_focus(True)
        self.menu_button.do_focus(self.menu_button, True)
        self.start_timer()
        return True
    
    ## Stop button action
    def on_buttonStop_clicked(self, buttonStop):
        """ button "clicked" in event buttonStop. """
        self.menu_button.set_can_focus(True)
        self.menu_button.do_focus(self.menu_button, True)
        self.stop_timer()
        print(jT["timing_ended"])
    
    ## Reset button action
    def on_buttonReset_clicked(self, buttonReset):
        self.reset_timer()
        
    ## Pause button action
    def on_buttonPause_clicked(self, buttonPause):
        self.pause_timer()
        
    ## Continue button action
    def on_buttonCont_clicked(self, buttonPause):
        self.continue_timer()
    
    def on_SpinnerWindow_destroy(self, widget, *args):
        """ procesing closing window """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()
        
    # Adw.ActionRow functions for activate tasks
    ## Save entry text (custom notification text)
    def on_entry_text_changed(self, entry):
        entry = self.entry.get_text()
        with open(f'{CONFIG}/notification.json', 'w') as n:
            n.write('{\n "custom-notification": "true",\n "text": "%s"\n}' % entry)
    
    ### Apply entry text from file (custom notification text)
    def apply_entry_text(self):
        if os.path.exists(f'{CONFIG}/notification.json'):
            with open(f'{CONFIG}/notification.json') as n:
                jN = json.load(n)
            text = jN["text"]
            self.entry.set_text(text)
    
    ## Save app theme configuration
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
    
    ## Save resizable window configuration
    def on_switch_02_toggled(self, switch02, GParamBoolean):
        if switch02.get_active():
            with open(f'{CONFIG}/window.json', 'w') as w:
                w.write('{\n "resizable": "true"\n}')
                self.set_resizable(True)
        else:
            os.remove(f'{CONFIG}/window.json')
            self.set_resizable(False)
            self.set_default_size(425, 425)
            self.set_size_request(425, 425)
            os.remove(f'{CONFIG}/window_size.json')
    
    ## Save playing beep configuration
    def on_switch_03_toggled(self, switch03, GParamBoolean):
        if switch03.get_active():
            with open(f'{CONFIG}/beep.json', 'w') as t:
                t.write('{\n "play-beep": "true"\n}')
        else:
            with open(f'{CONFIG}/beep.json', 'w') as t:
                t.write('{\n "play-beep": "false"\n}')
                
    ## Save notification text switch config
    def on_switch_04_toggled(self, switch04, GParamBoolean):
        if switch04.get_active():
            with open(f'{CONFIG}/use_in_notification.json', 'w') as t:
                t.write('{\n "use_in_notification": "true"\n}')
        else:
            with open(f'{CONFIG}/use_in_notification.json', 'w') as t:
                t.write('{\n "use_in_notification": "false"\n}')
                
    ## Save alarm clock text switch config
    def on_switch_05_toggled(self, switch05, GParamBoolean):
        if switch05.get_active():
            with open(f'{CONFIG}/use_text_alarm.json', 'w') as t:
                t.write('{\n "use_in_alarm_clock_dialog": "true"\n}')
        else:
            with open(f'{CONFIG}/use_text_alarm.json', 'w') as t:
                t.write('{\n "use_in_alarm_clock_dialog": "false"\n}')
                
    ## Save configuration of vertical text in countdown page
    def on_switch_06_toggled(self, switch06, GParamBoolean):
        if switch06.get_active():
            with open(f'{CONFIG}/countdown.json', 'w') as t:
                t.write('{\n "vertical_time_text": "true"\n}')
        else:
            with open(f'{CONFIG}/countdown.json', 'w') as t:
                t.write('{\n "vertical_time_text": "false"\n}')
    
    ## Save Combobox (actions) configuration
    def on_combo_box_text_s_changed(self, comborow, GParamObject):
        selected_item_02 = comborow.get_selected_item()
        with open(f'{CONFIG}/actions.json', 'w') as a:
            a.write('{\n "action": "%s"\n}' % selected_item_02.get_string())
    
    ## Save Combobox (spinner size) configuration
    def on_combo_box_text_changed(self, comborow, GParamObject):
        selected_item = comborow.get_selected_item()
        with open(f'{CONFIG}/spinner.json', 'w') as s:
            s.write('{\n "spinner-size": "%s"\n}' % selected_item.get_string())
        try:
            self.spinner.set_size_request(int(selected_item.get_string()), int(selected_item.get_string()))
        except ValueError:
            self.spinner.set_size_request(60,60)
        
# Adw Application class
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.create_action('shortcuts', self.on_shortcuts_action)
        self.create_action('about', self.on_about_action, ["F1"])
        self.create_action('reset_settings', self.on_reset_settings_action)
    
    # Run Keyboard shortcuts dialog
    def on_shortcuts_action(self, action, param):
        self.keys = Dialog_keys(self)
    
    # Run About dialog
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name(jT["timer_title"])
        dialog.set_version("2.9")
        dialog.set_release_notes(release_28 + release_27_11 + release_27I + release_27)
        dialog.set_developer_name("vikdevelop")
        self.add_translations_link(dialog)
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/timer")
        dialog.set_issue_url("https://github.com/vikdevelop/timer/issues")
        dialog.add_credit_section(jT["contributors"], ["Albano Battistella https://github.com/albanobattistella", "Allan Nordhøy https://hosted.weblate.org/user/kingu/", "gallegonovato https://github.com/gallegonovato", "haggen88 https://github.com/haggen88","J. Lavoie https://hosted.weblate.org/user/Edanas", "Kefir2105 https://github.com/Kefir2105", "KenyC https://github.com/KenyC", "linuxmasterclub https://hosted.weblate.org/user/linuxmasterclub/", "rene-coty https://github.com/rene-coty", "Vin https://hosted.weblate.org/user/VinLin", "ViktorOn https://github.com/ViktorOn"])
        dialog.set_translator_credits(jT["translator_credits"])
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("com.github.vikdevelop.timer")
        dialog.show()
    
    def add_translations_link(self, dialog):
        if lang == "en.json":
            dialog.add_link("Translate Timer to your language", "https://hosted.weblate.org/projects/vikdevelop/timer/")
        else:
            dialog.add_link("Contribute to translations", "https://hosted.weblate.org/projects/vikdevelop/timer/")

    def on_reset_settings_action(self, action, param):
        self.dialog_reset = Dialog_reset(self)
        
    def load_locales(self):
        os.popen("cd ~/.var/app/com.github.vikdevelop.timer/cache && wget -c {}/{} > /dev/null 2>&1 && pkill -15 wget && pkill -15 sh".format(BASE_URL, lang))
        
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
