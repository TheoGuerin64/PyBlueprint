from typing import TYPE_CHECKING

from PyQt6 import QtCore, QtGui, QtWidgets

if TYPE_CHECKING:
    from graph import Graph


class ANode(QtWidgets.QGraphicsObject):
    """A parent abstract class for nodes."""
    _TOP_SIZE = 25

    NAME: str = "Node"
    GRADIENT_COLOR1: QtGui.QColor = QtGui.QColor(0, 0, 0)
    GRADIENT_COLOR2: QtGui.QColor = QtGui.QColor(0, 0, 0)
    def __init__(self, graph: "Graph", x: int, y: int):
        super().__init__()
        self.graph = graph
        self._dragStart = False
        self._dragStartPos = QtCore.QPoint()

        self.setPos(self._stick_to_grid(QtCore.QPoint(x, y)))
        self.setAcceptHoverEvents(True)
        self.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.gradient = QtGui.QLinearGradient(0, 0, self.boundingRect().width(), 0)
        self.gradient.setColorAt(0.0, self.GRADIENT_COLOR1)
        self.gradient.setColorAt(1.0, self.GRADIENT_COLOR2)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget = None) -> None:
        """Paints the node on the graphics scene."""
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        x = round(self.boundingRect().x()) + 1
        y = round(self.boundingRect().y()) + 1
        w = round(self.boundingRect().width()) - 2
        h = round(self.boundingRect().height()) - 2

        # draw bot background
        path = QtGui.QPainterPath()
        path.addRoundedRect(x, y, w, h, 10.0, 10.0)

        painter.setOpacity(0.6)
        painter.fillPath(path, QtGui.QColor(0, 0, 0))

        # draw top background
        full_path = QtGui.QPainterPath()
        full_path.addRoundedRect(x, y, w, h, 10.0, 10.0)

        substract_path = QtGui.QPainterPath()
        substract_path.addRect(x, y + self._TOP_SIZE, w, h - self._TOP_SIZE)

        path = full_path.subtracted(substract_path)

        painter.setOpacity(1)
        painter.fillPath(path, self.gradient)

        # Draw the node name
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        painter.setFont(QtGui.QFont("Segoe UI", 14))
        painter.drawText(
            round(self.boundingRect().x()) + 5,
            round(self.boundingRect().y()) + 20,
            self.NAME
        )

        # draw selected border
        if self.isSelected():
            border_path = QtGui.QPainterPath()
            border_path.addRoundedRect(x - 1, y - 1, w + 2, h + 2, 10.0, 10.0)

            painter.setOpacity(1)
            painter.setPen(QtGui.QColor(241, 176, 0))
            painter.drawPath(border_path)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(2, 2, 150, 100)

    def hoverEnterEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)

    def hoverLeaveEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        """Override mousePressEvent to handle dragging."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_start = True
            self._drag_start_pos = self._stick_to_grid(event.pos().toPoint())

            # TODO: make it in top of the scene

            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
            QtWidgets.QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        """Override mouseMoveEvent to handle dragging."""
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self._drag_start:
                self.setPos(self._stick_to_grid(event.scenePos().toPoint()) - self._drag_start_pos)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        """Override mouseReleaseEvent to handle dragging."""
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_start = False
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            for item in self.graph.items():
                item.setSelected(False)
            self.setSelected(True)
            self.context_menu(event.screenPos())

    def context_menu(self, pos: QtCore.QPoint) -> None:
        """Shows the context menu of the node."""
        self.setSelected(True)

        menu = QtWidgets.QMenu(self.graph)
        destroy_action = menu.addAction("Destroy")
        action = menu.exec(pos)
        if action == destroy_action:
            self.graph.scene().removeItem(self)

    def _stick_to_grid(self, point: QtCore.QPoint) -> QtCore.QPointF:
        """Sticks a point to the grid."""
        return QtCore.QPointF(
            point.x() - point.x() % 20,
            point.y() - point.y() % 20
        )
