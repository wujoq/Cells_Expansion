from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import QTimer, QPointF
from PySide6.QtGui import QPixmap

class ArmyUnit(QGraphicsPixmapItem):
    def __init__(self, start_cell, end_cell, frame_count=6, steps=50, interval=20, scale_factor=0.4):
        super().__init__()
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.color = start_cell.color  
        self.arrival_callback = None
        self.frames = []
        self.current_frame = 0
        self.removed = False  

        self.start_pos = self._center_offset(start_cell)
        self.end_pos = self._center_offset(end_cell)
        direction = self._get_direction(self.start_pos, self.end_pos)

       
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
            self.setOffset(-self.pixmap().width() / 2, -self.pixmap().height() / 2)  

        self.current_step = 0
        self.total_steps = steps
        self.setPos(self.start_pos)
        self.setZValue(10)

       
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.update_position)
        self.move_timer.start(interval)

        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_frame)
        self.anim_timer.start(100)

    def _center_offset(self, cell):
        return cell.pos() + QPointF(cell.size / 2, cell.size * 0.85)  

    def _get_direction(self, start, end):
        delta = end - start
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
            if self.scene() and not self.removed:
                self.scene().removeItem(self)
                self.removed = True
            return

    
        t = self.current_step / self.total_steps
        new_x = (1 - t) * self.start_pos.x() + t * self.end_pos.x()
        new_y = (1 - t) * self.start_pos.y() + t * self.end_pos.y()
        self.setPos(QPointF(new_x, new_y))
        self.current_step += 1

       
        self.check_for_clashes()

    def update_frame(self):
        if not self.frames:
            return
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.setPixmap(self.frames[self.current_frame])
        self.setOffset(-self.pixmap().width() / 2, -self.pixmap().height() / 2) 

    def check_for_clashes(self):
        if not self.scene() or self.removed:
            return

        for item in self.scene().items():
            if isinstance(item, ArmyUnit) and item is not self:
                if item.color != self.color and not getattr(item, "removed", False):
                    distance = (self.scenePos() - item.scenePos()).manhattanLength()
                    if distance < 15:
                        self.removed = True
                        item.removed = True
                        if self.scene():
                            self.scene().removeItem(self)
                        if item.scene():
                            item.scene().removeItem(item)
                        return
