from ..widgets import (
    PreferencesGroup,
    SwitchRow,
    SpinRow,
    EntryRow,
    ComboRow,
)
from ..imports import Adw
import sys
import os

# Parse XKB Rules
kb_layouts = []
kb_variants = []

def parse_xkb_rules():
    layout_file = "/usr/share/X11/xkb/rules/evdev.lst"
    if not os.path.exists(layout_file):
        return
    
    try:
        current_section = None
        with open(layout_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('! '):
                    section_name = line[2:].strip()
                    if section_name == 'layout':
                        current_section = 'layout'
                    elif section_name == 'variant':
                        current_section = 'variant'
                    else:
                        current_section = None
                    continue
                
                if current_section == 'layout':
                    # Format: code    description
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2:
                        code, desc = parts
                        # Display: Description (code)
                        label = f"{desc} ({code})"
                        kb_layouts.append((label, code))
                        
                elif current_section == 'variant':
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2:
                        code, desc = parts
                        label = f"{desc} ({code})"
                        kb_variants.append((label, code))
                        
    except Exception as e:
        print(f"Error parsing XKB rules: {e}", file=sys.stderr)

parse_xkb_rules()

# Sort lists
kb_layouts.sort(key=lambda x: x[0])
kb_variants.sort(key=lambda x: x[0])
# Add "default" or empty option?
kb_layouts.insert(0, ("Default / Empty", ""))
kb_variants.insert(0, ("Default / Empty", ""))


input_page = Adw.PreferencesPage.new()

# Keyboard
settings_keyboard = PreferencesGroup("Keyboard", "Keyboard input settings.")

settings_keyboard_kb_layout = ComboRow(
    "Keyboard Layout",
    "Keyboard layout. Use 'hyprctl switchxkblayout' to switch.",
    "input:kb_layout",
    items=kb_layouts
)

settings_keyboard_kb_variant = ComboRow(
    "Keyboard Variant",
    "Keyboard variant.",
    "input:kb_variant",
    items=kb_variants
)

settings_keyboard_kb_options = EntryRow(
    "Keyboard Options",
    "Comma-separated list of keyboard options.",
    "input:kb_options",
)

settings_keyboard_kb_rules = EntryRow(
    "Keyboard Rules",
    "Keyboard rules.",
    "input:kb_rules",
)

settings_keyboard_kb_model = EntryRow(
    "Keyboard Model",
    "Keyboard model.",
    "input:kb_model",
)

settings_keyboard_follow_mouse = SwitchRow(
    "Follow Mouse",
    "Whether the cursor should follow the focus.",
    "input:follow_mouse",
)

settings_keyboard_mouse_refocus = SwitchRow(
    "Mouse Refocus",
    "Refocus the window under the cursor when it changes.",
    "input:mouse_refocus",
)

settings_keyboard_float_switch_override_focus = SwitchRow(
    "Float Switch Override Focus",
    "When on a floating window, focus the window under the cursor.",
    "input:float_switch_override_focus",
)

settings_keyboard_repeat_rate = SpinRow(
    "Repeat Rate",
    "Key repeat rate.",
    "input:repeat_rate",
    max=200,
)

settings_keyboard_repeat_delay = SpinRow(
    "Repeat Delay",
    "Delay before repeat.",
    "input:repeat_delay",
    max=2000,
)

settings_keyboard_numlock_by_default = SwitchRow(
    "Numlock by Default",
    "Enable numlock on startup.",
    "input:numlock_by_default",
)

# Mouse
settings_mouse = PreferencesGroup("Mouse", "Mouse input settings.")

settings_mouse_sensitivity = SpinRow(
    "Sensitivity",
    "Mouse sensitivity. Negative values are also allowed.",
    "input:sensitivity",
    data_type=float,
    min=-10.0,
    max=10.0,
    decimal_digits=2,
)

settings_mouse_accel_profile = SpinRow(
    "Accel Profile",
    "Mouse acceleration profile. Options: flat, adaptive.",
    "input:accel_profile",
    max=100,
)

settings_mouse_force_no_accel = SwitchRow(
    "Force No Accel",
    "Force no mouse acceleration.",
    "input:force_no_accel",
)

# Touchpad
settings_touchpad = PreferencesGroup("Touchpad", "Touchpad input settings.")

settings_touchpad_touchpad_natural_scroll = SwitchRow(
    "Natural Scroll",
    "Enable natural scrolling for touchpads.",
    "input:touchpad:natural_scroll",
)

settings_touchpad_touchpad_disable_while_typing = SwitchRow(
    "Disable While Typing",
    "Disable touchpad while typing.",
    "input:touchpad:disable_while_typing",
)

settings_touchpad_touchpad_clickfinger_behavior = SwitchRow(
    "Clickfinger Behavior",
    "Enable clickfinger behavior.",
    "input:touchpad:clickfinger_behavior",
)

settings_touchpad_touchpad_middle_button_emulation = SwitchRow(
    "Middle Button Emulation",
    "Enable middle button emulation.",
    "input:touchpad:middle_button_emulation",
)

settings_touchpad_touchpad_tap_button_map = SpinRow(
    "Tap Button Map",
    "Tap button map. Options: lrm, lmr.",
    "input:touchpad:tap_button_map",
    max=10,
)

settings_touchpad_touchpad_tap_to_click = SwitchRow(
    "Tap to Click",
    "Enable tap to click.",
    "input:touchpad:tap_to_click",
)

settings_touchpad_touchpad_drag_lock = SwitchRow(
    "Drag Lock",
    "Enable drag lock.",
    "input:touchpad:drag_lock",
)

settings_touchpad_scroll_factor = SpinRow(
    "Scroll Factor",
    "Scroll speed factor.",
    "input:touchpad:scroll_factor",
    data_type=float,
    min=0.1,
    max=5.0,
    decimal_digits=2,
)

# Tablet
settings_tablet = PreferencesGroup("Tablet", "Tablet input settings.")

settings_tablet_tablet_transform = SpinRow(
    "Transform",
    "Tablet transform. Options: 0-7.",
    "input:tablet:transform",
    min=0,
    max=7,
)

settings_tablet_tablet_output = SpinRow(
    "Output",
    "Tablet output. Leave empty for auto.",
    "input:tablet:output",
    max=100,
)

# General Settings (Top Level)
settings_general = PreferencesGroup("General", "")

settings_show_advanced = SwitchRow(
    "Advanced Mode",
    "Show advanced input settings.",
    None, # Not persistent via config, local state
)

# Advanced Mode Logic
def on_advanced_toggled(switch, *args):
    active = switch.get_active()
    # Toggle visibility of advanced rows
    for row in advanced_rows:
        row.set_visible(active)

settings_show_advanced.connect("notify::active", on_advanced_toggled)
settings_general.add(settings_show_advanced)
input_page.add(settings_general)


# Gestures (Merged)
settings_gestures = PreferencesGroup("Gestures", "Touchpad and touchscreen gesture settings.")

settings_gestures_workspace_swipe = SwitchRow(
    "Workspace Swipe",
    "Enable workspace swipe gesture.",
    "gestures:workspace_swipe",
)

settings_gestures_workspace_swipe_fingers = SpinRow(
    "Workspace Swipe Fingers",
    "Number of fingers for workspace swipe.",
    "gestures:workspace_swipe_fingers",
    min=1,
    max=5,
)

settings_gestures_workspace_swipe_distance = SpinRow(
    "Workspace Swipe Distance",
    "Distance in pixels to swipe before switching workspace.",
    "gestures:workspace_swipe_distance",
    min=0,
    max=1000,
)

settings_gestures_workspace_swipe_invert = SwitchRow(
    "Workspace Swipe Invert",
    "Invert the direction of workspace swipe.",
    "gestures:workspace_swipe_invert",
)

settings_gestures_workspace_swipe_min_speed_to_force = SpinRow(
    "Min Speed to Force",
    "Minimum speed in pixels per second to force workspace switch.",
    "gestures:workspace_swipe_min_speed_to_force",
    min=0,
    max=10000,
)

settings_gestures_workspace_swipe_cancel_ratio = SpinRow(
    "Cancel Ratio",
    "Ratio of swipe distance to cancel workspace switch (0.0-1.0).",
    "gestures:workspace_swipe_cancel_ratio",
    data_type=float,
    min=0.0,
    max=1.0,
    decimal_digits=2,
)

settings_gestures_workspace_swipe_create_new = SwitchRow(
    "Create New Workspace",
    "Create new workspace when swiping past the last one.",
    "gestures:workspace_swipe_create_new",
)

settings_gestures_workspace_swipe_forever = SwitchRow(
    "Workspace Swipe Forever",
    "Allow swiping forever (wraps around).",
    "gestures:workspace_swipe_forever",
)

settings_gestures_workspace_swipe_use_r = SwitchRow(
    "Use R",
    "Use R key for workspace swipe.",
    "gestures:workspace_swipe_use_r",
)

# Add gesture settings
for i in [
    settings_gestures_workspace_swipe,
    settings_gestures_workspace_swipe_fingers,
    settings_gestures_workspace_swipe_distance,
    settings_gestures_workspace_swipe_invert,
    settings_gestures_workspace_swipe_min_speed_to_force,
    settings_gestures_workspace_swipe_cancel_ratio,
    settings_gestures_workspace_swipe_create_new,
    settings_gestures_workspace_swipe_forever,
    settings_gestures_workspace_swipe_use_r,
]:
    settings_gestures.add(i)


# Add keyboard settings
for i in [
    settings_keyboard_kb_layout,
    settings_keyboard_kb_variant,
    settings_keyboard_kb_options,
    settings_keyboard_kb_rules,
    settings_keyboard_kb_model,
    settings_keyboard_follow_mouse,
    settings_keyboard_mouse_refocus,
    settings_keyboard_float_switch_override_focus,
    settings_keyboard_repeat_rate,
    settings_keyboard_repeat_delay,
    settings_keyboard_numlock_by_default,
]:
    settings_keyboard.add(i)

# Add mouse settings
for i in [
    settings_mouse_sensitivity,
    settings_mouse_accel_profile,
    settings_mouse_force_no_accel,
]:
    settings_mouse.add(i)

# Add touchpad settings
for i in [
    settings_touchpad_touchpad_natural_scroll,
    settings_touchpad_touchpad_disable_while_typing,
    settings_touchpad_touchpad_clickfinger_behavior,
    settings_touchpad_touchpad_middle_button_emulation,
    settings_touchpad_touchpad_tap_button_map,
    settings_touchpad_touchpad_tap_to_click,
    settings_touchpad_touchpad_drag_lock,
    settings_touchpad_scroll_factor,
]:
    settings_touchpad.add(i)

# Add tablet settings
for i in [
    settings_tablet_tablet_transform,
    settings_tablet_tablet_output,
]:
    settings_tablet.add(i)

# Add sections
for i in [
    settings_gestures, # Added Gestures here
    settings_keyboard,
    settings_mouse,
    settings_touchpad,
    settings_tablet,
]:
    input_page.add(i)

# Define Advanced Rows
# Mark specific rows as advanced to hide them by default
advanced_rows = [
    settings_keyboard_kb_rules,
    settings_keyboard_kb_model,
    settings_keyboard_repeat_rate,
    settings_keyboard_repeat_delay,
    settings_gestures_workspace_swipe_min_speed_to_force,
    settings_gestures_workspace_swipe_cancel_ratio,
    settings_touchpad_touchpad_tap_button_map,
    settings_tablet_tablet_transform,
    settings_tablet_tablet_output,
]

# Initial Visibility State
on_advanced_toggled(settings_show_advanced)

