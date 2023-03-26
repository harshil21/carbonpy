from gi.repository import Gtk, Gdk


class Interface:

    @staticmethod
    def on_enter_notify_event(widget, event):
        # print('hovering carbons')
        widget.get_window().set_cursor(Gdk.Cursor.new_from_name(display=widget.get_display(), name="pointer"))

    @staticmethod
    def on_leave_notify_event(widget, event):
        # print("HOVEE leave")
        widget.get_window().set_cursor(cursor=None)

    @staticmethod
    def on_carboncanvas_enter_notify_event(widget, event):
        # print('carboncanvas hover')
        # Set 'grab' cursor-
        cursor = Gdk.Cursor.new_from_name(display=widget.get_display(), name="hand1")  # TODO: Revert back to 'grab'
        widget.get_window().set_cursor(cursor)


# def on_button_clicked(button):
#     print("Clicked!!")
#
#
# def on_event_label_button_press_event(widget, event):
#     pass  # print(widget)
#
#
# def on_event_label_motion_notify_event(widget, event):
#     widget.set_state_flags(Gtk.StateFlags.PRELIGHT, clear=True)

