import sys
import resources_rc
from Event_handler import EventHandler
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QBrush, QPen, QColor, QPixmap

# Definicja klikalnego elementu menu.
class MenuItem(QGraphicsTextItem):
    def __init__(self, text: str, unit_type: str, scene, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.unit_type = unit_type
        self.scene = scene
        self.setDefaultTextColor(QColor("white"))
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def mousePressEvent(self, event):
        # Ustawienie wybranego typu jednostki w scenie.
        self.scene.selected_unit_type = self.unit_type
        self.setDefaultTextColor(QColor("green"))
        # Resetowanie koloru pozostałych elementów menu.
        for item in self.scene.menu_items:
            if item is not self:
                item.setDefaultTextColor(QColor("white"))
        event.accept()

class GameScene(EventHandler):
    def __init__(self):
        # Ustawiamy scenę na 800x800 i rozmiar jednostek na 100
        super().__init__(size=100)
        self.setSceneRect(0, 0, 800, 800)
        self.initBackground()
        self.initMenu()

    def initBackground(self):
        # Używamy powtarzającego się tła (tiling)
        pixmap = QPixmap(":/tiles/FieldsTile_38.png")
        if pixmap.isNull():
            print("Failed to load background image!")
            return
        brush = QBrush(pixmap)
        bg_rect = QGraphicsRectItem(self.sceneRect())
        bg_rect.setBrush(brush)
        bg_rect.setPen(Qt.NoPen)
        bg_rect.setZValue(-5)
        self.addItem(bg_rect)
        
    def initMenu(self):
        # Ustawiamy menu na dole sceny
        menu_height = self.menu_area_height  # np. 100 pikseli
        menu_rect = QGraphicsRectItem(0, self.sceneRect().height() - menu_height, self.sceneRect().width(), menu_height)
        menu_rect.setBrush(QBrush(QColor(50, 50, 50, 200)))  # Szary, półprzezroczysty
        menu_rect.setPen(QPen(Qt.NoPen))
        menu_rect.setZValue(1)
        self.addItem(menu_rect)

        self.menu_items = []
        spacing = 10
        # Pozycjonujemy elementy menu w poziomie
        start_x = spacing
        menu_y = self.sceneRect().height() - menu_height + spacing

        # Wskaźnik złota – przykładowy
        gold_item = QGraphicsTextItem("Gold: 100")
        gold_item.setDefaultTextColor(QColor("yellow"))
        gold_item.setPos(start_x, menu_y)
        gold_item.setZValue(2)
        self.addItem(gold_item)
        start_x += gold_item.boundingRect().width() + spacing

        # Klikalne elementy menu – wybór jednostek
        attack_item = MenuItem("Attacking Tower", "attacking", self)
        attack_item.setPos(start_x, menu_y)
        attack_item.setZValue(2)
        self.addItem(attack_item)
        self.menu_items.append(attack_item)
        start_x += attack_item.boundingRect().width() + spacing

        generating_item = MenuItem("Generating Tower", "generating", self)
        generating_item.setPos(start_x, menu_y)
        generating_item.setZValue(2)
        self.addItem(generating_item)
        self.menu_items.append(generating_item)
        start_x += generating_item.boundingRect().width() + spacing

        supporting_item = MenuItem("Supporting Tower", "supporting", self)
        supporting_item.setPos(start_x, menu_y)
        supporting_item.setZValue(2)
        self.addItem(supporting_item)
        self.menu_items.append(supporting_item)

        self.selected_unit_type = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = GameScene()
    view = QGraphicsView(scene)
    view.setWindowTitle("Game Scene")
    view.setFixedSize(800, 800)
    view.show()
    sys.exit(app.exec())
