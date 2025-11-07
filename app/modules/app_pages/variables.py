from ..widgets import (
    PreferencesGroup,
    SpinRow,
    InfoButton,
)
from ..imports import Adw


variables_page = Adw.PreferencesPage.new()

# Variables Info
settings_variables = PreferencesGroup("Variables", "Environment variables and configuration variables.")
settings_variables.set_header_suffix(
    InfoButton(
        "Variables are defined in the Hyprland config file using the $ syntax. "
        "Common variables include paths, colors, and other reusable values."
    )
)

# Note: Variable management would require parsing and editing the variables section.
# This is a placeholder that can be expanded later with a proper variable editor.

settings_variables_info = Adw.ActionRow.new()
settings_variables_info.set_title("Variable Management")
settings_variables_info.set_subtitle("Variable management will be available in a future update. "
                                     "Variables are typically defined at the top of your config file.")

settings_variables.add(settings_variables_info)

# Add sections
for i in [
    settings_variables,
]:
    variables_page.add(i)

