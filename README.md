# Hyprset

A GTK4/LibAdwaita tool to configure your Hyprland desktop.

Built using [hyprparser-py](https://github.com/tokyob0t/hyprparser-py)

![app_image](./img/app.png)

## Installation

### Dependencies

Hyprset requires:
- Python 3
- GTK4 & LibAdwaita
- PyGObject (`gi`)
- `hyprparser` (Python library)

### Manual Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/michaelmassoni/hyprset.git
   cd hyprset
   ```

2. Install dependencies:
   ```bash
   # Fedora
   sudo dnf install python3-gobject gtk4 libadwaita
   
   # Arch
   sudo pacman -S python-gobject gtk4 libadwaita
   ```

3. Install Python dependencies:
   ```bash
   pip install --user PyGObject
   ```
   *Note: `hyprparser` is currently expected to be in the python path or installed manually.*

## Usage

To launch the application:

```bash
python3 app/__main__.py
```

---

## Roadmap

- [ ] Support colors, gradients, etc.
- [ ] Add a preview for decoration settings
- [ ] Keybinding management
- [ ] Environment variables management
- [ ] Startup commands management
- [ ] Pages:
  - [x] General
  - [x] Decoration
  - [ ] Animations
  - [ ] Input
  - [ ] Gestures
  - [ ] Group
  - [ ] Misc
  - [ ] Binds
  - [ ] Variables
