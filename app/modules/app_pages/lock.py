from ..widgets import (
    PreferencesGroup,
    InfoButton,
)
from ..imports import Adw

lock_page = Adw.PreferencesPage.new()

settings_lock = PreferencesGroup("Lock", "Hyprlock configuration.")
settings_lock.set_header_suffix(
    InfoButton(
        "Hyprlock settings are not yet fully implemented. "
        "Please edit ~/.config/hypr/hyprlock.conf manually for now."
    )
)

info = Adw.ActionRow.new()
info.set_title("Lock Configuration")
info.set_subtitle("Coming soon...")
settings_lock.add(info)

lock_page.add(settings_lock)
