from ..widgets import (
    PreferencesGroup,
    SwitchRow,
    BezierGroup,
    InfoButton,
    ExpanderRow,
    SpinRow,
)
from ..imports import Adw


animations_page = Adw.PreferencesPage.new()


settings_animations = PreferencesGroup("General", "Enable or disable animations.")
settings_animations.add(
    SwitchRow(
        "Animations Enabled",
        "Master switch for all animations.",
        "animations:enabled",
    )
)

settings_animations.add(
    SwitchRow(
        "First Launch Animation",
        "Enable first launch animation.",
        "animations:first_launch_animation",
    )
)

settings_bezier = BezierGroup()

settings_anim_tree = PreferencesGroup(
    "Animation Tree",
    "Animation tree for windows, layers, border and workspaces.",
)
settings_anim_tree.set_header_suffix(
    InfoButton(
        "The animations are a tree. If an animation is unset, it will inherit its parent's values."
    )
)

settings_anim_tree_windows = ExpanderRow("Windows", "Window animations")
settings_anim_tree_windows_windowsIn = ExpanderRow("Windows In", "Window open")
settings_anim_tree_windows_windowsOut = ExpanderRow("Windows Out", "Window close")
settings_anim_tree_windows_windowsMove = ExpanderRow(
    "Windows Move", "Everything in between, moving, dragging and resizing."
)

settings_anim_tree_layers = ExpanderRow("Layers", "Layer animations")
settings_anim_tree_layers_layersIn = ExpanderRow("Layers In", "Layer open")
settings_anim_tree_layers_layersOut = ExpanderRow("Layers Out", "Layer close")

settings_anim_tree_border = ExpanderRow("Border", "Border animations")
settings_anim_tree_border_borderIn = ExpanderRow("Border In", "Border animation in")
settings_anim_tree_border_borderOut = ExpanderRow("Border Out", "Border animation out")

settings_anim_tree_workspaces = ExpanderRow("Workspaces", "Workspace animations")
settings_anim_tree_workspaces_workspacesIn = ExpanderRow("Workspaces In", "Workspace open")
settings_anim_tree_workspaces_workspacesOut = ExpanderRow("Workspaces Out", "Workspace close")

for i in [
    settings_anim_tree_windows_windowsIn,
    settings_anim_tree_windows_windowsOut,
    settings_anim_tree_windows_windowsMove,
]:
    settings_anim_tree_windows.add_row(i)

for i in [
    settings_anim_tree_layers_layersIn,
    settings_anim_tree_layers_layersOut,
]:
    settings_anim_tree_layers.add_row(i)

for i in [
    settings_anim_tree_border_borderIn,
    settings_anim_tree_border_borderOut,
]:
    settings_anim_tree_border.add_row(i)

for i in [
    settings_anim_tree_workspaces_workspacesIn,
    settings_anim_tree_workspaces_workspacesOut,
]:
    settings_anim_tree_workspaces.add_row(i)

for i in [
    settings_anim_tree_windows,
    settings_anim_tree_layers,
    settings_anim_tree_border,
    settings_anim_tree_workspaces,
]:
    settings_anim_tree.add(i)


for i in [settings_animations, settings_bezier, settings_anim_tree]:
    animations_page.add(i)
