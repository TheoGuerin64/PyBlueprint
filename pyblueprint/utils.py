"""Utilities for pyblueprint"""

from abc import ABCMeta
from PyQt6 import sip


class ABCQtMeta(sip.wrappertype, ABCMeta):
    """Metaclass for abstract classes using PyQt6."""
    pass
