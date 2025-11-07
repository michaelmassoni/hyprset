#!/bin/bash
# Launcher script for Hyprset

cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)/app:$PYTHONPATH"

# Suppress GTK CSS parser warnings (they're harmless)
export G_MESSAGES_DEBUG=""
export GTK_DEBUG=""

# Redirect GTK warnings to /dev/null, but keep real errors
exec python3 -m app "$@" 2> >(grep -v "Theme parser error" | grep -v "Gtk-WARNING" | grep -v "libadwaita" >&2)

