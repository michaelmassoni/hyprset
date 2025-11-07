#!/usr/bin/env python3
"""Simple test to verify GTK window can appear"""
import sys
import os
os.environ['G_MESSAGES_DEBUG'] = ''
os.environ['GTK_DEBUG'] = ''

import gi
gi.require_versions({"Adw": "1", "Gtk": "4.0"})
from gi.repository import Adw, Gtk

def on_activate(app):
    win = Adw.ApplicationWindow(application=app)
    win.set_title("Test Window")
    win.set_default_size(400, 300)
    
    label = Gtk.Label(label="If you see this, GTK windows work!")
    win.set_content(label)
    win.present()

app = Adw.Application(application_id="com.test.window")
app.connect("activate", on_activate)
app.run(None)

