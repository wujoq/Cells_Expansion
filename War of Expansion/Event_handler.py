from PySide6.QtWidgets import QGraphicsScene, QGraphicsLineItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QFont, QColor, QMouseEvent, QTransform
from Cell import AttackCell, GeneratorCell, SupportCell, Cell
from Connections_manager import ConnectionsManager
from Connections import Connection  
from Army_unit import ArmyUnit  # at the top of the file




class EventHandler(QGraphicsScene):
    def __init__(self, view=None, size: int = 100, parent=None):
        super().__init__(parent)
        self.view = view
        self.size = size
        self.selected_unit_type = None  # Typ jednostki z menu (np. "attacking", "generating", "supporting")
        self.setSceneRect(0, 0, 800, 800)
        if self.view is not None:
            self.view.setScene(self)

        # Wysokość obszaru menu (umieszczonego na dole)
        self.menu_area_height = 100

        # Menedżer połączeń
        self.connections_manager = ConnectionsManager()

        # Atrybuty dla tworzenia połączeń metodą drag-and-drop
        self.connection_start_cell = None
        self.connection_preview = None

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.scenePos()
        # Jeśli kliknięto w obszarze menu (na dole), przekazujemy zdarzenie dalej
        if pos.y() > (self.sceneRect().height() - self.menu_area_height):
            super().mousePressEvent(event)
            return

        # Jeśli wybrano typ jednostki, wstawiamy nową komórkę – to ma pierwszeństwo
        if self.selected_unit_type is not None:
            self.add_cell(QColor("blue"), pos)
            event.accept()
            return

        # Jeśli nie wybrano jednostki, sprawdzamy, czy kliknięto na komórce (lewy przycisk) – rozpoczynamy tworzenie połączenia
        if event.button() == Qt.LeftButton:
            clicked_item = self.itemAt(pos, self.view.transform() if self.view else QTransform())
            if isinstance(clicked_item, Cell):
                self.connection_start_cell = clicked_item
                # Tworzymy tymczasowy podgląd linii, ustawiając flagę, aby nie reagował na zdarzenia myszy
                self.connection_preview = QGraphicsLineItem()
                self.connection_preview.setAcceptedMouseButtons(Qt.NoButton)
                pen = QPen(QColor(0, 0, 0, 150))
                pen.setWidth(2)
                self.connection_preview.setPen(pen)
                start = QPointF(clicked_item.x() + clicked_item.size / 2, 
                                clicked_item.y() + clicked_item.size / 2)
                self.connection_preview.setLine(start.x(), start.y(), pos.x(), pos.y())
                self.addItem(self.connection_preview)
                event.accept()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        # Aktualizujemy podgląd linii, jeśli trwa przeciąganie połączenia
        if self.connection_start_cell and self.connection_preview:
            start = QPointF(self.connection_start_cell.x() + self.connection_start_cell.size / 2,
                            self.connection_start_cell.y() + self.connection_start_cell.size / 2)
            pos = event.scenePos()
            self.connection_preview.setLine(start.x(), start.y(), pos.x(), pos.y())
            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        pos = event.scenePos()
        # Jeśli kliknięcie nastąpiło w obszarze menu, usuwamy ewentualny podgląd i resetujemy zmienne
        if pos.y() > (self.sceneRect().height() - self.menu_area_height):
            if self.connection_preview:
                self.removeItem(self.connection_preview)
                self.connection_preview = None
            self.connection_start_cell = None
            super().mouseReleaseEvent(event)
            return

        # Jeśli zwalniamy lewy przycisk po rozpoczęciu przeciągania
        if self.connection_start_cell and event.button() == Qt.LeftButton:
            # Najpierw usuwamy podgląd, aby nie przeszkadzał przy wykrywaniu celu
            if self.connection_preview:
                self.removeItem(self.connection_preview)
                self.connection_preview = None

            target_item = self.itemAt(pos, self.view.transform() if self.view else QTransform())
            if isinstance(target_item, Cell) and target_item is not self.connection_start_cell:
                self.connections_manager.add_connection(self.connection_start_cell, target_item, self)
            self.connection_start_cell = None
            event.accept()
            
            return

        super().mouseReleaseEvent(event)

    def add_cell(self, color: QColor, position: QPointF):
        """Dodaje komórkę (tower) wybranego typu w zadanej pozycji."""
        
        unit_type = self.selected_unit_type
        if unit_type == "attacking":
            cell = AttackCell(self.size, position, color)
        elif unit_type == "generating":
            cell = GeneratorCell(self.size, position, color)
        elif unit_type == "supporting":
            cell = SupportCell(self.size, position, color)
        else:
            return
        self.addItem(cell)
        # Po dodaniu jednostki resetujemy wybrany typ
        self.selected_unit_type = None
