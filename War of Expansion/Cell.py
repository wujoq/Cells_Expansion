from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QFont

class Cell(QGraphicsItem):
    def __init__(self, size, position, color, connections=None, max_connections=2, cells=0, cells_increase_speed=1):
        super().__init__()

        self.size = size
        self.position = position
        self.connections = connections if connections is not None else []
        self.max_connections = max_connections
        self.cells = cells
        self.cells_increase_speed = cells_increase_speed
        self.color = color

        self.setPos(position)

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget=None):
        brush = QBrush(self.color)
        pen = QPen(Qt.black)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(0, 0, self.size, self.size)
        painter.setFont(QFont("Arial", 10))  
        text_rect = QRectF(0, 0, self.size, self.size)
        text_rect.moveCenter(QPointF(self.size / 2, self.size / 2))
        painter.drawText(text_rect, Qt.AlignCenter, str(self.cells))

    def increase_cells(self):
        self.cells += self.cells_increase_speed