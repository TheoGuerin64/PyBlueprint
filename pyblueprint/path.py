"""Path to the pyblueprint package and its assets."""

import os

PYBLUEPRINT_PATH = os.path.dirname(os.path.dirname(__file__))
ASSETS_PATH = os.path.join(PYBLUEPRINT_PATH, "assets")
ICON_PATH = os.path.join(ASSETS_PATH, "icon.ico")
