"""Root runner for Kiran's Star-Style ASCII Birthday Surprise.

Allows running directly from workspace root:
    python main.py
"""

import os
import sys

# Ensure birthday_ascii is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(SCRIPT_DIR, "birthday_ascii")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from main import main

if __name__ == "__main__":
    main()
