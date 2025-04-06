from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsTextItem, QGraphicsItemGroup
from PySide6.QtGui import QPixmap, QFont, QColor, QPen, QBrush
from PySide6.QtCore import QRectF, Qt

class TowerSelector:
    def __init__(self, scene):
        self.scene = scene
        self.options = []

    def show(self, spot):
        self.clear()  # Remove old options

        labels = [
            ("Attacking", "attacking", ":/towers/attacking_unit.png", 6),
            ("Generating", "generating", ":/towers/generating_unit.png", 6),
            ("Supporting", "supporting", ":/towers/support_unit.png", 4)
        ]

        spacing = 10
        box_size = 50
        start_x = spot.x() - ((box_size + spacing) * len(labels) - spacing) / 2
        y = spot.y() - 80

        for i, (text, unit_type, icon_path, frame_count) in enumerate(labels):
            x = start_x + i * (box_size + spacing)
            group = QGraphicsItemGroup()

            # Background rectangle
            rect = QGraphicsRectItem(0, 0, box_size, box_size)
            rect.setBrush(QColor(80, 80, 160))
            rect.setPen(QPen(Qt.white, 1))
            rect.setZValue(10)
            rect.setAcceptHoverEvents(True)

            def make_hover_handlers(r):
                def hover_enter(event):
                    r.setBrush(QColor(120, 120, 200))

                def hover_leave(event):
                    r.setBrush(QColor(80, 80, 160))

                return hover_enter, hover_leave

            enter, leave = make_hover_handlers(rect)
            rect.hoverEnterEvent = enter
            rect.hoverLeaveEvent = leave

            # Icon (cropping sprite based on the number of frames)
            sprite_sheet = QPixmap(icon_path)
            if icon_path == ":/towers/attacking_unit.png" or icon_path == ":/towers/generating_unit.png":
                icon = sprite_sheet.copy(0, 0, sprite_sheet.width() // frame_count, sprite_sheet.height())
            elif icon_path == ":/towers/support_unit.png":
                icon = sprite_sheet.copy(0, 0, sprite_sheet.width() // frame_count, sprite_sheet.height())

            icon = icon.scaled(box_size - 8, box_size - 8, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_item = QGraphicsPixmapItem(icon)
            icon_item.setPos(4, 4)
            icon_item.setZValue(11)

            # Label (below box)
            label = QGraphicsTextItem(text)
            label.setFont(QFont("Arial", 8))
            label.setDefaultTextColor(Qt.white)
            label.setPos(0, box_size + 2)
            label.setTextWidth(box_size)
            label.setZValue(11)
            label.setTextInteractionFlags(Qt.NoTextInteraction)

            # Grouping
            group.addToGroup(rect)
            group.addToGroup(icon_item)
            group.addToGroup(label)
            group.setPos(x, y)
            group.setFlag(QGraphicsItemGroup.ItemIsSelectable)
            group.setData(0, (spot, unit_type))
            group.mousePressEvent = self._make_placement_handler(group)

            self.scene.addItem(group)
            self.options.append(group)

    def _make_placement_handler(self, item):
        def handler(event):
            spot, unit_type = item.data(0)
            self.scene.place_tower(spot, unit_type)
            spot.mark_used()
            self.clear()
            event.accept()
        return handler

    def clear(self):
        for opt in self.options:
            self.scene.removeItem(opt)
        self.options.clear()
