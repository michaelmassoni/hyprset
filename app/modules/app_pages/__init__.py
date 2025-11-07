# Lazy imports - pages are only loaded when accessed
# This speeds up startup, especially when Hyprland isn't running

def _get_general_page():
    from .general import general_page
    return general_page

def _get_decoration_page():
    from .decoration import decoration_page
    return decoration_page

def _get_animations_page():
    from .animations import animations_page
    return animations_page

def _get_input_page():
    from .input import input_page
    return input_page

def _get_gestures_page():
    from .gestures import gestures_page
    return gestures_page

def _get_group_page():
    from .group import group_page
    return group_page

def _get_misc_page():
    from .misc import misc_page
    return misc_page

def _get_binds_page():
    from .binds import binds_page
    return binds_page

def _get_variables_page():
    from .variables import variables_page
    return variables_page

def _get_more_page():
    from .more import more_page
    return more_page

# Import decoration_page directly for the pop_to_tag call
from .decoration import decoration_page

PAGES_DICT = {
    'General': _get_general_page,
    'Decoration': _get_decoration_page,
    'Animations': _get_animations_page,
    'Input': _get_input_page,
    'Gestures': _get_gestures_page,
    'Group': _get_group_page,
    'Misc': _get_misc_page,
    'Binds': _get_binds_page,
    'Variables': _get_variables_page,
    'More': _get_more_page,
}

PAGES_LIST = [
    {
        'icon': 'settings-symbolic',
        'label': 'General',
        'desc': 'Gaps, borders, colors, cursor and other settings.',
    },
    {
        'icon': 'window-new-symbolic',
        'label': 'Decoration',
        'desc': 'Rounding, blur, transparency, shadow and dim settings.',
    },
    {
        'icon': 'move-to-window-symbolic',
        'label': 'Animations',
        'desc': 'Change animations settings.',
    },
    {'separator': True},
    {
        'icon': 'input-keyboard-symbolic',
        'label': 'Input',
        'desc': 'Change input settings.',
    },
    {
        'icon': 'input-touchpad-symbolic',
        'label': 'Gestures',
        'desc': 'Gesture and swipe settings.',
    },
    {
        'icon': 'overlapping-windows-symbolic',
        'label': 'Group',
        'desc': 'Change group settings.',
    },
    {'separator': True},
    {
        'icon': 'preferences-system-symbolic',
        'label': 'Misc',
        'desc': 'Change miscellaneous settings.',
    },
    {
        'icon': 'preferences-desktop-keyboard-shortcuts-symbolic',
        'label': 'Binds',
        'desc': 'Change binds settings.',
    },
    {
        'icon': 'test-symbolic',
        'label': 'Variables',
        'desc': 'Adjust variables.',
    },
    {'separator': True},
    {
        # "icon": "preferences-desktop-wallpaper-symbolic",
        'icon': 'preferences-desktop-appearance-symbolic',
        'label': 'Wallpaper',
        'desc': 'Hyprpaper settings.',
    },
    {
        'icon': 'background-app-sleepyface-symbolic',
        'label': 'Idle',
        'desc': 'Hypridle settings.',
    },
    {
        'icon': 'key4-symbolic',
        'label': 'Lock',
        'desc': 'Hyprlock settings.',
    },
    {'separator': True},
    {'icon': 'view-more-symbolic', 'label': 'More', 'desc': ''},
]
