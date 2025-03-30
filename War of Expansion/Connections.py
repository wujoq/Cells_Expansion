import math
from Cell import *
from Army_unit import *
import resources_rc
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF, QTimer
from PySide6.QtGui import QBrush, QPen, QColor, QPixmap

class Connection(QGraphicsItem):
    def __init__(self, cell1: Cell, cell2: Cell):
        super().__init__()
        self.cell1 = cell1
        self.cell2 = cell2
        self.setZValue(-1)  # Rysujemy pod komórkami
        self.sendingTimer = QTimer()
        self.sendingTimer.timeout.connect(self.send_unit)
        self.sendingTimer.start(2000)

    def boundingRect(self):
        x1 = self.cell1.x() + self.cell1.size / 2
        y1 = self.cell1.y() + self.cell1.size * 0.85
        x2 = self.cell2.x() + self.cell2.size / 2
        y2 = self.cell2.y() + self.cell2.size * 0.85
        return QRectF(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)).adjusted(-20, -20, 20, 20)


    def paint(self, painter, option, widget=None):
        pixmap = QPixmap(":/tiles/FieldsTile_01.png")
        if pixmap.isNull():
            return

        start = self.cell1.pos() + QPointF(self.cell1.size / 2, self.cell1.size * 0.85)
        end = self.cell2.pos() + QPointF(self.cell2.size / 2, self.cell2.size * 0.85)

        # Vector from start to end
        line_vector = end - start
        length = (line_vector.x() ** 2 + line_vector.y() ** 2) ** 0.5
        angle = math.degrees(math.atan2(line_vector.y(), line_vector.x()))
        tile_width = pixmap.width()

        # Number of full tiles needed
        count = int(length // tile_width) + 1

        for i in range(count):
            fraction = i / count
            pos = start + line_vector * fraction
            painter.save()
            painter.translate(pos)
            painter.rotate(angle)

            # Center tile vertically on path
            x_offset = -tile_width / 2
            y_offset = -pixmap.height() / 2
            painter.drawPixmap(x_offset, y_offset, pixmap)

            painter.restore()

        
    def send_unit(self):
        if self.cell1.army <= 0:
            return

        self.cell1.army -= 1
        self.cell1.update()  # To reflect new army count visually

        unit = ArmyUnit(self.cell1, self.cell2)
        unit.arrival_callback = lambda: self.on_unit_arrival(unit)
        self.scene().addItem(unit)


    def on_unit_arrival(self, unit):
        self.cell2.army += 1
        self.cell2.update()
        