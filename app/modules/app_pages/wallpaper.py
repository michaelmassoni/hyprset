from ..widgets import (
    PreferencesGroup,
    InfoButton,
)
from ..imports import Adw

wallpaper_page = Adw.PreferencesPage.new()

settings_wallpaper = PreferencesGroup("Wallpaper", "Hyprpaper configuration.")
settings_wallpaper.set_header_suffix(
    InfoButton(
        "Hyprpaper settings are not yet fully implemented. "
        "Please edit ~/.config/hypr/hyprpaper.conf manually for now."
    )
)

info = Adw.ActionRow.new()
info.set_title("Wallpaper Configuration")
info.set_subtitle("Coming soon...")
settings_wallpaper.add(info)

wallpaper_page.add(settings_wallpaper)
