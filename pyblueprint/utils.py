from abc import ABCMeta

from PyQt6 import sip


class ABCQtMeta(sip.wrappertype, ABCMeta):
    pass
