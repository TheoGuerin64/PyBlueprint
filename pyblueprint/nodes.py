from anode import ANode
from PyQt6 import QtGui


class Print(ANode):
    NAME = "Print"
    GRADIENT_COLOR1 = QtGui.QColor(255, 0, 0)
    GRADIENT_COLOR2 = QtGui.QColor(60, 60, 60)


class Branch(ANode):
    NAME = "Branch"
    GRADIENT_COLOR1 = QtGui.QColor(40, 40, 40)
    GRADIENT_COLOR2 = QtGui.QColor(80, 80, 80)
