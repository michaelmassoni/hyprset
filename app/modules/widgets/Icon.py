from ..imports import Literal, Gio, GLib, Gtk


def Icon(
    name: str, size: Literal["large", "normal", "inherit"] = "normal"
) -> Gtk.Image:
    display = GLib.Variant("s", "") # Placeholder check, actual check needs StyleManager or settings
    # Since Icon is a function returning Gtk.Image, we can't easily react to theme changes dynamically 
    # unless we return a custom widget class or bind it. 
    # But for initialization transparency:
    
    from pathlib import Path
    # ../../icons
    base_dir = Path(__file__).parent.parent.parent / "icons"
    target_file = base_dir / f"{name}.svg"
    
    # Check dark mode for layout diagrams (prefixed with _)
    try:
        from ..imports import Adw
        style_manager = Adw.StyleManager.get_default()
        if style_manager.get_dark():
             dark_file = base_dir / f"_{name}.svg"
             if dark_file.exists():
                 target_file = dark_file
    except Exception:
        pass

    new_icon = Gtk.Image.new()
    
    if target_file.exists():
        new_icon.set_from_file(str(target_file))
    else:
        new_icon.set_from_icon_name(name)
    match size:
        case "large":
            new_icon.set_icon_size(Gtk.IconSize.LARGE)
        case "normal":
            new_icon.set_icon_size(Gtk.IconSize.NORMAL)
        case "inherit":
            new_icon.set_icon_size(Gtk.IconSize.INHERIT)

    return new_icon
