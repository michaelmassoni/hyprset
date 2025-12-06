from ..imports import Adw, Gtk, HyprData, Setting
from .CustomToastOverlay import ToastOverlay
import sys

class _ComboRow:
    def __init__(self, title, subtitle, section, items):
        self._instance = Adw.ComboRow()
        self.instance.set_title(title)
        self.instance.set_subtitle(subtitle)
        
        # Prepare items list (Label, Value)
        self.item_pairs = []
        display_items = []
        
        for item in items:
            if isinstance(item, (tuple, list)) and len(item) == 2:
                self.item_pairs.append((str(item[0]), str(item[1])))
                display_items.append(str(item[0]))
            else:
                self.item_pairs.append((str(item), str(item)))
                display_items.append(str(item))
        
        # Populate model
        model = Gtk.StringList.new(display_items)
        self.instance.set_model(model)
        self.section = section
        
        ToastOverlay.instances.append(self)

        # Initialize Value
        current_val = None
        if self.section is not None:
            try:
                opt = HyprData.get_option(self.section)
                if not opt:
                   # Fallback creates Setting locally but doesn't call new_option to avoid recursion hang
                   default_val = self.item_pairs[0][1] if self.item_pairs else ""
                   opt = Setting(self.section, default_val)
                   
                if opt and hasattr(opt, 'value'):
                    current_val = str(opt.value)
            except Exception as e:
                print(f"Warning: Could not load setting {section}: {e}", file=sys.stderr)
        
        # Find index based on VALUE
        selected_idx = 0
        if current_val is not None:
            for i, (label, value) in enumerate(self.item_pairs):
                if value == current_val:
                    selected_idx = i
                    break
            
        self.instance.set_selected(selected_idx)
        self._default = selected_idx

        self.instance.connect("notify::selected", self.on_selected)

    def on_selected(self, *_):
        if self.instance.get_selected() != self._default:
            ToastOverlay.add_change()
        else:
            ToastOverlay.del_change()

        if self.section is None:
            return

        # Get VALUE from pairs
        selected_idx = self.instance.get_selected()
        if 0 <= selected_idx < len(self.item_pairs):
            selected_val = self.item_pairs[selected_idx][1]
            return HyprData.set_option(self.section, selected_val)
        
        return None

    @property
    def instance(self):
        return self._instance
    
    def update_default(self):
        self._default = self.instance.get_selected()

def ComboRow(title, subtitle, section, items):
    return _ComboRow(title, subtitle, section, items).instance
