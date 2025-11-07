from ..widgets import (
    PreferencesGroup,
    SwitchRow,
    SpinRow,
)
from ..imports import Adw


gestures_page = Adw.PreferencesPage.new()

# Gestures
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

settings_gestures_workspace_swipe_numbered = SwitchRow(
    "Numbered Workspaces",
    "Use numbered workspaces for swipe.",
    "gestures:workspace_swipe_numbered",
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
    settings_gestures_workspace_swipe_numbered,
]:
    settings_gestures.add(i)

# Add sections
for i in [
    settings_gestures,
]:
    gestures_page.add(i)

