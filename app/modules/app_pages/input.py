from ..widgets import (
    PreferencesGroup,
    SwitchRow,
    SpinRow,
)
from ..imports import Adw


input_page = Adw.PreferencesPage.new()

# Keyboard
settings_keyboard = PreferencesGroup("Keyboard", "Keyboard input settings.")

settings_keyboard_kb_layout = SpinRow(
    "Keyboard Layout",
    "Keyboard layout. Use 'hyprctl switchxkblayout' to switch.",
    "input:kb_layout",
    max=100,
)

settings_keyboard_kb_variant = SpinRow(
    "Keyboard Variant",
    "Keyboard variant.",
    "input:kb_variant",
    max=100,
)

settings_keyboard_kb_options = SpinRow(
    "Keyboard Options",
    "Comma-separated list of keyboard options.",
    "input:kb_options",
    max=100,
)

settings_keyboard_kb_rules = SpinRow(
    "Keyboard Rules",
    "Keyboard rules.",
    "input:kb_rules",
    max=100,
)

settings_keyboard_kb_model = SpinRow(
    "Keyboard Model",
    "Keyboard model.",
    "input:kb_model",
    max=100,
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
    settings_keyboard,
    settings_mouse,
    settings_touchpad,
    settings_tablet,
]:
    input_page.add(i)

