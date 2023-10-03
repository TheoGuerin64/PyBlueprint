"""Main application file for PyBlueprint."""

import sys

import argparse
from PyQt6 import QtWidgets

from main_window import MainWindow
from settings import settings


def parse_args() -> argparse.Namespace:
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser(description="PyBlueprint")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.debug:
        settings["debug"] = True

    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
