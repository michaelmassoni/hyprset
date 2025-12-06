from ..widgets import (
    PreferencesGroup,
    InfoButton,
    EntryRow,
    ToastOverlay,
)
from ..imports import Adw, Gtk, Gdk, HyprData, GLib

try:
    from hyprparser import Binding
except ImportError:
    pass

# ... imports ...

try:
    from hyprparser import Binding
except ImportError:
    pass

# Global page references
binds_page = Adw.PreferencesPage.new()
settings_binds = None

def create_bind_row(bind):
    mods = " + ".join(bind.mods) if bind.mods else ""
    key = bind.key
    title = f"{mods} + {key}" if mods else key
    
    params = " ".join(bind.params) if bind.params else ""
    # Safe escape
    params = GLib.markup_escape_text(params)
    subtitle = f"{bind.dispatcher} {params}"
    
    row = Adw.ActionRow.new()
    row.set_title(title)
    row.set_subtitle(subtitle)
    
    # Edit Button
    edit_btn = Gtk.Button.new_from_icon_name("document-edit-symbolic")
    edit_btn.add_css_class("flat")
    edit_btn.set_valign(Gtk.Align.CENTER)
    edit_btn.connect("clicked", on_edit_clicked, bind)
    row.add_suffix(edit_btn)
    
    # Delete Button
    del_btn = Gtk.Button.new_from_icon_name("user-trash-symbolic")
    del_btn.add_css_class("flat")
    del_btn.set_valign(Gtk.Align.CENTER)
    del_btn.connect("clicked", on_delete_clicked, bind, row)
    row.add_suffix(del_btn)
    
    return row

def refresh_binds(*args):
    """Reloads the list of keybindings from HyprData."""
    global settings_binds
    
    if settings_binds:
        binds_page.remove(settings_binds)
    
    settings_binds = PreferencesGroup("Keybindings", "Configure keyboard and mouse bindings.")
    
    if hasattr(HyprData, 'binds') and HyprData.binds:
        for bind in HyprData.binds:
            row = create_bind_row(bind)
            settings_binds.add(row)
    else:
        info = Adw.ActionRow.new()
        info.set_title("No Keybindings Found")
        settings_binds.add(info)
        
    binds_page.add(settings_binds)

class KeybindDialog(Adw.Window):
    def __init__(self, **kwargs):
        # Extract bind from kwargs manually to appease GObject
        self.original_bind = kwargs.pop('bind', None)
        
        super().__init__(**kwargs)
        self.set_modal(True)
        self.set_title("Add Keybinding" if not self.original_bind else "Edit Keybinding")
        self.set_default_size(600, 550)
        
        bind = self.original_bind
        self.mods = bind.mods.copy() if bind else []
        self.key = bind.key if bind else ""
        self.recording = False
        
        # UI
        content = Adw.ToolbarView.new()
        self.set_content(content)
        
        # Header
        header = Adw.HeaderBar.new()
        content.add_top_bar(header)
        
        # Page
        page = Adw.PreferencesPage.new()
        content.set_content(page)
        
        group = PreferencesGroup("Configuration", "")
        page.add(group)
        
        # Recorder Row
        self.record_row = Adw.ActionRow.new()
        self.record_row.set_title("Key Combination")
        self.record_row.set_subtitle("Click 'Record' and press keys")
        
        self.record_btn = Gtk.Button.new_with_label("Record")
        self.record_btn.connect("clicked", self.toggle_recording)
        self.record_btn.add_css_class("suggested-action")
        self.record_btn.set_valign(Gtk.Align.CENTER)
        
        self.record_row.add_suffix(self.record_btn)
        group.add(self.record_row)
        
        # Manual Input Expander
        manual_expander = Adw.ExpanderRow.new()
        manual_expander.set_title("Manual Input")
        manual_expander.set_subtitle("Manually select modifiers and key to avoid host conflicts.")
        group.add(manual_expander)
        
        # Modifiers
        self.check_super = Gtk.CheckButton.new_with_label("Super")
        self.check_ctrl = Gtk.CheckButton.new_with_label("Ctrl")
        self.check_alt = Gtk.CheckButton.new_with_label("Alt")
        self.check_shift = Gtk.CheckButton.new_with_label("Shift")
        
        for check in [self.check_super, self.check_ctrl, self.check_alt, self.check_shift]:
             check.connect("toggled", self.on_manual_change)
             
             # Wrap in ActionRow for niceness
             row = Adw.ActionRow.new()
             row.set_title(check.get_label())
             row.add_suffix(check)
             manual_expander.add_row(row)

        # Check for $mainMod variable
        self.check_main_mod = None
        has_main_mod = False
        if hasattr(HyprData, 'variables'):
            for v in HyprData.variables:
                # Variable names usually stored without $
                if v.name == "mainMod":
                     has_main_mod = True
                     break
        
        if has_main_mod:
             self.check_main_mod = Gtk.CheckButton.new_with_label("$mainMod")
             self.check_main_mod.connect("toggled", self.on_manual_change)
             
             row = Adw.ActionRow.new()
             row.set_title("$mainMod")
             row.set_subtitle("Use variable (usually replaces SUPER/ALT)")
             row.add_suffix(self.check_main_mod)
             manual_expander.add_row(row)

        # Key Entry
        self.key_entry = Adw.EntryRow.new()
        self.key_entry.set_title("Key")
        self.key_entry.connect("changed", self.on_manual_change)
        manual_expander.add_row(self.key_entry)

        # Command Entry
        self.dispatcher_entry = Adw.EntryRow.new()
        self.dispatcher_entry.set_title("Dispatcher")
        self.dispatcher_entry.set_text(bind.dispatcher if bind else "exec")
        group.add(self.dispatcher_entry)
        
        self.command_entry = Adw.EntryRow.new()
        self.command_entry.set_title("Command / Args")
        self.command_entry.set_text(" ".join(bind.params) if bind and bind.params else "")
        group.add(self.command_entry)
        
        # Save Button
        save_btn = Gtk.Button.new_with_label("Save")
        save_btn.connect("clicked", self.save)
        save_btn.add_css_class("suggested-action")
        header.pack_end(save_btn)
        
        # Key Controller
        self.key_controller = Gtk.EventControllerKey.new()
        self.key_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        self.key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(self.key_controller)
        
        # Initialize UI if editing
        if bind:
            self.update_ui_from_data()
            self.update_label()

    def toggle_recording(self, btn):
        self.recording = not self.recording
        if self.recording:
            self.record_btn.set_label("Stop Recording")
            self.record_btn.add_css_class("destructive-action")
            self.record_btn.remove_css_class("suggested-action")
            self.record_row.set_subtitle("Press any key combination...")
            self.record_btn.grab_focus()
        else:
            self.record_btn.set_label("Record")
            self.record_btn.remove_css_class("destructive-action")
            self.record_btn.add_css_class("suggested-action")
            self.update_label()
            
    def on_key_pressed(self, controller, keyval, keycode, state):
        if not self.recording:
            return False
            
        # Ignore modifier-only presses for finalization, but track them blocks?
        # Hyprset logic: we just capture everything if recording.
        
        # Convert state to mods
        mods = []
        if state & Gdk.ModifierType.SUPER_MASK: mods.append("SUPER")
        if state & Gdk.ModifierType.CONTROL_MASK: mods.append("CTRL")
        if state & Gdk.ModifierType.ALT_MASK: mods.append("ALT")
        if state & Gdk.ModifierType.SHIFT_MASK: mods.append("SHIFT")
        
        # Get key name
        key_name = Gdk.keyval_name(keyval)
        
        # Filter out if key IS a modifier
        if key_name in ["Super_L", "Super_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"]:
            return True # Consume but don't set
            
        self.mods = mods
        self.key = key_name
        self.update_ui_from_data()
        self.update_label()
        
        # Stop recording after key press?
        # Usually yes for single bind
        self.toggle_recording(self.record_btn)
        return True

    def on_manual_change(self, *args):
        # Update internal state from manual widgets
        mods = []
        if self.check_super.get_active(): mods.append("SUPER")
        if self.check_ctrl.get_active(): mods.append("CTRL")
        if self.check_alt.get_active(): mods.append("ALT")
        if self.check_shift.get_active(): mods.append("SHIFT")
        
        if self.check_main_mod and self.check_main_mod.get_active():
            mods.append("$mainMod")
        
        self.mods = mods
        self.key = self.key_entry.get_text()
        self.update_label()

    def update_ui_from_data(self):
        # Update switches and entry from internal state
        self.check_super.set_active("SUPER" in self.mods)
        self.check_ctrl.set_active("CTRL" in self.mods)
        self.check_alt.set_active("ALT" in self.mods)
        self.check_shift.set_active("SHIFT" in self.mods)
        
        if self.check_main_mod:
            self.check_main_mod.set_active("$mainMod" in self.mods)
            
        self.key_entry.set_text(self.key)

    def update_label(self):
        mods_str = " + ".join(self.mods)
        txt = f"{mods_str} + {self.key}" if mods_str else self.key
        if not txt: txt = "Click 'Record'..."
        self.record_row.set_subtitle(txt)

    def save(self, btn):
        dispatcher = self.dispatcher_entry.get_text()
        params = self.command_entry.get_text()
        
        if not self.key:
            toast = Adw.Toast.new("Please define a key.")
            ToastOverlay.instance.add_toast(toast)
            return

        # Check for conflicts
        # ... logic ...
        self.commit_save(dispatcher, params)

    def commit_save(self, dispatcher, params):
        try:
            # If editing, remove old one first
            if self.original_bind:
                try:
                    remove_bind_from_files(self.original_bind)
                    if self.original_bind in HyprData.binds:
                        HyprData.binds.remove(self.original_bind)
                except ValueError:
                    print("Could not find original bind to remove in memory.")
            
            new_bind = Binding(
                mods=self.mods,
                key=self.key,
                dispatcher=dispatcher,
                params=params.split(),
                bindtype='bind' 
            )
            HyprData.new_bind(new_bind)
            
            # Save to disk
            if hasattr(HyprData, 'save_all'):
                HyprData.save_all()

            self.close()
            
            toast = Adw.Toast.new("Keybinding saved. Restart/Reload needed to confirm.")
            ToastOverlay.instance.add_toast(toast)
            
            # Refresh List
            refresh_binds()
            
        except Exception as e:
            print(f"Error saving bind: {e}")
            import traceback
            traceback.print_exc()

def on_add_clicked(btn):
    root = btn.get_root()
    dialog = KeybindDialog(transient_for=root)
    # Ensure content is visible
    dialog.get_content().set_visible(True)
    dialog.present()

def on_edit_clicked(btn, bind):
    root = btn.get_root()
    dialog = KeybindDialog(bind=bind, transient_for=root)
    # Ensure content is visible
    dialog.get_content().set_visible(True)
    dialog.present()
    
def remove_bind_from_files(bind):
    """
    Manually remove the bind line from HyprData.files content.
    This is required because HyprData.binds.remove() does not update the file content list.
    """
    if not hasattr(bind, 'format'):
        print("Bind object has no format() method via hyprparser?")
        # Fallback? construct manually?
        # Assuming verify_hyprparser_behavior confirmed format exists.
        return

    # Normalize target string for comparison (ignore spaces around commas/equals)
    # format() -> "bind = SUPER, W, exec, firefox"
    target_str = bind.format().replace(" ", "")
    
    deleted = False
    
    if hasattr(HyprData, 'files'):
        for file in HyprData.files:
            if not file.content: continue
            
            idx_to_remove = -1
            for i, line in enumerate(file.content):
                # Normalize line from file
                # Remove comments?
                clean_line = line.split('#')[0].strip().replace(" ", "")
                if clean_line == target_str:
                    idx_to_remove = i
                    break
            
            if idx_to_remove != -1:
                print(f"Removing line {idx_to_remove} from {file.path}: {file.content[idx_to_remove]}")
                file.content.pop(idx_to_remove)
                deleted = True
                break # Remove only first occurrence? Safer.

def on_delete_clicked(btn, bind, row):
    root = btn.get_root()
    body = f"Are you sure you want to delete this keybinding?"
    dialog = Adw.MessageDialog.new(root, "Delete Keybinding", body)
    dialog.add_response("cancel", "Cancel")
    dialog.add_response("delete", "Delete")
    dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
    
    def on_response(d, resp):
        if resp == "delete":
            try:
                # Remove from file content first
                remove_bind_from_files(bind)
                
                # Remove from memory list
                if bind in HyprData.binds:
                    HyprData.binds.remove(bind)
                
                # Save to disk
                if hasattr(HyprData, 'save_all'):
                    HyprData.save_all()
                    
                refresh_binds()
                
                toast = Adw.Toast.new("Keybinding deleted.")
                ToastOverlay.instance.add_toast(toast)
            except Exception as e:
                print(f"Error deleting: {e}")
                import traceback
                traceback.print_exc()
        d.close()
        
    dialog.connect("response", on_response)
    dialog.present()

# Defaults
DEFAULT_KEYBINDINGS = [
    {"mods": ["$mainMod"], "key": "Q", "dispatcher": "exec", "params": ["$terminal"]},
    {"mods": ["$mainMod"], "key": "C", "dispatcher": "killactive", "params": []},
    {"mods": ["$mainMod"], "key": "M", "dispatcher": "exit", "params": []},
    {"mods": ["$mainMod"], "key": "E", "dispatcher": "exec", "params": ["$fileManager"]},
    {"mods": ["$mainMod"], "key": "V", "dispatcher": "togglefloating", "params": []},
    {"mods": ["$mainMod"], "key": "R", "dispatcher": "exec", "params": ["$menu"]},
    {"mods": ["$mainMod"], "key": "P", "dispatcher": "pseudo", "params": []},
    {"mods": ["$mainMod"], "key": "J", "dispatcher": "togglesplit", "params": []},
    {"mods": ["$mainMod"], "key": "left", "dispatcher": "movefocus", "params": ["l"]},
    {"mods": ["$mainMod"], "key": "right", "dispatcher": "movefocus", "params": ["r"]},
    {"mods": ["$mainMod"], "key": "up", "dispatcher": "movefocus", "params": ["u"]},
    {"mods": ["$mainMod"], "key": "down", "dispatcher": "movefocus", "params": ["d"]},
]
# Add workspaces 1-10
for i in range(1, 11):
    k = str(i % 10)
    DEFAULT_KEYBINDINGS.append({"mods": ["$mainMod"], "key": k, "dispatcher": "workspace", "params": [str(i)]})
    DEFAULT_KEYBINDINGS.append({"mods": ["$mainMod", "SHIFT"], "key": k, "dispatcher": "movetoworkspace", "params": [str(i)]})

# Add mouse
DEFAULT_KEYBINDINGS.append({"mods": ["$mainMod"], "key": "mouse:272", "dispatcher": "movewindow", "params": []})
DEFAULT_KEYBINDINGS.append({"mods": ["$mainMod"], "key": "mouse:273", "dispatcher": "resizewindow", "params": []})

def on_reset_clicked(btn):
    root = btn.get_root()
    body = "Are you sure? This will delete ALL custom keybindings and restore defaults."
    dialog = Adw.MessageDialog.new(root, "Reset Keybindings", body)
    dialog.add_response("cancel", "Cancel")
    dialog.add_response("reset", "Reset")
    dialog.set_response_appearance("reset", Adw.ResponseAppearance.DESTRUCTIVE)
    
    def on_response(d, resp):
        if resp == "reset":
            try:
                # 1. Clear Existing
                current_binds = list(HyprData.binds) if hasattr(HyprData, 'binds') and HyprData.binds else []
                for bind in current_binds:
                    remove_bind_from_files(bind) # Remove from file content
                    if bind in HyprData.binds:
                        HyprData.binds.remove(bind)
                
                # 2. Add Defaults
                for item in DEFAULT_KEYBINDINGS:
                    # Determine bind type
                    btype = 'bindm' if 'mouse' in item['key'] else 'bind'
                    
                    new_bind = Binding(
                        mods=item['mods'],
                        key=item['key'],
                        dispatcher=item['dispatcher'],
                        params=item['params'],
                        bindtype=btype 
                    )
                    HyprData.new_bind(new_bind)

                # 3. Save
                if hasattr(HyprData, 'save_all'):
                    HyprData.save_all()
                
                refresh_binds()
                
                toast = Adw.Toast.new("Keybindings reset to default.")
                ToastOverlay.instance.add_toast(toast)
                
            except Exception as e:
                print(f"Error resetting: {e}")
                import traceback
                traceback.print_exc()
        d.close()
        
    dialog.connect("response", on_response)
    dialog.present()


# Setup Page
actions_group = PreferencesGroup("Actions", "")
add_btn_row = Adw.ActionRow.new()
add_btn_row.set_title("Add New Keybinding")
add_btn_row.set_subtitle("Record a new keybinding.")

# Container for buttons
box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
box.set_valign(Gtk.Align.CENTER)

# Refresh Button
refresh_btn = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
refresh_btn.set_tooltip_text("Reload keybindings")
refresh_btn.add_css_class("flat")
refresh_btn.connect("clicked", refresh_binds)
box.append(refresh_btn)

# Add Button
add_btn = Gtk.Button.new_with_label("Add")
add_btn.add_css_class("suggested-action")
add_btn.connect("clicked", on_add_clicked)
box.append(add_btn)

add_btn_row.add_suffix(box)
actions_group.add(add_btn_row)

# Reset Row
reset_btn_row = Adw.ActionRow.new()
reset_btn_row.set_title("Reset Keybindings")
reset_btn_row.set_subtitle("Restore default Hyprland keybindings.")

reset_btn = Gtk.Button.new_with_label("Reset")
reset_btn.add_css_class("destructive-action")
reset_btn.set_valign(Gtk.Align.CENTER)
reset_btn.connect("clicked", on_reset_clicked)

reset_btn_row.add_suffix(reset_btn)
actions_group.add(reset_btn_row)


binds_page.add(actions_group)

# Initial Load
refresh_binds()
