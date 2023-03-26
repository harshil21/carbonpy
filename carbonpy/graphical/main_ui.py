try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gdk
except ModuleNotFoundError:
    raise ModuleNotFoundError("PyGObject isn't installed on your machine. Run pip install PyGObject")

from interface import Interface
from playground import Playground
from builder import builder


handlers = {
    "on_window1_destroy": Gtk.main_quit,
    # "on_button_clicked": Interface.on_button_clicked,
    "on_enter_notify_event": Interface.on_enter_notify_event,
    "on_leave_notify_event": Interface.on_leave_notify_event,
    # "on_event_label_button_press_event": on_event_label_button_press_event,
    # "on_event_label_motion_notify_event": on_event_label_motion_notify_event,
    "on_carbon_clicked": Playground().on_carbon_clicked,
    "on_carboncanvas_enter_notify_event": Interface.on_carboncanvas_enter_notify_event,
}

builder.connect_signals(handlers)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('./css_styles/styles.css')
screen = Gdk.Screen().get_default()
Gtk.StyleContext().add_provider_for_screen(screen, cssProvider,  Gtk.STYLE_PROVIDER_PRIORITY_USER)

window = builder.get_object("window1")
window.show_all()

Gtk.main()
