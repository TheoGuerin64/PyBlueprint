"""Main application file for PyBlueprint."""

import sys

import argparse
from PyQt6 import QtWidgets

from pyblueprint.main_window import MainWindow


def parse_args() -> argparse.Namespace:
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser(description="PyBlueprint")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.settings.setValue("debug", args.debug)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
