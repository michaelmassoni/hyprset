from ..widgets import (
    PreferencesGroup,
    InfoButton,
)
from ..imports import Adw


more_page = Adw.PreferencesPage.new()

# More Info
settings_more = PreferencesGroup("Additional Settings", "Additional configuration options.")
settings_more.set_header_suffix(
    InfoButton(
        "This section contains additional settings and features that may be added in future updates."
    )
)

settings_more_info = Adw.ActionRow.new()
settings_more_info.set_title("More Settings")
settings_more_info.set_subtitle("Additional settings and features will be available here in future updates.")

settings_more.add(settings_more_info)

# Add sections
for i in [
    settings_more,
]:
    more_page.add(i)

