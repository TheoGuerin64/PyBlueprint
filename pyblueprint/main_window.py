from PyQt6 import QtGui, QtWidgets, QtCore

from .graph import Graph
from .path import ICON_PATH


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application."""
    def __init__(self) -> None:
        super().__init__()
        self.settings = QtCore.QSettings("TheoGuerin", "PyBlueprint")

        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI."""
        self.setWindowTitle("PyBlueprint")
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.resize(800, 800)
        self.setCentralWidget(Graph(self))
