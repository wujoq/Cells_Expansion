from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QApplication
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QFont, QColor, QMouseEvent
from Cell import *
from Connections import *


class EventHandler(QGraphicsScene):
    def __init__(self, view, size: int, parent=None):
        super().__init__(parent)
        self.view = view
        self.size = size
        self.player_color = QColor(0, 0, 255)  # Blue for player
        self.enemy_color = QColor(255, 0, 0)   # Red for enemy
        self.selected_cell = None  # To track the selected cell for making connections

        self.setSceneRect(-500, -500, 1000, 1000)  # Set an arbitrary scene size
        self.view.setScene(self)

    def mousePressEvent(self, event):
        # Right-click to add player cell
        if event.button() == Qt.RightButton:
            self.add_cell(self.player_color, event.scenePos())
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Left double-click to add enemy cell
        if event.button() == Qt.RightButton:
            self.add_cell(self.enemy_color, event.scenePos())
        super().mouseDoubleClickEvent(event)

    def add_cell(self, color: QColor, position: QPointF):
        """Add a cell of the specified color at the given position."""
        cell = Cell(self.size, position, color)
        self.addItem(cell)

    def mouseReleaseEvent(self, event):
        """Handles the cell connection logic after clicking two cells."""
        clicked_cell = self.itemAt(event.scenePos(), self.view.transform())

        if isinstance(clicked_cell, Cell):
            if self.selected_cell:
                # If a cell is selected, create a connection between the two cells
                self.create_connection(self.selected_cell, clicked_cell)
                self.selected_cell.selected = False  # Deselect the previous cell
                self.selected_cell.update()  # Update previous cell to remove the selection indicator
                self.selected_cell = None  # Reset selected cell
            else:
                # Select the clicked cell
                clicked_cell.selected = True
                self.selected_cell = clicked_cell
                clicked_cell.update()  # Update cell to show selection indicator

        super().mouseReleaseEvent(event)