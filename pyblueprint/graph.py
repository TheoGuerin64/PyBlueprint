from PyQt6 import QtCore, QtGui, QtWidgets


class Graph(QtWidgets.QGraphicsView):
    """A graph view to display nodes and connections."""
    BACKGROUND_COLOR = QtGui.QColor(38, 38, 38)
    AXIS_COLOR = QtGui.QColor(0, 0, 0)
    MAIN_LINE_COLOR = QtGui.QColor(22, 22, 22)
    SECONDARY_LINE_COLOR = QtGui.QColor(52, 52, 52)
    DEFAULT_RECT = QtCore.QRectF(-2000, -2000, 4000, 4000)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        """Construct a new Graph object and set up the scene."""
        super().__init__(parent)
        self._drag_start = False
        self._zoom = 100

        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI."""
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setSceneRect(self.DEFAULT_RECT)

        # Set up view
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheModeFlag.CacheBackground)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # Set up zoom label
        self.zoom_label = QtWidgets.QLabel("100%", self)
        self.zoom_label.setGeometry(QtCore.QRect(4, 0, 46, 20))
        self.zoom_label.setStyleSheet("color: grey")

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        """Override drawBackground to draw grid and axis."""
        half_width = round(self.sceneRect().width() / 2)
        half_height = round(self.sceneRect().height() / 2)

        # Draw background
        painter.fillRect(rect, self.BACKGROUND_COLOR)

        # Draw secondary lines
        painter.setPen(self.SECONDARY_LINE_COLOR)
        for x in range(-half_width, half_width, 20):
            painter.drawLine(x, -half_height, x, half_height)
        for y in range(-half_height, half_height, 20):
            painter.drawLine(-half_width, y, half_width, y)

        # Draw main lines
        painter.setPen(self.MAIN_LINE_COLOR)
        for x in range(-half_width, half_width, 100):
            painter.drawLine(x, -half_height, x, half_height)
        for y in range(-half_height, half_height, 100):
            painter.drawLine(-half_width, y, half_width, y)

        # Draw axis lines
        painter.setPen(self.AXIS_COLOR)
        painter.drawLine(0, -half_height, 0, half_height)
        painter.drawLine(-half_width, 0, half_width, 0)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """Override mouseMoveEvent to handle dragging."""
        if event.buttons() == QtCore.Qt.MouseButton.RightButton:
            if not self._drag_start:
                self._drag_start = True
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
                self.setInteractive(False)

                e = QtGui.QMouseEvent(
                    QtCore.QEvent.Type.MouseButtonPress,
                    event.position(), event.globalPosition(),
                    QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.NoButton,
                    QtCore.Qt.KeyboardModifier.NoModifier
                )
                QtWidgets.QGraphicsView.mousePressEvent(self, e)
        QtWidgets.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Override mouseReleaseEvent to handle drag end and context menu."""
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self._drag_start:
                self._drag_start = False
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
                self.setInteractive(True)
            else:
                if self.itemAt(event.position().toPoint()) is None:
                    self._context_menu(event.position().toPoint())
                else:
                    QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """Override wheelEvent to handle zoom."""
        zoom_delta = 10 if event.angleDelta().y() > 0 else -10

        new_zoom = self._zoom + zoom_delta
        if 50 <= new_zoom <= 100:
            self.scale(100 / self._zoom, 100 / self._zoom)
            self._zoom = new_zoom
            self.scale(self._zoom / 100, self._zoom / 100)

            self.zoom_label.setText(f"{self._zoom}%")

    def _context_menu(self, position: QtCore.QPoint) -> None:
        """Show graph context menu."""
        menu = QtWidgets.QMenu(self)
        exit_action = menu.addAction("Exit")
        action = menu.exec(self.mapToGlobal(position))
        if action == exit_action:
            self.parent().close()
