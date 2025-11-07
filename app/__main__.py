import sys
import os
import traceback

# Suppress GTK CSS parser warnings (they're harmless)
os.environ['G_MESSAGES_DEBUG'] = ''
os.environ['GTK_DEBUG'] = ''

# Increase recursion limit to handle hyprparser parsing issues
sys.setrecursionlimit(5000)

from modules.app import MyApplication


def main() -> None:
    try:
        print("Starting Hyprset application...", file=sys.stderr)
        MyApplication.run()
        print("Application started successfully", file=sys.stderr)
    except KeyboardInterrupt:
        print("Application interrupted by user", file=sys.stderr)
        pass
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    finally:
        exit(0)


if __name__ == '__main__':
    main()
