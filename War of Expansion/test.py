import sys
from Event_handler import *
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF, QEvent
from PySide6.QtGui import QBrush, QPen, QColor, QPainter, QMouseEvent


class GameView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)


if __name__ == "__main__":
    app = QApplication([])

    view = GameView(None)
    scene = EventHandler(view, size=30)
    view.show()

    app.exec()