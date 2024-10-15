#!/usr/bin/env python3
#Name: desktop-session-exit.py
#Dir: /usr/local/lib/desktop-session/
#Version: 2.0
#Depends: python, Gtk
#Author: Dave (david@daveserver.info)
#Purpose: GUI for desktop-session-exit script
#License: gplv3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib, Gio, GdkPixbuf
import gettext
import os
import sys
#Variables
ButtonWidth = 240
ButtonHeight = 80

# More robust icon path handling
try:
    ICONS = os.path.expanduser("~/.local/share/icons/hicolor/48x48/apps") #Fallback to a common location
    if not os.path.exists(ICONS):
        ICONS = "/usr/share/icons/hicolor/48x48/apps" #Fallback to a system location
except Exception as e:
    print(f"Error determining icon path: {e}")
    ICONS = "" #Set to empty string if path cannot be determined


gettext.install(domain = "desktop-session-exit", codeset   = 'utf-8')

class mainWindow(Gtk.Window):
    def button_clicked(self, widget, command):
        try:
            os.system(command)
            sys.exit()
        except Exception as e:
            print(f"Error executing command: {e}")
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, f"Error: {e}")
            dialog.run()
            dialog.destroy()

    def build_button(self,image,text,command,column,row):
        button = Gtk.Button.new_with_mnemonic("_"+_(text))
        try:
            button_image = Gtk.Image.new_from_file(image)
            button.set_image(button_image)
            button.set_image_position(Gtk.PositionType.TOP)
            button.set_always_show_image(True)
        except Exception as e:
            print(f"Error loading image {image}: {e}")

        button.connect("clicked", self.button_clicked, command)
        button.set_hexpand(True)
        button.set_vexpand(True)
        button.set_size_request(ButtonWidth, ButtonHeight)
        button.show()
        
        self.grid.attach(button, column, row, 1, 1)

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_size_request(400,100)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_title(_("Exit Session"))
        self.show()
        
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.show()
        
        #Build Buttons: ICON, NAME, ACTION, COLUMN, ROW
        self.build_button(ICONS+"/lock.png","Lock Screen","desktop-session-exit -L",1,1)
        self.build_button(ICONS+"/restart.png","Restart Session","desktop-session-exit -R",1,2) 
        self.build_button(ICONS+"/reboot.png","Reboot","desktop-session-exit -r",1,3)
        self.build_button(ICONS+"/logout.png","Log Out","desktop-session-exit -l",2,1)
        self.build_button(ICONS+"/suspend.png","Suspend","desktop-session-exit -S",2,2)
        self.build_button(ICONS+"/shutdown.png","Shutdown","desktop-session-exit -s",2,3)
        
win = mainWindow()
win.connect("delete-event", Gtk.main_quit)
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL) 
Gtk.main()
