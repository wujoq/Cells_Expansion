from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QFont, QColor, QMouseEvent

class Cell(QGraphicsItem):
    def __init__(self, size:int, position:QPointF, color:QColor):
        super().__init__()

        self.size = size
        self.position = position
        self.color = color
        self.connections = []  # Store connections for the cell
        self.selected = False  # New flag to track selection state

        self.setPos(position)

    def boundingRect(self):
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget=None):
        # Paint the cell itself
        brush = QBrush(self.color)
        pen = QPen(Qt.black)

        # If the cell is selected, use a thicker border (indicator)
        if self.selected:
            pen.setWidth(3)  # Thicker border for selected cell
            pen.setColor(QColor(0, 255, 0))  # Green color for selection indicator
        else:
            pen.setWidth(1)  # Default border width

        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(0, 0, self.size, self.size)

        # Draw the cell's label (optional)
        painter.setFont(QFont("Arial", 10))  
        text_rect = QRectF(0, 0, self.size, self.size)
        text_rect.moveCenter(QPointF(self.size / 2, self.size / 2))
        painter.drawText(text_rect, Qt.AlignCenter, "Cell")

    def mousePressEvent(self, event: QMouseEvent):
        event.accept()
        return super().mousePressEvent(event)