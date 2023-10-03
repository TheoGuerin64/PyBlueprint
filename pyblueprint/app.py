"""Main application file for PyBlueprint."""

import sys

from PyQt6 import QtWidgets

from main_window import MainWindow


def main() -> None:
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
