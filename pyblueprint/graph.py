from typing import TYPE_CHECKING

from PyQt6 import QtCore, QtGui, QtWidgets

from .nodes import Branch, Print
from .selection_group import SelectionGroup

if TYPE_CHECKING:
    from .anode import ANode


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
        self._single_click = False
        self.last_selected: "ANode" | None = None
        self.zoom = 100

        self.init_ui()

        self._half_width = round(self.sceneRect().width() / 2)
        self._half_height = round(self.sceneRect().height() / 2)

        self.selected = SelectionGroup(self)
        self.scene().addItem(self.selected)

    def scene(self) -> QtWidgets.QGraphicsScene:
        """Override scene to return a typed scene."""
        scene = super().scene()
        assert scene is not None
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
        assert painter is not None

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

    def leftOrRightClick(self, event: QtGui.QMouseEvent) -> bool:
        """Check if the event is a left or right click."""
        return (event.buttons() == QtCore.Qt.MouseButton.LeftButton
                or event.buttons() == QtCore.Qt.MouseButton.RightButton)

    def itemsAtEventAreSelected(self, event: QtGui.QMouseEvent) -> bool:
        """Check if the items at the event are selected."""
        return self.itemAt(event.position().toPoint()) in self.selected.childItems()

    def mousePressEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """Override mousePressEvent to handle dragging."""
        assert event is not None
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            item = self.itemAt(event.position().toPoint())
            if item is not None:
                if self.last_selected is not None and self.last_selected.isSelected():
                    self.last_selected.setGroup(self.selected)
                if item.group() is not None:
                    item.setGroup(None)
                    item.setSelected(False)
                elif item != self.selected:
                    item.setGroup(self.selected)
                    item.setSelected(True)
            self._single_click = True
        elif self.leftOrRightClick(event) and not self.itemsAtEventAreSelected(event):
            self.selected.clear()
        QtWidgets.QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """Override mouseMoveEvent to handle dragging."""
        assert event is not None
        if not self._single_click and not self._drag_start and self.leftOrRightClick(event):
            self._drag_start = True

            if event.buttons() == QtCore.Qt.MouseButton.RightButton or self.itemAt(event.position().toPoint()) is None:
                if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                    self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)
                    self.setInteractive(True)
                else:
                    self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
                    self.setInteractive(False)

                left_click_event = QtGui.QMouseEvent(
                    QtCore.QEvent.Type.MouseButtonPress,
                    event.position(), event.globalPosition(),
                    QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.NoButton,
                    QtCore.Qt.KeyboardModifier.NoModifier
                )
                QtWidgets.QGraphicsView.mousePressEvent(self, left_click_event)
        QtWidgets.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent | None) -> None:
        """Override mouseReleaseEvent to handle drag end and context menu."""
        assert event is not None
        if self._single_click:
            self._single_click = False
        elif self._drag_start:
            if self.dragMode() == QtWidgets.QGraphicsView.DragMode.RubberBandDrag:
                self.selected.clear()
                for item in self.scene().selectedItems():
                    item.setGroup(self.selected)
                    item.setSelected(True)

            self._drag_start = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self.setInteractive(True)
        elif event.button() == QtCore.Qt.MouseButton.LeftButton:
            QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.itemAt(event.position().toPoint()) is None:
                self.context_menu(event.position().toPoint())
            else:
                QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)

    def wheelEvent(self, event: QtGui.QWheelEvent | None) -> None:
        """Override wheelEvent to handle zoom."""
        assert event is not None
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
        assert event is not None
        if event.key() == QtCore.Qt.Key.Key_Delete:
            if self.selected.childItems() != []:
                self.selected.delete()
            else:
                for item in self.scene().selectedItems():
                    self.scene().removeItem(item)
        else:
            QtWidgets.QGraphicsView.keyPressEvent(self, event)
