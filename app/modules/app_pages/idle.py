from ..widgets import (
    PreferencesGroup,
    InfoButton,
)
from ..imports import Adw

idle_page = Adw.PreferencesPage.new()

settings_idle = PreferencesGroup("Idle", "Hypridle configuration.")
settings_idle.set_header_suffix(
    InfoButton(
        "Hypridle settings are not yet fully implemented. "
        "Please edit ~/.config/hypr/hypridle.conf manually for now."
    )
)

info = Adw.ActionRow.new()
info.set_title("Idle Configuration")
info.set_subtitle("Coming soon...")
settings_idle.add(info)

idle_page.add(settings_idle)
