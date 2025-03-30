from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import QTimer, QPointF
from PySide6.QtGui import QPixmap


class ArmyUnit(QGraphicsPixmapItem):
    def __init__(self, start_cell, end_cell, frame_count=6, steps=50, interval=20, scale_factor=0.4):
        super().__init__()

        self.start_cell = start_cell
        self.end_cell = end_cell
        self.arrival_callback = None
        self.frames = []
        self.current_frame = 0

        # Load sprite based on direction
        direction = self._get_direction()
        sprite_path = self._sprite_for_direction(direction)

        sprite_sheet = QPixmap(sprite_path)
        if sprite_sheet.isNull():
            print(f"Failed to load sprite: {sprite_path}")
        else:
            frame_width = sprite_sheet.width() // frame_count
            frame_height = sprite_sheet.height()
            for i in range(frame_count):
                frame = sprite_sheet.copy(i * frame_width, 0, frame_width, frame_height)
                scaled = frame.scaled(frame_width * scale_factor, frame_height * scale_factor)
                self.frames.append(scaled)
            self.setPixmap(self.frames[0])

        self.current_step = 0
        self.total_steps = steps

        base_offset = QPointF(start_cell.size / 2, start_cell.size * 0.85)
        vertical_offset = -8
        self.start_pos = self.start_cell.pos() + base_offset + QPointF(0, vertical_offset)
        self.end_pos = self.end_cell.pos() + base_offset + QPointF(0, vertical_offset)
        self.setPos(self.start_pos)
        self.setZValue(10)

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.update_position)
        self.move_timer.start(interval)

        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_frame)
        self.anim_timer.start(100)

    def _get_direction(self):
        delta = self.end_cell.pos() - self.start_cell.pos()
        if abs(delta.x()) > abs(delta.y()):
            return "right" if delta.x() > 0 else "left"
        else:
            return "down" if delta.y() > 0 else "up"

    def _sprite_for_direction(self, direction):
        return {
            "up":    ":/units/U_Run.png",
            "down":  ":/units/D_Run.png",
            "left":  ":/units/S_Run.png",
            "right": ":/units/SR_Run.png",
        }[direction]

    def update_position(self):
        if self.current_step >= self.total_steps:
            self.move_timer.stop()
            self.anim_timer.stop()
            if self.arrival_callback:
                self.arrival_callback()
            if self.scene():
                self.scene().removeItem(self)
            return

        t = self.current_step / self.total_steps
        new_x = (1 - t) * self.start_pos.x() + t * self.end_pos.x()
        new_y = (1 - t) * self.start_pos.y() + t * self.end_pos.y()
        self.setPos(QPointF(new_x, new_y))
        self.current_step += 1

    def update_frame(self):
        if not self.frames:
            return
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.setPixmap(self.frames[self.current_frame])

