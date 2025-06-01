import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works in dev and PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # Base path is the directory containing the script (not cwd!)
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("INPUT: ", relative_path, "OUTPUT: ", os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)
