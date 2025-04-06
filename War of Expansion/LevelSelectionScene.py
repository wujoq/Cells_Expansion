from PySide6.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem
from PySide6.QtGui import QFont, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QRectF, Signal, QObject

class LevelSelectorSignal(QObject):
    level_selected = Signal(int)

class LevelSelectionScene(QGraphicsScene):
    def __init__(self, levels=2):
        super().__init__()
        self.signals = LevelSelectorSignal()
        self.setSceneRect(0, 0, 800, 600)

        title = QGraphicsTextItem("Select Level")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setDefaultTextColor(Qt.white)
        title.setPos(300, 50)
        self.addItem(title)

        for i in range(levels):
            self.add_level_button(i + 1, 300, 150 + i * 80)

    def add_level_button(self, level_number, x, y):
        rect = QGraphicsRectItem(QRectF(0, 0, 200, 50))
        rect.setPos(x, y)
        rect.setBrush(QBrush(QColor(60, 130, 200)))
        rect.setPen(QPen(Qt.black))

        # ✅ Fixed this line
        rect.setFlag(QGraphicsItem.ItemIsSelectable)
        rect.setAcceptHoverEvents(True)

        self.addItem(rect)

        text = QGraphicsTextItem(f"Level {level_number}")
        text.setFont(QFont("Arial", 14))
        text.setDefaultTextColor(Qt.white)
        text.setParentItem(rect)
        text.setPos(50, 10)

        # Clicking the rectangle triggers level switch
        rect.mousePressEvent = lambda event, lvl=level_number: self.signals.level_selected.emit(lvl)
