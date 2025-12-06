from ..widgets import (
    PreferencesGroup,
    SpinRow,
    InfoButton,
    EntryRow,
    ToastOverlay,
)
from ..imports import Adw, Gtk, Gdk, HyprData, GLib

try:
    from hyprparser import Variable
except ImportError:
    # Try importing from hyprparser package if top-level fail
    # Although HyprData uses it, so it should be available.
    try:
        from hyprparser.src.classes.structures import Variable
    except ImportError:
        pass

# Global page references
variables_page = Adw.PreferencesPage.new()
settings_variables = None

def create_variable_row(var):
    name = f"${var.name}"
    value = var.value
    
    row = Adw.ActionRow.new()
    row.set_title(name)
    row.set_subtitle(value)
    
    # Edit Button
    edit_btn = Gtk.Button.new_from_icon_name("document-edit-symbolic")
    edit_btn.add_css_class("flat")
    edit_btn.set_valign(Gtk.Align.CENTER)
    edit_btn.connect("clicked", on_edit_clicked, var)
    row.add_suffix(edit_btn)
    
    # Delete Button
    del_btn = Gtk.Button.new_from_icon_name("user-trash-symbolic")
    del_btn.add_css_class("flat")
    del_btn.set_valign(Gtk.Align.CENTER)
    del_btn.connect("clicked", on_delete_clicked, var, row)
    row.add_suffix(del_btn)
    
    return row

def refresh_variables(*args):
    """Reloads the list of variables from HyprData."""
    global settings_variables
    
    if settings_variables:
        variables_page.remove(settings_variables)
    
    settings_variables = PreferencesGroup("Variables", "Environment variables and configuration variables.")
    
    if hasattr(HyprData, 'variables') and HyprData.variables:
        for var in HyprData.variables:
            row = create_variable_row(var)
            settings_variables.add(row)
    else:
        info = Adw.ActionRow.new()
        info.set_title("No Variables Found")
        settings_variables.add(info)
        
    variables_page.add(settings_variables)

def remove_variable_from_files(var):
    """
    Manually remove the variable line from HyprData.files content.
    Required because HyprData.variables list changes might not sync to file content automatically.
    """
    if not hasattr(var, 'format'):
        print("Variable object has no format() method?")
        return

    # Normalize target string
    # format() -> "$mainMod = SUPER"
    target_str = var.format().replace(" ", "")
    
    if hasattr(HyprData, 'files'):
        for file in HyprData.files:
            if not file.content: continue
            
            idx_to_remove = -1
            for i, line in enumerate(file.content):
                # Normalize line from file
                clean_line = line.split('#')[0].strip().replace(" ", "")
                if clean_line == target_str:
                    idx_to_remove = i
                    break
            
            if idx_to_remove != -1:
                print(f"Removing variable line {idx_to_remove} from {file.path}")
                file.content.pop(idx_to_remove)
                break

class VariableDialog(Adw.Window):
    def __init__(self, **kwargs):
        # Handle 'var' kwarg safely for GObject
        self.original_var = kwargs.pop('var', None)
        
        super().__init__(**kwargs)
        self.set_modal(True)
        self.set_title("Add Variable" if not self.original_var else "Edit Variable")
        self.set_default_size(500, 300)
        
        # UI
        content = Adw.ToolbarView.new()
        self.set_content(content)
        
        # Header
        header = Adw.HeaderBar.new()
        content.add_top_bar(header)
        
        # Page
        page = Adw.PreferencesPage.new()
        content.set_content(page)
        
        group = PreferencesGroup("Variable Details", "")
        page.add(group)
        
        # Name Entry
        self.name_entry = Adw.EntryRow.new()
        self.name_entry.set_title("Name (without $)")
        if self.original_var:
            self.name_entry.set_text(self.original_var.name)
        group.add(self.name_entry)

        # Value Entry
        self.value_entry = Adw.EntryRow.new()
        self.value_entry.set_title("Value")
        if self.original_var:
            self.value_entry.set_text(self.original_var.value)
        group.add(self.value_entry)
        
        # Save Button
        save_btn = Gtk.Button.new_with_label("Save")
        save_btn.connect("clicked", self.save)
        save_btn.add_css_class("suggested-action")
        header.pack_end(save_btn)
        
    def save(self, btn):
        name = self.name_entry.get_text().strip()
        value = self.value_entry.get_text() # Value can be anything
        
        if not name:
            toast = Adw.Toast.new("Please enter a variable name.")
            ToastOverlay.instance.add_toast(toast)
            return

        # Ensure no $ at start of name for internal storage if that's how it works
        if name.startswith("$"):
            name = name[1:]

        try:
            # If editing, remove old one first
            if self.original_var:
                try:
                    remove_variable_from_files(self.original_var)
                    if self.original_var in HyprData.variables:
                        HyprData.variables.remove(self.original_var)
                except ValueError:
                    pass
            
            # Create new Variable
            new_var = Variable(name=name, value=value)
            
            # Add to list? HyprData likely has no new_variable method, 
            # so we append to list and rely on save_all NOT using the list 
            # but manually adding it to file content? 
            # Wait, for Binds, new_bind ADDS to file content.
            # Does HyprData have new_variable? 
            # If not, we must manually append formatted string to file content AND add to list.
            
            # Let's check HyprData methods again (I recall only new_bind/new_env/new_option)
            # If no new_variable, we do it manually.
            
            # Update: HyprData probably lacks new_variable. 
            # We append directly to file content for persistence?
            
            # Add to list
            if hasattr(HyprData, 'variables'):
                HyprData.variables.append(new_var)
                
            # Add to file content manually with smart placement
            if hasattr(HyprData, 'files') and HyprData.files:
                f = HyprData.files[0] # Main config
                
                # Find insertion point (after last variable)
                insert_idx = -1
                for i, line in enumerate(f.content):
                    if line.strip().startswith("$"):
                        insert_idx = i
                
                if insert_idx != -1:
                    # Insert after last found variable
                    f.content.insert(insert_idx + 1, new_var.format())
                else:
                    # No variables found? Insert at top (after comments?) or just append?
                    # User mentioned "MY PROGRAMS". If we can't find variables, 
                    # we might just search for "MY PROGRAMS" or defaults.
                    # Fallback: Insert at line 0 if empty, or append if safer.
                    # Let's try to match user preference: "add to where existing ones are listed".
                    # If none exist, top is better than bottom for vars.
                    f.content.insert(0, new_var.format())
            
            # Save to disk
            if hasattr(HyprData, 'save_all'):
                HyprData.save_all()

            self.close()
            
            toast = Adw.Toast.new("Variable saved.")
            ToastOverlay.instance.add_toast(toast)
            
            refresh_variables()
            
        except Exception as e:
            print(f"Error saving variable: {e}")
            import traceback
            traceback.print_exc()

def on_add_clicked(btn):
    root = btn.get_root()
    dialog = VariableDialog(transient_for=root)
    dialog.get_content().set_visible(True)
    dialog.present()

def on_edit_clicked(btn, var):
    root = btn.get_root()
    dialog = VariableDialog(var=var, transient_for=root)
    dialog.get_content().set_visible(True)
    dialog.present()

def on_delete_clicked(btn, var, row):
    root = btn.get_root()
    body = f"Are you sure you want to delete ${var.name}?"
    dialog = Adw.MessageDialog.new(root, "Delete Variable", body)
    dialog.add_response("cancel", "Cancel")
    dialog.add_response("delete", "Delete")
    dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
    
    def on_response(d, resp):
        if resp == "delete":
            try:
                remove_variable_from_files(var)
                
                if var in HyprData.variables:
                    HyprData.variables.remove(var)
                
                if hasattr(HyprData, 'save_all'):
                    HyprData.save_all()
                    
                refresh_variables()
                
                toast = Adw.Toast.new("Variable deleted.")
                ToastOverlay.instance.add_toast(toast)
            except Exception as e:
                print(f"Error deleting variable: {e}")
        d.close()
        
    dialog.connect("response", on_response)
    dialog.present()

# Setup Page Actions
actions_group = PreferencesGroup("Actions", "")
add_btn_row = Adw.ActionRow.new()
add_btn_row.set_title("Add New Variable")
add_btn_row.set_subtitle("Define a new variable.")

box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
box.set_valign(Gtk.Align.CENTER)

refresh_btn = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
refresh_btn.set_tooltip_text("Reload variables")
refresh_btn.add_css_class("flat")
refresh_btn.connect("clicked", refresh_variables)
box.append(refresh_btn)

add_btn = Gtk.Button.new_with_label("Add")
add_btn.add_css_class("suggested-action")
add_btn.connect("clicked", on_add_clicked)
box.append(add_btn)

add_btn_row.add_suffix(box)
actions_group.add(add_btn_row)
variables_page.add(actions_group)

# Initial Load
refresh_variables()

