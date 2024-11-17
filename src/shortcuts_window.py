from __init__ import jT
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

SHORTCUTS_WINDOW = '<?xml version="1.0" encoding="UTF-8"?>\
<interface>\
  <requires lib="gtk" version="4.0"/>\
  <template class="ShortcutsWindow" parent="GtkShortcutsWindow">\
    <property name="modal">1</property>\
    <property name="destroy-with-parent">1</property>\
    <child>\
      <object class="GtkShortcutsSection">\
        <child>\
          <object class="GtkShortcutsGroup">\
            <property name="title" translatable="yes"></property>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;s</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;c</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;q</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;question</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;r</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;p</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;t</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">&lt;primary&gt;n</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">F5</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
          </object>\
        </child>\
      </object>\
    </child>\
  </template>\
</interface>' % (jT["run_timer"], jT["stop_timer"], jT["quit"], jT["show"], jT["reset_counter"], jT["pause_timer"], jT["continue_timer"], jT["new_window"], jT["delete_timer_settings"])

# Shortcuts window
@Gtk.Template(string=SHORTCUTS_WINDOW) # from shortcuts_window.py
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
