import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils import check, folder_convert, file_convert, url_convert
import time
from time import sleep
import sys



class interface(Gtk.Window):

    def __init__(self, compressor):
        # MAIN WINDOW

        self.compressor = compressor

        # variables used

        self.is_url = False
        self.is_folder = False
        self.m_replace = True
        self.OUTPUT_LOCATION = ""
        self.INPUT_LOCATION = ""

        Gtk.Window.__init__(self, title="ImageCompressor")
        self.set_default_size(500, 350)
        self.set_border_width(20)

        # Box that holds items Vertically

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(self.vbox)

        # Welcome title

        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=25)
        self.title = Gtk.Label("Welcome to ImageCompressor 1.0")
        self.hbox1.pack_start(self.title, True, True, 0)
        self.vbox.pack_start(self.hbox1, True, True, 0)

        # RADIO BUTTONS

        self.frame = Gtk.Frame()

        self.hbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.check1 = Gtk.RadioButton.new_with_label_from_widget(None,
                        "Convert a single image")
        self.check1.connect("toggled", self.on_button_toggled, "1")
        self.hbox2.pack_start(self.check1, True, True, 0)

        self.check2 = Gtk.RadioButton.new_from_widget(self.check1)
        self.check2.set_label("Convert all images in a folder")
        self.check2.connect("toggled", self.on_button_toggled, "2")
        self.hbox2.pack_start(self.check2, True, True, 0)

        self.check3 = Gtk.RadioButton.new_from_widget(self.check1)
        self.check3.set_label("Convert image from url")
        self.check3.connect("toggled", self.on_button_toggled, "3")
        self.hbox2.pack_start(self.check3, True, True, 0)

        self.frame.add(self.hbox2)
        self.vbox.pack_start(self.frame, True, True, 0)

        # INPUT SECTION

        self.input_lbox= Gtk.ListBox()
        self.vbox.pack_start(self.input_lbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(hbox)
        self.input_label = Gtk.Label("Input file", xalign=0)
        hbox.pack_start(self.input_label, True, True, 0)
        self.input_lbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.add(hbox)
        self.input_file = Gtk.Entry(xalign=0)
        self.input_button = Gtk.Button(label="Select")
        self.input_button.connect("clicked", self.choose_input)
        hbox.pack_start(self.input_file, True, True, 0)
        hbox.pack_start(self.input_button, False, True, 0)
        self.input_lbox.add(row)

        # REPLACE OPTION

        self.replace_lbox= Gtk.ListBox()
        self.vbox.pack_start(self.replace_lbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.add(hbox)
        self.replace_label = Gtk.Label("Replace the original image", xalign=0)
        self.replace_switch = Gtk.Switch()
        hbox.pack_start(self.replace_label, True, True, 0)
        hbox.pack_start(self.replace_switch, False, True, 0)
        self.replace_lbox.add(row)

        # OUTPUT SECTION

        self.output_lbox = Gtk.ListBox()
        self.vbox.pack_start(self.output_lbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(hbox)
        self.output_label = Gtk.Label("Output folder", xalign=0)
        hbox.pack_start(self.output_label, True, True, 0)
        self.output_lbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.add(hbox)
        self.output_file = Gtk.Entry(xalign=0)
        self.output_button = Gtk.Button(label="Select")
        self.output_button.connect("clicked", self.choose_output)
        hbox.pack_start(self.output_file, True, True, 0)
        hbox.pack_start(self.output_button, False, True, 0)
        self.output_lbox.add(row)

        self.replace_switch.connect("notify::active", self.on_switch_activated)
        self.replace_switch.set_active(True)
        self.output_lbox.set_sensitive(False)

        # Compress Button

        self.hbox3 = Gtk.Box(spacing=4, orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox3.set_homogeneous(False)
        self.vbox.pack_start(self.hbox3, True, True, 0)

        self.cancel_button = Gtk.Button("Cancel")
        self.cancel_button.connect("clicked", Gtk.main_quit)

        self.compress_button = Gtk.Button("Compress")
        self.compress_button.connect("clicked", self.final_compress)

        self.hbox3.pack_end(self.cancel_button, False, False, 0)
        self.hbox3.pack_end(self.compress_button, False, False, 0)
        self.set_resizable(False)


    def on_button_toggled(self, button, name):
        if button.get_active():
            if name == "3":
                self.is_url = True
                self.input_label.set_label("Input URL")
                self.replace_switch.set_sensitive(False)
                self.output_lbox.set_sensitive(True)
                self.input_button.set_sensitive(False)
            else:
                self.is_url = False
                self.replace_switch.set_sensitive(True)
                self.replace_switch.set_active(True)
                self.output_lbox.set_sensitive(False)
                self.input_button.set_sensitive(True)
                if name == "1":
                    self.is_folder = False
                    self.input_label.set_label("Input file")
                else:
                    self.is_folder = True
                    self.input_label.set_label("Input folder")
        self.input_file.set_text("")
        self.INPUT_LOCATION = ""


    def on_switch_activated(self, widget, gparam):
        self.OUTPUT_LOCATION = ""
        self.output_file.set_text("")
        if widget.get_active():
            self.m_replace = True
            self.output_lbox.set_sensitive(False)
        else:
            self.m_replace = False
            self.output_lbox.set_sensitive(True)

    def choose_input(self, widget):
        if self.is_folder:
            self.dialog = Gtk.FileChooserDialog("Please choose a folder", self,
                Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        else:
            self.dialog = Gtk.FileChooserDialog("Please choose a image", self,
                Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.dialog.set_default_size(300, 200)

        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            self.input_file.set_text(self.dialog.get_filename())
            self.INPUT_LOCATION = self.dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        self.dialog.destroy()

    def choose_output(self, widget):
        self.dialog = Gtk.FileChooserDialog("Choose a folder to save image",
            self, Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.dialog.set_default_size(300, 200)

        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            self.output_file.set_text(self.dialog.get_filename())
            self.OUTPUT_LOCATION = self.dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        self.dialog.destroy()

     def final_compress(self, widget):
        widget.set_sensitive(False)
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        self.INPUT_LOCATION = self.input_file.get_text()
        self.OUTPUT_LOCATION = self.output_file.get_text()
        def print_slowly(text):
            for c in text:
                print(c, end='')
                sys.stdout.flush()
                sleep(1.5)
        if self.is_url:
            if os.path.isdir(self.OUTPUT_LOCATION):
                print("Compressing ",self.INPUT_LOCATION,"  In Progress..",end="")
                print_slowly('.....')
                print(".",end="\r")
                url_convert(self.compressor, self.INPUT_LOCATION, self.OUTPUT_LOCATION)
            else:
                print("Invalid save path")
        elif check(self.INPUT_LOCATION, self.OUTPUT_LOCATION, self.m_replace, self.is_folder):
            if self.is_folder:
                print("Compressing ",self.INPUT_LOCATION,"  In Progress..",end="")
                print_slowly('.....')
                print("..",end="\r")
                folder_convert(self.compressor, self.INPUT_LOCATION,
                        replace=self.m_replace, output_path=self.OUTPUT_LOCATION)
            else:
                print("Compressing ",self.INPUT_LOCATION,"  In Progress..",end="")
                print_slowly('.....')
                print("..",end="\r")
                file_convert(self.compressor, self.INPUT_LOCATION,
                        replace=self.m_replace, output_path=self.OUTPUT_LOCATION)
        else:
            print("Invalid options")
        print ("Done!                                                                         ")
        widget.set_sensitive(True)
