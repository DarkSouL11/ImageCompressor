import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import tinify, time


class authInterface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Enter API key")
        self.set_default_size(450, 150)
        self.set_border_width(20)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(self.vbox)

        self.api_input = Gtk.Entry(xalign=0)
        self.vbox.pack_start(self.api_input, True, True, 0)

        self.alert = Gtk.Label()
        self.vbox.pack_start(self.alert, True, True, 0)

        self.hbox = Gtk.Box(spacing=4, orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.set_homogeneous(False)
        self.vbox.pack_start(self.hbox, True, True, 0)

        self.auth_button = Gtk.Button(label="Authenticate")
        self.auth_button.connect("clicked", self.verify)
        self.hbox.pack_end(self.auth_button, True, False, 0)

        self.label = Gtk.Label()
        self.label.set_markup("<i>Don't have a key?</i> Get it <a href='https://tinypng.com/developers'>here</a>")
        self.vbox.pack_start(self.label, True, True, 0)
        self.set_resizable(False)

    def verify(self, widget):
        apikey = self.api_input.get_text()
        tinify.key = apikey
        self.alert.set_text("Checking...")
        while Gtk.events_pending():
                 Gtk.main_iteration_do(False)
        try:
            tinify.validate()
            keyfile = open('.apikey', 'w')
            print(apikey, file=keyfile)
            Gtk.main_quit()
            self.destroy()
        except Exception as e:
            self.api_input.set_text("")
            self.alert.set_text("Invalid API key, re-enter the key.")
