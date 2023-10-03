from typing import TYPE_CHECKING

from PyQt6 import QtCore, QtGui, QtWidgets

from agraph_item import AGraphItem

if TYPE_CHECKING:
    from graph import Graph


class SelectionGroup(QtWidgets.QGraphicsItemGroup, AGraphItem):
    """A group of selected nodes."""

    def __init__(self, graph: "Graph") -> None:
        super(QtWidgets.QGraphicsItemGroup, self).__init__(graph, 0, 0)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def scene(self) -> QtWidgets.QGraphicsScene:
        """Override scene to return a typed scene."""
        scene = super().scene()
        assert scene is not None
        return scene

    def clear(self) -> None:
        """Clears the group."""
        for item in self.childItems():
            item.setGroup(None)
            item.setSelected(False)

    def delete(self) -> None:
        """Deletes the group."""
        for item in self.childItems():
            item.setGroup(None)
            self.scene().removeItem(item)

    def paint(self, painter: QtGui.QPainter | None, option: QtWidgets.QStyleOptionGraphicsItem | None, widget: QtWidgets.QWidget | None = None) -> None:
        """Override paint to draw a rectangle around the group."""
        assert painter is not None
        painter.drawRect(self.boundingRect())

    def context_menu(self, pos: QtCore.QPoint) -> None:
        """Shows the context menu of the node."""
        self.setSelected(True)

        menu = QtWidgets.QMenu(self.graph)
        destroy_action = menu.addAction("Destroy")
        action = menu.exec(pos)
        if action == destroy_action:
            self.delete()
