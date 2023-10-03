"""This module contains the nodes that are used in the blueprint."""

from PyQt6 import QtGui

from anode import ANode


class Print(ANode):
    NAME = "Print"
    GRADIENT_COLOR1 = QtGui.QColor(255, 0, 0)
    GRADIENT_COLOR2 = QtGui.QColor(60, 60, 60)

    def execute(self) -> None:
        pass


class Branch(ANode):
    NAME = "Branch"
    GRADIENT_COLOR1 = QtGui.QColor(40, 40, 40)
    GRADIENT_COLOR2 = QtGui.QColor(80, 80, 80)

    def execute(self) -> None:
        pass
