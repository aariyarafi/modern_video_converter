#!/usr/bin/env python3
"""
Modern Video Converter
A user-friendly video conversion application built with Python and PyQt5.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main

if __name__ == '__main__':
    main()

