import math
from Cell import *
from Army_unit import *
import resources_rc
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtCore import QRectF, Qt, QPointF, QTimer
from PySide6.QtGui import QBrush, QPen, QColor, QPixmap


class Connection(QGraphicsItem):
    def __init__(self, cell1: Cell, cell2: Cell, manager):
        super().__init__()
        self.cell1 = cell1
        self.cell2 = cell2
        self.manager = manager
        self.setZValue(-1)
        self.base_interval = 2000

        self.sendingTimer = QTimer()
        self.sendingTimer.timeout.connect(self.send_unit)
        self.sendingTimer.start(self.base_interval)

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

        line_vector = end - start
        length = (line_vector.x() ** 2 + line_vector.y() ** 2) ** 0.5
        angle = math.degrees(math.atan2(line_vector.y(), line_vector.x()))
        tile_width = pixmap.width()
        count = int(length // tile_width) + 1

        for i in range(count):
            fraction = i / count
            pos = start + line_vector * fraction
            painter.save()
            painter.translate(pos)
            painter.rotate(angle)
            painter.drawPixmap(-tile_width / 2, -pixmap.height() / 2, pixmap)
            painter.restore()

    def send_unit(self):
        if self.scene() is None:
            return

        if isinstance(self.cell1, GeneratorCell) and self.cell2.is_enemy(self.cell1.color):
            return

        if self.cell1.army <= 0:
            return

        self.cell1.army -= 1
        self.cell1.update()

        unit = ArmyUnit(self.cell1, self.cell2)
        unit.arrival_callback = lambda: self.on_unit_arrival(unit)
        self.scene().addItem(unit)
        self.update_timer_interval()

    def update_timer_interval(self):
        interval = self.base_interval

        if isinstance(self.cell1, GeneratorCell):
            army_factor = max(1.0, math.log(self.cell1.army + 5))
            interval = max(500, int(self.base_interval / army_factor))
        elif isinstance(self.cell1, AttackCell) and self.cell1.army > 50:
            interval = int(self.base_interval / 1.5)

        if self.sendingTimer.interval() != interval:
            self.sendingTimer.setInterval(interval)

    def on_unit_arrival(self, unit):
        if self.cell2.is_enemy(self.cell1.color):
            self.cell2.army -= 1
            if self.cell2.army < 0:
                self.cell2.army = 1
                old_cell = self.cell2
                scene = old_cell.scene()
                color = self.cell1.color

                if scene:
                   
                    scene.removeItem(old_cell)

                    
                    if color == QColor("red"):
                        new_cell = AttackCell(old_cell.size, old_cell.pos(), QColor("red"), resource_path=":/towers/attacking_unit_enemy.png")
                    else:
                        old_cell.setColor(color)
                        new_cell = old_cell

                    
                    if hasattr(scene, "cells"):
                        if old_cell in scene.cells:
                            scene.cells.remove(old_cell)
                        scene.cells.append(new_cell)

                    for conn in list(scene.connections_manager.connections):
                        if conn.cell1 == old_cell:
                            conn.cell1 = new_cell
                        if conn.cell2 == old_cell:
                            conn.cell2 = new_cell

                    new_cell.connections = []
                    scene.addItem(new_cell)
                    self.cell2 = new_cell

                    self.show_capture_effect(new_cell.pos(), color)

            self.cell2.update()
        else:
            self.cell2.army += 1
            self.cell2.update()

    def show_capture_effect(self, pos: QPointF, color: QColor):
        scene = self.cell2.scene()
        if scene is None:
            return

        glow = QGraphicsEllipseItem(-30, -30, 60, 60)
        glow.setPos(pos + QPointF(self.cell2.size / 2, self.cell2.size / 2))
        glow.setZValue(20)
        glow.setBrush(QColor(color.red(), color.green(), color.blue(), 120))
        glow.setPen(Qt.NoPen)
        scene.addItem(glow)
        QTimer.singleShot(600, lambda: scene.removeItem(glow))

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.delete_connection()
        else:
            super().mousePressEvent(event)

    def delete_connection(self):
        self.sendingTimer.stop()

        if self.cell2 in self.cell1.connections:
            self.cell1.connections.remove(self.cell2)
        if self.cell1 in self.cell2.connections:
            self.cell2.connections.remove(self.cell1)

        if self.manager and self in self.manager.connections:
            self.manager.connections.remove(self)

        if self.scene():
            self.scene().removeItem(self)
