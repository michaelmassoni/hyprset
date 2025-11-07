from ..widgets import (
    PreferencesGroup,
    InfoButton,
)
from ..imports import Adw


binds_page = Adw.PreferencesPage.new()

# Binds Info
settings_binds = PreferencesGroup("Keybindings", "Configure keyboard and mouse bindings.")
settings_binds.set_header_suffix(
    InfoButton(
        "Keybindings are configured in the Hyprland config file. "
        "Use the config file editor or command line tools to manage bindings. "
        "This section will show existing bindings when implemented."
    )
)

# Note: Full keybinding management (add/remove/edit) is complex and would require
# parsing and editing the binds section of the config file. This is a placeholder
# that can be expanded later with a proper keybinding editor widget.

settings_binds_info = Adw.ActionRow.new()
settings_binds_info.set_title("Keybinding Management")
settings_binds_info.set_subtitle("Keybinding management will be available in a future update.")

settings_binds.add(settings_binds_info)

# Add sections
for i in [
    settings_binds,
]:
    binds_page.add(i)

