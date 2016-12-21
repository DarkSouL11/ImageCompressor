import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from interface import interface
from compressor import Compressor
from loginUi import authInterface
import sys, os


if __name__ == "__main__":
    if not os.path.isfile('.apikey'):
        open('.apikey', 'w')
    key = open('.apikey')
    API_KEY = key.readline()[:-1]
    key.close()
    print(API_KEY)
    try:
        c = Compressor(API_KEY)
    except Exception:
        try:
            window = authInterface()
            window.connect("delete-event", Gtk.main_quit)
            window.show_all()
            Gtk.main()
            key = open('.apikey')
            API_KEY = key.readline()[:-1]
            key.close()
            c = Compressor(API_KEY)
        except Exception:
            print("Sorry something went wrong!")
            sys.exit(1)
    window = interface(c)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
