import sys

from PyQt6 import QtWidgets


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
