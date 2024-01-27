from timer import *

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
                <property name="accelerator">&lt;primary&gt;m</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
          </object>\
        </child>\
        <child>\
          <object class="GtkShortcutsGroup">\
            <property name="title" translatable="yes"></property>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">F1</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">F2</property>\
                <property name="title" translatable="yes">%s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="accelerator">F3</property>\
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
</interface>' % (jT["run_timer"], jT["stop_timer"], jT["quit"], jT["show"], jT["reset_counter"], jT["pause_timer"], jT["continue_timer"], jT["go_to_notification_settings"], jT["go_to_more_settings"], jT["show_about_dialog"], jT["activate_dark_theme"], jT["activate_system_theme"], jT["delete_timer_settings"])
