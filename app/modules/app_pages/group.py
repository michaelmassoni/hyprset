from ..widgets import (
    PreferencesGroup,
    SwitchRow,
    SpinRow,
    ColorExpanderRow,
)
from ..imports import Adw


group_page = Adw.PreferencesPage.new()

# Group Settings
settings_group = PreferencesGroup("Group", "Window grouping settings.")

settings_group_insert_after_current = SwitchRow(
    "Insert After Current",
    "Insert new windows after the current window in the group.",
    "group:insert_after_current",
)

settings_group_focus_removed_window = SwitchRow(
    "Focus Removed Window",
    "Focus the window that was removed from the group.",
    "group:focus_removed_window",
)

settings_group_lock_new_group_members = SwitchRow(
    "Lock New Group Members",
    "Lock new group members.",
    "group:lock_new_group_members",
)

settings_group_bar_enabled = SwitchRow(
    "Bar Enabled",
    "Enable the group bar.",
    "group:bar:enabled",
)

settings_group_bar_height = SpinRow(
    "Bar Height",
    "Height of the group bar in pixels.",
    "group:bar:height",
    min=0,
    max=100,
)

settings_group_bar_priority = SpinRow(
    "Bar Priority",
    "Priority of the group bar. Higher values are drawn on top.",
    "group:bar:priority",
    min=0,
    max=1000,
)

settings_group_bar_font_family = SpinRow(
    "Bar Font Family",
    "Font family for the group bar.",
    "group:bar:font_family",
    max=100,
)

settings_group_bar_font_size = SpinRow(
    "Bar Font Size",
    "Font size for the group bar.",
    "group:bar:font_size",
    min=1,
    max=100,
)

settings_group_bar_gradient = SwitchRow(
    "Bar Gradient",
    "Enable gradient for the group bar.",
    "group:bar:gradient",
)

settings_group_bar_col_active = ColorExpanderRow(
    "Bar Active Color",
    "Active color for the group bar.",
    "group:bar:col.active",
)

settings_group_bar_col_inactive = ColorExpanderRow(
    "Bar Inactive Color",
    "Inactive color for the group bar.",
    "group:bar:col.inactive",
)

settings_group_bar_col_locked_active = ColorExpanderRow(
    "Bar Locked Active Color",
    "Locked active color for the group bar.",
    "group:bar:col.locked_active",
)

settings_group_bar_col_locked_inactive = ColorExpanderRow(
    "Bar Locked Inactive Color",
    "Locked inactive color for the group bar.",
    "group:bar:col.locked_inactive",
)

# Add group settings
for i in [
    settings_group_insert_after_current,
    settings_group_focus_removed_window,
    settings_group_lock_new_group_members,
    settings_group_bar_enabled,
    settings_group_bar_height,
    settings_group_bar_priority,
    settings_group_bar_font_family,
    settings_group_bar_font_size,
    settings_group_bar_gradient,
    settings_group_bar_col_active,
    settings_group_bar_col_inactive,
    settings_group_bar_col_locked_active,
    settings_group_bar_col_locked_inactive,
]:
    settings_group.add(i)

# Add sections
for i in [
    settings_group,
]:
    group_page.add(i)

