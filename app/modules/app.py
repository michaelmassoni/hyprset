from .app_pages import (
    PAGES_DICT,
    PAGES_LIST,
    decoration_page,
)
from .imports import Adw, Gdk, Gio, Gtk
from .widgets import Icon, ToastOverlay, MyBezierEditorWindow
from .config_manager import get_config_summary, check_config_files


class ApplicationWindow(Adw.ApplicationWindow):
    def __init__(self, app: Adw.Application):
        super().__init__(application=app)
        self.set_title("Hyprland Settings")
        MyBezierEditorWindow.set_transient_for(self)

        self.root = Adw.OverlaySplitView.new()
        self.breakpoint = Adw.Breakpoint.new(
            Adw.BreakpointCondition.parse('max-width: 900px')  # type: ignore
        )
        self.set_size_request(700, 360)
        self.set_content(self.root)
        self.add_breakpoint(self.breakpoint)
        self.breakpoint.add_setter(
            self.root, 'collapsed', True  # type: ignore
        )

        # Main Content
        self.main_content = Adw.ToolbarView.new()
        self.main_content_navigation_page = Adw.NavigationPage.new(
            self.main_content, 'General'
        )

        self.main_content_top_bar = Adw.HeaderBar.new()
        self.main_content_top_bar_title = Adw.WindowTitle.new(
            'General', 'Gaps, borders, colors, cursor and other settings.'
        )

        self.main_content.add_top_bar(self.main_content_top_bar)
        self.main_content_top_bar.set_title_widget(
            self.main_content_top_bar_title
        )
        self.main_content_view_stack = Adw.ViewStack.new()

        self.toast_overlay = ToastOverlay
        self.toast_overlay.instance.set_child(self.main_content_view_stack)
        self.main_content.set_content(self.toast_overlay.instance)

        # Sidebar
        self.sidebar = Adw.ToolbarView()
        self.sidebar.add_css_class('list-box-scroll')
        self.sidebar_navigation_page = Adw.NavigationPage.new(
            self.sidebar, 'Settings'
        )
        self.sidebar_navigation_page.add_css_class('sidebar')
        self.sidebar_top_bar = Adw.HeaderBar.new()
        self.sidebar.add_top_bar(self.sidebar_top_bar)
        self.sidebar_scrolled_window = Gtk.ScrolledWindow.new()
        self.sidebar_listbox = Gtk.ListBox.new()
        self.sidebar_scrolled_window.set_child(self.sidebar_listbox)
        self.sidebar.set_content(self.sidebar_scrolled_window)

        # Sidebar Stuff
        for item in PAGES_LIST:
            if item.get('separator'):
                tmp_rowbox = Gtk.ListBoxRow.new()
                tmp_rowbox.set_can_focus(False)
                tmp_rowbox.set_activatable(False)
                tmp_rowbox.set_selectable(False)
                tmp_rowbox.set_sensitive(False)
                tmp_rowbox.set_child(
                    Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
                )

            else:
                tmp_grid = Gtk.Grid.new()
                tmp_grid.set_column_spacing(12)
                tmp_grid.set_valign(Gtk.Align.CENTER)
                tmp_grid.set_vexpand(True)

                tmp_rowbox = Gtk.ListBoxRow.new()
                tmp_rowbox.add_css_class('list-box-row')
                setattr(tmp_rowbox, 'title', item['label'])
                setattr(tmp_rowbox, 'desc', item['desc'])

                label = Gtk.Label.new(item['label'])
                tmp_grid.attach(Icon(item['icon']), 0, 0, 1, 1)
                tmp_grid.attach(label, 1, 0, 1, 1)
                tmp_rowbox.set_child(tmp_grid)

            self.sidebar_listbox.append(tmp_rowbox)

        self.root.set_content(self.main_content_navigation_page)
        self.root.set_sidebar(self.sidebar_navigation_page)

        self.sidebar_listbox.connect('row-activated', self.on_row_activated)

        shortcut_controller = Gtk.ShortcutController.new()
        # Add ctrl+s shortcut
        shortcut_controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string('<Control>s'),
                Gtk.CallbackAction.new(self.toast_overlay.save_changes),
            )
        )

        self.root.add_controller(shortcut_controller)
        
        self.sidebar_listbox.unselect_all()
        
        # Check and log config file status
        try:
            config_status = check_config_files()
            print(f"Config status: {config_status['message']}", file=__import__('sys').stderr)
            if config_status['missing_files']:
                print(f"Warning: Missing config files: {config_status['missing_files']}", file=__import__('sys').stderr)
        except Exception as e:
            print(f"Warning: Could not check config files: {e}", file=__import__('sys').stderr)
        
        # Show window FIRST, then load pages (so user sees something immediately)
        self.set_visible(True)
        self.present()
        self.set_focus()
        
        # Add pages after window is shown (this might take time due to HyprData access)
        # Use GLib.idle_add to do this asynchronously so window appears immediately
        from gi.repository import GLib
        def load_pages():
            try:
                self.add_pages()
            except Exception as e:
                print(f"Error adding pages: {e}", file=__import__('sys').stderr)
                import traceback
                traceback.print_exc()
        GLib.idle_add(load_pages)

    def on_row_activated(self, _, sidebar_rowbox: Gtk.ListBoxRow):
        page_name = getattr(sidebar_rowbox, 'title')
        
        # Update UI immediately
        self.main_content_top_bar_title.set_title(page_name)
        self.main_content_top_bar_title.set_subtitle(
            getattr(sidebar_rowbox, 'desc')
        )
        
        # Check if page is already loaded
        existing = self.main_content_view_stack.get_child_by_name(page_name)
        if existing:
            # Page already loaded, just switch to it
            match self.main_content_view_stack.get_visible_child_name().lower():
                case 'general':
                    pass
                case 'decoration':
                    decoration_page.pop_to_tag('index-page')
                case _:
                    pass
            self.main_content_view_stack.set_visible_child_name(page_name)
            return
        
        # Page not loaded yet - load it asynchronously to avoid freezing UI
        from gi.repository import GLib
        def load_and_switch():
            try:
                page = self.get_or_load_page(page_name)
                if page is None:
                    print(f"Failed to load page '{page_name}'", file=__import__('sys').stderr)
                    return False
                
                # Switch to the page after it's loaded
                match self.main_content_view_stack.get_visible_child_name().lower():
                    case 'general':
                        pass
                    case 'decoration':
                        decoration_page.pop_to_tag('index-page')
                    case _:
                        pass
                self.main_content_view_stack.set_visible_child_name(page_name)
                return False  # Don't repeat
            except Exception as e:
                print(f"Error loading page '{page_name}': {e}", file=__import__('sys').stderr)
                import traceback
                traceback.print_exc(file=__import__('sys').stderr)
                return False  # Don't repeat
        
        # Load page asynchronously so UI doesn't freeze
        GLib.idle_add(load_and_switch)

    def add_pages(self):
        # Only add the General page initially - others will be loaded on demand
        # This speeds up startup when Hyprland isn't running
        try:
            general_page = PAGES_DICT['General']()
            self.main_content_view_stack.add_named(general_page, 'General')
        except Exception as e:
            print(f"Warning: Could not add page 'General': {e}", file=__import__('sys').stderr)
            import traceback
            traceback.print_exc()
    
    def get_or_load_page(self, name: str):
        """Get a page, loading it if it hasn't been loaded yet."""
        # Check if page is already in the stack
        existing = self.main_content_view_stack.get_child_by_name(name)
        if existing:
            return existing
        
        # Load the page lazily
        if name in PAGES_DICT:
            try:
                page_getter = PAGES_DICT[name]
                page = page_getter()
                self.main_content_view_stack.add_named(page, name)
                return page
            except Exception as e:
                print(f"Error: Could not load page '{name}': {e}", file=__import__('sys').stderr)
                import traceback
                traceback.print_exc(file=__import__('sys').stderr)
                # Return None to indicate failure, but don't crash the app
                return None
        return None


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__()
        self.window = None
        self.set_application_id('com.tokyob0t.HyprSettings')
        self.set_flags(Gio.ApplicationFlags.FLAGS_NONE)
        self.load_css()

    def load_css(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f'{__file__[:-15]}/style.css')

        return Gtk.StyleContext.add_provider_for_display(  # type: ignore
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_activate(self) -> None:
        if not self.window:
            try:
                print("Creating ApplicationWindow...", file=__import__('sys').stderr)
                self.window = ApplicationWindow(self)
                print("ApplicationWindow created successfully", file=__import__('sys').stderr)
            except Exception as e:
                print(f"Error creating window: {e}", file=__import__('sys').stderr)
                import traceback
                traceback.print_exc(file=__import__('sys').stderr)
                return
        print("Presenting window...", file=__import__('sys').stderr)
        self.window.present()
        self.window.set_focus()
        print("Window presented", file=__import__('sys').stderr)


MyApplication = Application()
