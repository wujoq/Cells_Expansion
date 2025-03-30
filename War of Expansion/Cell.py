from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QTimer, QRectF, Qt, QPointF
from PySide6.QtGui import QPixmap, QBrush, QPen, QFont, QColor, QMouseEvent


class Cell(QGraphicsItem):
    def __init__(self, size: int, position: QPointF, color: QColor):
        super().__init__()
        self.army = 10
        self.price = 25
        self.size = size
        self.position = position
        self.color = color
        self.connections = []  # Przechowuje połączenia komórek
        self.selected = False  # Flaga wskazująca, czy komórka jest zaznaczona
        self.setPos(position)

        self.increasearmyTimer = QTimer()
        self.increasearmyTimer.timeout.connect(self.increaseArmy)
        self.increasearmyTimer.start(1500)

    def boundingRect(self):
        # Rozszerzamy obszar rysowania o 20 pikseli w górę, aby zmieścić licznik
        return QRectF(0, -20, self.size, self.size + 20)

    def paint(self, painter, option, widget=None):
        # Rysujemy komórkę jako okrąg
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

        # Rysujemy nazwę "Cell" wewnątrz okręgu
        painter.setFont(QFont("Arial", 10))
        text_rect = QRectF(0, 0, self.size, self.size)
        text_rect.moveCenter(QPointF(self.size / 2, self.size / 2))
        painter.drawText(text_rect, Qt.AlignCenter, "Cell")

    def increaseArmy(self):
        self.army += 1
        # Wymuszamy odświeżenie całego rozszerzonego obszaru
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
        # Upewniamy się, że boundingRect obejmuje zarówno sprite, jak i licznik (obszar nad komórką)
        return QRectF(0, -20, self.size, self.size + 20)

    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % self.frame_count
        # Wymuszamy odświeżenie całego rozszerzonego obszaru
        self.update(0, -20, self.size, self.size + 20)

    def paint(self, painter, option, widget=None):
        # Rysujemy animowany sprite lub standardowy rysunek komórki
        if self.frames:
            pixmap = self.frames[self.current_frame]
            x_offset = (self.size - pixmap.width()) / 2
            y_offset = (self.size - pixmap.height()) / 2
            painter.drawPixmap(x_offset, y_offset, pixmap)
        else:
            super().paint(painter, option, widget)
        # Rysujemy licznik army nad sprite'em
        painter.setFont(QFont("Arial", 10))
        army_rect = QRectF(0, -20, self.size, 20)
        painter.drawText(army_rect, Qt.AlignCenter, str(self.army))


class AttackCell(AnimatedCell):
    def __init__(self, size: int, position: QPointF, color: QColor):
        resource_path = ":/towers/attacking_unit.png"  # Dostosuj ścieżkę do zasobów
        super().__init__(size, position, color, resource_path)
        

class SupportCell(AnimatedCell):
    def __init__(self, size: int, position: QPointF, color: QColor, frame_count: int = 4):
        resource_path = ":/towers/support_unit.png"  # Dostosuj ścieżkę do zasobów
        super().__init__(size, position, color, resource_path, frame_count)
        self.price = 30

class GeneratorCell(AnimatedCell):
    def __init__(self, size: int, position: QPointF, color: QColor):
        resource_path = ":/towers/generating_unit.png"  # Dostosuj ścieżkę do zasobów
        super().__init__(size, position, color, resource_path)
        self.price = 35
    
    
