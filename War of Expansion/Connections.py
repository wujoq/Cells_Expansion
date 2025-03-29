from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QFont, QColor

class Connection(QGraphicsItem):
    def __init__(self, cell1, cell2):
        super().__init__()
        self.cell1 = cell1
        self.cell2 = cell2
        self.setZValue(-1)  # Ensure connections are drawn beneath the cells

    def boundingRect(self):
        return QRectF(self.cell1.x(), self.cell1.y(), self.cell2.x() - self.cell1.x(), self.cell2.y() - self.cell1.y())

    def paint(self, painter, option, widget=None):
        pen = QPen(QColor(0, 0, 0))  # black color for the connection line
        pen.setWidth(2)
        painter.setPen(pen)

        # Draw a line between the center of the two cells
        painter.drawLine(self.cell1.x() + self.cell1.size / 2, self.cell1.y() + self.cell1.size / 2,
                         self.cell2.x() + self.cell2.size / 2, self.cell2.y() + self.cell2.size / 2)
