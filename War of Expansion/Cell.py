from PySide6.QtCore import Qt, QTimer, QPointF, QRectF, QLineF
from PySide6.QtGui import QBrush, QPen, QColor, QFont, QPixmap, QPainterPath
from PySide6.QtWidgets import QGraphicsItem
import math

class Cell(QGraphicsItem):
    def __init__(self, size: int, position: QPointF, color: QColor):
        super().__init__()

        self.army = 10
        self.price = 25
        self.size = size
        self.position = position
        self.color = color
        self.connections = []  
        self.selected = False  
        self.setPos(position)

        self.increasearmyTimer = QTimer()
        self.increasearmyTimer.timeout.connect(self.increaseArmy)
        self.increasearmyTimer.start(1500)
    
    def setColor(self, new_color: QColor):
        self.color = new_color
        self.update()


    def is_enemy(self, color):
        self.isenemy = False
        if self.color != color:
            self.isenemy = True
        return self.isenemy

    def shape(self):
        path = QPainterPath()
        
        path.addEllipse(0, 0, self.size, self.size)
        return path

    def boundingRect(self):
       
        return QRectF(0, -20, self.size, self.size + 20)

    def paint(self, painter, option, widget=None):
        
        brush = QBrush(self.color)
        pen = QPen(Qt.black)
        if self.selected:
            pen.setWidth(3)
            pen.setColor(QColor(0, 255, 0))
        else:
            pen.setWidth(1)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(0, 0, self.size, self.size)

        
        painter.setFont(QFont("Arial", 10))
        text_rect = QRectF(0, 0, self.size, self.size)
        text_rect.moveCenter(QPointF(self.size / 2, self.size / 2))
        painter.drawText(text_rect, Qt.AlignCenter, "Cell")

    def increaseArmy(self):
        self.army += 1
        
        self.update(0, -20, self.size, self.size + 20)


class AnimatedCell(Cell):
    def __init__(self, size: int, position: QPointF, color: QColor, resource_path: str, frame_count: int = 6):
        super().__init__(size, position, color)
        self.sprite_sheet = QPixmap(resource_path)
        self.frame_count = frame_count
        self.current_frame = 0
        self.frames = []

        if not self.sprite_sheet.isNull():
            frame_width = self.sprite_sheet.width() / frame_count
            frame_height = self.sprite_sheet.height()
            for i in range(frame_count):
                frame = self.sprite_sheet.copy(i * frame_width, 0, frame_width, frame_height)
                scaled_frame = frame.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.frames.append(scaled_frame)
        else:
            print("Failed to load sprite:", resource_path)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(150)
        
    def boundingRect(self):
        
        return QRectF(0, -20, self.size, self.size + 20)

    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % self.frame_count
        
        self.update(0, -20, self.size, self.size + 20)

    def paint(self, painter, option, widget=None):
        
        if self.frames:
            pixmap = self.frames[self.current_frame]
            x_offset = (self.size - pixmap.width()) / 2
            y_offset = (self.size - pixmap.height()) / 2
            painter.drawPixmap(x_offset, y_offset, pixmap)
        else:
            super().paint(painter, option, widget)
      
        painter.setFont(QFont("Arial", 10))
        army_rect = QRectF(0, -20, self.size, 20)
        painter.drawText(army_rect, Qt.AlignCenter, str(self.army))


class AttackCell(AnimatedCell):
    def __init__(self, size: int, position: QPointF, color: QColor, resource_path: str = None):
        if resource_path is None:
            resource_path = ":/towers/attacking_unit.png"
        super().__init__(size, position, color, resource_path)
        self.boosted = False

    def setBoosted(self, status: bool):
        self.boosted = status

    def attack(self):
        attack_strength = 4 if self.boosted else 2
        self.boosted = False

    def setColor(self, new_color: QColor):
        self.color = new_color
        resource_path = ":/towers/attacking_unit.png"
        self.sprite_sheet = QPixmap(resource_path)
        self.frames.clear()

        if not self.sprite_sheet.isNull():
            frame_width = self.sprite_sheet.width() // self.frame_count
            frame_height = self.sprite_sheet.height()
            for i in range(self.frame_count):
                frame = self.sprite_sheet.copy(i * frame_width, 0, frame_width, frame_height)
                scaled = frame.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.frames.append(scaled)

        self.current_frame = 0
        self.update(0, -20, self.size, self.size + 20)

    def paint(self, painter, option, widget=None):
       
        if self.frames:
            pixmap = self.frames[self.current_frame]
            x_offset = (self.size - pixmap.width()) / 2
            y_offset = (self.size - pixmap.height()) / 2
            painter.drawPixmap(x_offset, y_offset, pixmap)
        else:
            super().paint(painter, option, widget)

        
        painter.setFont(QFont("Arial", 10))
        army_rect = QRectF(0, -20, self.size, 20)


        if self.army > 50:
            painter.setPen(QColor(0, 120, 255))  
        else:
            painter.setPen(Qt.black)

        painter.drawText(army_rect, Qt.AlignCenter, str(self.army))

class SupportCell(AnimatedCell):
    def __init__(self, size: int, position: QPointF, color: QColor, frame_count: int = 4, resource_path: str = None):
        if resource_path is None:
            resource_path = ":/towers/support_unit.png"
        super().__init__(size, position, color, resource_path, frame_count)
        self.price = 30
        self.radius = 100 

        self.boost_timer = QTimer()
        self.boost_timer.timeout.connect(self.apply_boost)
        self.boost_timer.start(1000)

    def boundingRect(self):
       
        return QRectF(-self.radius + self.size / 2, -self.radius + self.size / 2,
                      self.radius * 2, self.radius * 2 + 20)  
    def shape(self):
        path = QPainterPath()
        radius = self.size * 0.8  
        offset = (self.size - radius) / 2
        path.addEllipse(offset, offset, radius, radius)
        return path

    def apply_boost(self):
        if not self.scene():
            return


    def paint(self, painter, option, widget=None):
        
        super().paint(painter, option, widget)
         
        painter.setPen(QPen(QColor(0, 255, 255, 100), 1, Qt.DashLine))
        painter.setBrush(QBrush(QColor(0, 255, 255, 40)))  
        center = QPointF(self.size / 2, self.size / 2)
        painter.drawEllipse(center, self.radius, self.radius)

class GeneratorCell(AnimatedCell):
    def __init__(self, size: int, position: QPointF, color: QColor, resource_path: str = None):
        if resource_path is None:
            resource_path = ":/towers/generating_unit.png"
        super().__init__(size, position, color, resource_path)
        self.boosted = False

        self.increasearmyTimer = QTimer()
        self.increasearmyTimer.timeout.connect(self.increaseArmy)
        self.increasearmyTimer.start(2000)  

    def setColor(self, new_color: QColor):
        self.color = new_color
        
        self.update()


    def setBoosted(self, status: bool):
        self.boosted = status

    def increaseArmy(self):
        self.army += 4 if self.boosted else 2
        self.update(0, -20, self.size, self.size + 20)
        self.boosted = False

        
        army_factor = max(1.0, math.log(self.army + 5))
        max_interval = 2000
        min_interval = 500
        new_interval = max(min_interval, int(max_interval / army_factor))
        self.increasearmyTimer.setInterval(new_interval)

