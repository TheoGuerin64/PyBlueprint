from abc import abstractmethod
from typing import TYPE_CHECKING

from PyQt6 import QtCore, QtWidgets

from utils import ABCQtMeta

if TYPE_CHECKING:
    from graph import Graph


class AGraphItem(QtWidgets.QGraphicsItem, metaclass=ABCQtMeta):
    def __init__(self, graph: "Graph", x: int, y: int) -> None:
        super().__init__()
        self.graph = graph
        self._drag_start = False
        self._drag_start_pos = QtCore.QPointF()

        self.setPos(self._stick_to_grid(QtCore.QPoint(x, y)))

    def scene(self) -> QtWidgets.QGraphicsScene:
        """Override scene to return a typed scene."""
        scene = super().scene()
        assert scene is not None
        return scene

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent | None) -> None:
        """Override mousePressEvent to handle dragging."""
        assert event is not None
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

            self._drag_start = True
            self._drag_start_pos = self._stick_to_grid(event.pos().toPoint())

            QtWidgets.QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent | None) -> None:
        """Override mouseMoveEvent to handle dragging."""
        assert event is not None
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self._drag_start:
                self.setPos(self._stick_to_grid(event.scenePos().toPoint()) - self._drag_start_pos)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent | None) -> None:
        """Override mouseReleaseEvent to handle dragging."""
        assert event is not None
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_start = False
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.setSelected(True)
            self.context_menu(event.screenPos())

    def _stick_to_grid(self, point: QtCore.QPoint) -> QtCore.QPointF:
        """Sticks a point to the grid."""
        return QtCore.QPointF(
            point.x() - point.x() % 20,
            point.y() - point.y() % 20
        )

    @abstractmethod
    def context_menu(self, pos: QtCore.QPoint) -> None:
        """Shows the context menu of the node."""
        pass
