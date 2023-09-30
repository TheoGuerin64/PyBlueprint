from nodes import Branch, Print
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
        self.zoom = 100

        self.init_ui()

        self._half_width = round(self.sceneRect().width() / 2)
        self._half_height = round(self.sceneRect().height() / 2)

    def scene(self) -> QtWidgets.QGraphicsScene:
        """Override scene to return a typed scene."""

        scene = super().scene()
        if scene is None:
            raise RuntimeError("Scene is None")
        return scene

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

    def drawBackground(self, painter: QtGui.QPainter | None, rect: QtCore.QRectF) -> None:
        """Override drawBackground to draw grid and axis."""
        if painter is None:
            return

        # Draw background
        painter.fillRect(rect, self.BACKGROUND_COLOR)

        # Draw secondary lines
        painter.setPen(self.SECONDARY_LINE_COLOR)
        for x in range(-self._half_width, self._half_width, 20):
            painter.drawLine(x, -self._half_height, x, self._half_height)
        for y in range(-self._half_height, self._half_height, 20):
            painter.drawLine(-self._half_width, y, self._half_width, y)

        # Draw main lines
        painter.setPen(self.MAIN_LINE_COLOR)
        for x in range(-self._half_width, self._half_width, 100):
            painter.drawLine(x, -self._half_height, x, self._half_height)
        for y in range(-self._half_height, self._half_height, 100):
            painter.drawLine(-self._half_width, y, self._half_width, y)

        # Draw axis lines
        painter.setPen(self.AXIS_COLOR)
        painter.drawLine(0, -self._half_height, 0, self._half_height)
        painter.drawLine(-self._half_width, 0, self._half_width, 0)

    def is_left_or_right_click(self, event: QtGui.QMouseEvent) -> bool:
        """Return True if the event is a left or right click."""
        return event.buttons() == QtCore.Qt.MouseButton.LeftButton or event.buttons() == QtCore.Qt.MouseButton.RightButton

    def mouseMoveEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """Override mouseMoveEvent to handle dragging."""
        if event is None:
            return

        if not self._drag_start and self.is_left_or_right_click(event):
            if self.scene().selectedItems() == [] or event.buttons() == QtCore.Qt.MouseButton.RightButton:
                self._drag_start = True
                if event.buttons() == QtCore.Qt.MouseButton.RightButton:
                    self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
                    self.setInteractive(False)
                else:
                    self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)
                    self.setInteractive(True)

                e = QtGui.QMouseEvent(
                    QtCore.QEvent.Type.MouseButtonPress,
                    event.position(), event.globalPosition(),
                    QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.NoButton,
                    QtCore.Qt.KeyboardModifier.NoModifier
                )
                QtWidgets.QGraphicsView.mousePressEvent(self, e)
        QtWidgets.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """Override mouseReleaseEvent to handle drag end and context menu."""
        if event is None:
            return

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self._drag_start:
                self._drag_start = False
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
                self.setInteractive(True)
            else:
                if self.itemAt(event.position().toPoint()) is None:
                    self.context_menu(event.position().toPoint())
                else:
                    QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
        elif event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self._drag_start:
                self._drag_start = False
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
                self.setInteractive(True)
            else:
                QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)

    def wheelEvent(self, event: QtGui.QWheelEvent | None) -> None:
        """Override wheelEvent to handle zoom."""
        if event is None:
            return

        zoom_delta = 10 if event.angleDelta().y() > 0 else -10

        newzoom = self.zoom + zoom_delta
        if 50 <= newzoom <= 100:
            self.scale(100 / self.zoom, 100 / self.zoom)
            self.zoom = newzoom
            self.scale(self.zoom / 100, self.zoom / 100)

            self.zoom_label.setText(f"{self.zoom}%")

    def context_menu(self, position: QtCore.QPoint) -> None:
        """Show graph context menu."""
        menu = QtWidgets.QMenu(self)
        add_print_action = menu.addAction("Add print")
        add_branch_action = menu.addAction("Add branch")
        action = menu.exec(self.mapToGlobal(position))
        if action == add_print_action:
            node_pos = self.mapToScene(position).toPoint()
            new_print_node = Print(self, node_pos.x(), node_pos.y())
            self.scene().addItem(new_print_node)
        elif action == add_branch_action:
            node_pos = self.mapToScene(position).toPoint()
            new_branch_node = Branch(self, node_pos.x(), node_pos.y())
            self.scene().addItem(new_branch_node)

    def keyPressEvent(self, event: QtGui.QKeyEvent | None) -> None:
        """Override keyPressEvent to handle node deletion."""
        if event is None:
            return

        if event.key() == QtCore.Qt.Key.Key_Delete:
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
        else:
            QtWidgets.QGraphicsView.keyPressEvent(self, event)
