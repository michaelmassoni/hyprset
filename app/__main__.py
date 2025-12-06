import sys
import os
import traceback

# Suppress GTK CSS parser warnings (they're harmless)
os.environ['G_MESSAGES_DEBUG'] = ''
os.environ['GTK_DEBUG'] = ''

# Increase recursion limit to handle hyprparser parsing issues
# Increase recursion limit to handle hyprparser parsing issues
sys.setrecursionlimit(5000)

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

def check_needs_setup():
    path = os.path.expanduser("~/.config/hypr/hyprland.conf")
    return not os.path.exists(path)

if check_needs_setup():
    from modules.config_manager import download_default_config

    class SetupApplication(Adw.Application):
        def __init__(self):
            super().__init__(application_id='com.michaelmassoni.hyprset.setup', flags=Gio.ApplicationFlags.FLAGS_NONE)

        def do_activate(self):
            self.win = Adw.ApplicationWindow(application=self)
            self.win.set_title("Hyprset Setup")
            self.win.set_default_size(400, 200)
            
            # Show dialog immediately
            self.show_dialog(self.win)
            
            self.win.present()

        def show_dialog(self, window):
            def on_dialog_response(dialog, response):
                if response == 'download':
                    if download_default_config():
                        success = Adw.MessageDialog(
                            transient_for=window,
                            heading="Success",
                            body="Default configuration installed.\nContinuing to application..."
                        )
                        success.add_response("ok", "Continue")
                        success.connect("response", lambda *args: self.finish())
                        success.present()
                    else:
                        err = Adw.MessageDialog(
                            transient_for=window,
                            heading="Error",
                            body="Download failed. Please check internet connection."
                        )
                        err.add_response("ok", "Quit")
                        err.connect("response", lambda *args: self.finish())
                        err.present()
                else:
                    self.finish()
                dialog.close()

            dialog = Adw.MessageDialog(
                transient_for=window,
                heading="No Config Found",
                body="No Hyprland configuration file was found.\nWould you like to download and install the default configuration?",
            )
            dialog.add_response("quit", "Quit")
            dialog.add_response("download", "Download & Install")
            dialog.set_response_appearance("download", Adw.ResponseAppearance.SUGGESTED)
            dialog.connect("response", on_dialog_response)
            dialog.present()

        def finish(self):
            if hasattr(self, 'win'):
                self.win.close()
            self.quit()

    app = SetupApplication()
    app.run(None)
    
    if check_needs_setup():
        print("Setup incomplete. Exiting.", file=sys.stderr)
        sys.exit(1)

from modules.app import MyApplication


def main() -> None:
    try:
        MyApplication.run()
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        print(f"CRITICAL ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    finally:
        exit(0)


if __name__ == '__main__':
    main()
