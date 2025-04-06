from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt

class BuildSpot(QGraphicsPixmapItem):
    def __init__(self, position, size, game_scene):
        super().__init__()
        self.setPixmap(QPixmap(":/towers/1.png").scaled(size, size))
        self.setOffset(-size / 2, -size / 2)  
        self.setPos(position)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setZValue(2)
        self.game_scene = game_scene
        self.used = False

    def mousePressEvent(self, event):
        if self.used:
            return
        self.game_scene.show_tower_selector(self)
        event.accept()

    def mark_used(self):
        self.used = True
        self.game_scene.removeItem(self)
