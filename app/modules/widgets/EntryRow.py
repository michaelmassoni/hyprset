from ..imports import Gtk, Adw, HyprData, Setting
from .CustomToastOverlay import ToastOverlay
import sys

def EntryRow(title: str, subtitle: str, section: str):
    row = Adw.ActionRow()
    row.set_title(title)
    row.set_subtitle(subtitle)
    
    entry = Gtk.Entry()
    entry.set_valign(Gtk.Align.CENTER)
    entry.set_hexpand(True) # Maybe?
    
    # Styling to look nice
    # entry.add_css_class("flat") # Optional
    
    row.add_suffix(entry)
    
    # Load value
    try:
        opt = HyprData.get_option(section)
        if not opt:
            opt = Setting(section, "")
            try:
                HyprData.new_option(opt)
            except RecursionError:
                pass
        
        if opt.value:
            entry.set_text(str(opt.value))
            
        entry._default = (entry.get_text(), False)
    except Exception as e:
        print(f"Warning loading {section}: {e}", file=sys.stderr)
        entry._default = ("", False)
        
    def on_changed(widget):
        text = widget.get_text()
        if entry._default[0] != text:
             if not entry._default[1]:
                 ToastOverlay.add_change()
                 entry._default = (entry._default[0], True)
        else:
             ToastOverlay.del_change()
             entry._default = (entry._default[0], False)
             
        HyprData.set_option(section, text)
        
    entry.connect("changed", on_changed)
    
    return row
