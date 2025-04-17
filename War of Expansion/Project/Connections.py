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

        self.sending_from_cell1 = False
        self.sending_from_cell2 = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.send_units)
        self.timer.start(self.base_interval)

    def enable_sending_from(self, cell):
        if cell == self.cell1:
            self.sending_from_cell1 = True
        elif cell == self.cell2:
            self.sending_from_cell2 = True

    def stop_all_sending(self):
        self.timer.stop()
        self.sending_from_cell1 = False
        self.sending_from_cell2 = False

    def send_units(self):
        if self.scene() is None:
            return
        if self.sending_from_cell1:
            self._send_unit(self.cell1, self.cell2)
        if self.sending_from_cell2:
            self._send_unit(self.cell2, self.cell1)

    def _send_unit(self, source, target):
        if isinstance(source, GeneratorCell) and target.is_enemy(source.color):
            return
        if source.army <= 0:
            return

        source.army -= 1
        source.update()

        unit = ArmyUnit(source, target)
        unit.source = source  # Restore reference for callback
        unit.target = target
        unit.arrival_callback = lambda: self.on_unit_arrival(unit)
        self.scene().addItem(unit)

    def on_unit_arrival(self, unit):
        sender = unit.source
        target = unit.target

        if target.is_enemy(sender.color):
            target.army -= 1
            if target.army < 0:
                target.army = 1
                scene = target.scene()
                color = sender.color

                if scene:
                    scene.removeItem(target)

                    # Replace the captured cell
                    if color == QColor("red"):
                        new_cell = AttackCell(target.size, target.pos(), QColor("red"),
                                            resource_path=":/towers/attacking_unit_enemy.png")
                    else:
                        target.setColor(color)
                        new_cell = target

                    if hasattr(scene, "cells"):
                        if target in scene.cells:
                            scene.cells.remove(target)
                        scene.cells.append(new_cell)

                    # ✅ REMOVE ALL CONNECTIONS involving captured cell
                    to_remove = []
                    for conn in list(scene.connections_manager.connections):
                        if conn.cell1 == target or conn.cell2 == target:
                            to_remove.append(conn)

                    for conn in to_remove:
                        conn.stop_all_sending()
                        other_cell = conn.cell2 if conn.cell1 == target else conn.cell1
                        if target in other_cell.connections:
                            other_cell.connections.remove(target)
                        if other_cell in target.connections:
                            target.connections.remove(other_cell)
                        if conn in scene.connections_manager.connections:
                            scene.connections_manager.connections.remove(conn)
                        if conn.scene():
                            conn.scene().removeItem(conn)

                    # Reset the captured cell
                    new_cell.connections = []
                    scene.addItem(new_cell)

                    if sender == self.cell1:
                        self.cell2 = new_cell
                    else:
                        self.cell1 = new_cell

                    self.show_capture_effect(new_cell.pos(), color)

            target.update()
        else:
            target.army += 1
            target.update()


    def show_capture_effect(self, pos: QPointF, color: QColor):
        scene = self.scene()
        if scene is None:
            return

        glow = QGraphicsEllipseItem(-30, -30, 60, 60)
        glow.setPos(pos + QPointF(self.cell2.size / 2, self.cell2.size / 2))
        glow.setZValue(20)
        glow.setBrush(QColor(color.red(), color.green(), color.blue(), 120))
        glow.setPen(Qt.NoPen)
        scene.addItem(glow)
        QTimer.singleShot(600, lambda: scene.removeItem(glow))

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

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.delete_connection()
        else:
            super().mousePressEvent(event)

    def delete_connection(self):
        self.stop_all_sending()

        if self.cell2 in self.cell1.connections:
            self.cell1.connections.remove(self.cell2)
        if self.cell1 in self.cell2.connections:
            self.cell2.connections.remove(self.cell1)

        if self.manager and self in self.manager.connections:
            self.manager.connections.remove(self)

        if self.scene():
            self.scene().removeItem(self)
