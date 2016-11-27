import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from interface import interface
from compressor import Compressor
import sys


if __name__ == "__main__":
    key = open('apikey.txt')
    API_KEY = key.readline()[:-1]
    key.close()
    print(API_KEY)
    if API_KEY:
        try:
            c = Compressor(API_KEY)
        except Exception:
            print("Please enter the right api key in apikey.txt file")
            sys.exit(1)
    else:
        print("Please enter the api key in apikey.txt file")
        sys.exit(1)
    window = interface(c)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
