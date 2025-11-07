from ..widgets import (
    PreferencesGroup,
    SwitchRow,
    SpinRow,
)
from ..imports import Adw


misc_page = Adw.PreferencesPage.new()

# General Misc
settings_misc = PreferencesGroup("General", "Miscellaneous settings.")

settings_misc_force_default_wallpaper = SwitchRow(
    "Force Default Wallpaper",
    "Force the default wallpaper.",
    "misc:force_default_wallpaper",
)

settings_misc_vfr = SwitchRow(
    "VFR",
    "Enable variable frame rate.",
    "misc:vfr",
)

settings_misc_vrr = SwitchRow(
    "VRR",
    "Enable variable refresh rate.",
    "misc:vrr",
)

settings_misc_disable_hyprland_logo = SwitchRow(
    "Disable Hyprland Logo",
    "Disable the Hyprland logo on startup.",
    "misc:disable_hyprland_logo",
)

settings_misc_disable_splash_rendering = SwitchRow(
    "Disable Splash Rendering",
    "Disable splash rendering.",
    "misc:disable_splash_rendering",
)

settings_misc_always_follow_on_dnd = SwitchRow(
    "Always Follow on DnD",
    "Always follow the cursor when dragging and dropping.",
    "misc:always_follow_on_dnd",
)

settings_misc_layers_hog_memory = SwitchRow(
    "Layers Hog Memory",
    "Layers will hog memory.",
    "misc:layers_hog_memory",
)

settings_misc_animate_manual_resizes = SwitchRow(
    "Animate Manual Resizes",
    "Animate manual window resizes.",
    "misc:animate_manual_resizes",
)

settings_misc_animate_mouse_windowdragging = SwitchRow(
    "Animate Mouse Window Dragging",
    "Animate window dragging with mouse.",
    "misc:animate_mouse_windowdragging",
)

settings_misc_disable_autoreload = SwitchRow(
    "Disable Autoreload",
    "Disable automatic config reload.",
    "misc:disable_autoreload",
)

settings_misc_enable_swallow = SwitchRow(
    "Enable Swallow",
    "Enable window swallowing.",
    "misc:enable_swallow",
)

settings_misc_swallow_regex = SpinRow(
    "Swallow Regex",
    "Regex pattern for window swallowing.",
    "misc:swallow_regex",
    max=200,
)

settings_misc_swallow_exception_regex = SpinRow(
    "Swallow Exception Regex",
    "Regex pattern for exceptions to window swallowing.",
    "misc:swallow_exception_regex",
    max=200,
)

settings_misc_focus_on_activate = SwitchRow(
    "Focus on Activate",
    "Focus window when it's activated.",
    "misc:focus_on_activate",
)

settings_misc_no_direct_scanout = SwitchRow(
    "No Direct Scanout",
    "Disable direct scanout.",
    "misc:no_direct_scanout",
)

settings_misc_hide_cursor_on_touch = SwitchRow(
    "Hide Cursor on Touch",
    "Hide cursor when touching the screen.",
    "misc:hide_cursor_on_touch",
)

settings_misc_mouse_move_enables_dpms = SwitchRow(
    "Mouse Move Enables DPMS",
    "Mouse movement enables DPMS.",
    "misc:mouse_move_enables_dpms",
)

settings_misc_keyboard_move_enables_dpms = SwitchRow(
    "Keyboard Move Enables DPMS",
    "Keyboard input enables DPMS.",
    "misc:keyboard_move_enables_dpms",
)

# Add misc settings
for i in [
    settings_misc_force_default_wallpaper,
    settings_misc_vfr,
    settings_misc_vrr,
    settings_misc_disable_hyprland_logo,
    settings_misc_disable_splash_rendering,
    settings_misc_always_follow_on_dnd,
    settings_misc_layers_hog_memory,
    settings_misc_animate_manual_resizes,
    settings_misc_animate_mouse_windowdragging,
    settings_misc_disable_autoreload,
    settings_misc_enable_swallow,
    settings_misc_swallow_regex,
    settings_misc_swallow_exception_regex,
    settings_misc_focus_on_activate,
    settings_misc_no_direct_scanout,
    settings_misc_hide_cursor_on_touch,
    settings_misc_mouse_move_enables_dpms,
    settings_misc_keyboard_move_enables_dpms,
]:
    settings_misc.add(i)

# Add sections
for i in [
    settings_misc,
]:
    misc_page.add(i)

