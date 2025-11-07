# Installation and Setup Guide

## Project Analysis

**Hyprset** is a GTK4/LibAdwaita desktop application for configuring Hyprland window manager settings. It provides a graphical interface to edit Hyprland configuration files.

## Dependencies

### System Dependencies (Already Installed ✓)
- **Python 3.12.3** - Python runtime
- **GTK4** - GTK toolkit version 4
- **LibAdwaita** - Adwaita UI library
- **GObject Introspection (gi)** - Python bindings for GTK4/Adwaita
  - Adw 1
  - GdkPixbuf 2.0
  - Gdk 4.0
  - Gtk 4.0

### Python Dependencies
- **hyprparser** - Python parser for Hyprland configuration files
  - **Note**: Not available on PyPI, must be installed from GitHub
  - Repository: https://github.com/tokyob0t/hyprparser-py

## Installation Steps

### 1. Install pip (if not already installed)
```bash
curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user --break-system-packages
```

### 2. Install hyprparser
```bash
~/.local/bin/pip install --user --break-system-packages git+https://github.com/tokyob0t/hyprparser-py.git
```

Or using the requirements file:
```bash
~/.local/bin/pip install --user --break-system-packages -r requirements.txt
```

**Note**: On Debian/Ubuntu systems with PEP 668 protection, you may need to use `--break-system-packages` flag or set up a virtual environment.

### 3. Ensure Hyprland config file exists
The `hyprparser` package requires a Hyprland configuration file to exist:
```bash
mkdir -p ~/.config/hypr
touch ~/.config/hypr/hyprland.conf
```

If you don't have Hyprland installed, you can create a minimal config file for testing.

## Running the Application

### Easiest Way: Use the launcher script
```bash
cd /home/michael/hyprset
./run.sh
```

### Option 1: Run as a module (from project directory)
```bash
cd /home/michael/hyprset
PYTHONPATH=/home/michael/hyprset/app python3 -m app
```

### Option 2: Add to your shell config (recommended for frequent use)
Add the following to your `~/.bashrc` or `~/.zshrc`:
```bash
export PYTHONPATH="/home/michael/hyprset/app:$PYTHONPATH"
```

Then you can run from anywhere:
```bash
cd /home/michael/hyprset
python3 -m app
```

Or create an alias:
```bash
alias hyprset='cd /home/michael/hyprset && PYTHONPATH=/home/michael/hyprset/app python3 -m app'
```

## Project Structure

- `app/` - Main application directory
  - `__main__.py` - Application entry point
  - `modules/` - Application modules
    - `app.py` - Main application class
    - `imports.py` - Dependency imports
    - `app_pages/` - Configuration pages (General, Decoration, Animations, etc.)
    - `widgets/` - Custom GTK widgets
  - `style.css` - Compiled CSS styles
  - `style.scss` - SCSS source (already compiled)
  - `icons/` - Application icons

## Additional Notes

- The application requires a running X11/Wayland session with GTK4 support
- The `hyprparser` package reads the Hyprland config file on import, so the file must exist
- CSS is already compiled from SCSS, so no additional build step is needed
- The application uses LibAdwaita for modern GNOME/GTK theming

## Troubleshooting

### ModuleNotFoundError: No module named 'modules'
- Ensure you're running from the correct directory or set PYTHONPATH

### FileNotFoundError: hyprland.conf
- Create the config directory and file: `mkdir -p ~/.config/hypr && touch ~/.config/hypr/hyprland.conf`

### GTK4/Adwaita not found
- Install system packages: `sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1`

