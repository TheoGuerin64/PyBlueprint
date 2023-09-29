from path import ICON_PATH
from PyQt6 import QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("PyBlueprint")
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
