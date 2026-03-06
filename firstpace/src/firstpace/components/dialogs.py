"""Common dialog components."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TextEntryDialog(Gtk.Dialog):
    def __init__(self, parent, title="", placeholder=""):
        super().__init__(title, parent,
                         Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        content = self.get_content_area()
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text(placeholder)
        content.add(self.entry)
        self.show_all()

    def get_text(self):
        return self.entry.get_text().strip()
