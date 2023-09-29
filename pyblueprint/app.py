import sys

from main_window import MainWindow
from PyQt6 import QtWidgets


def main() -> None:
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
