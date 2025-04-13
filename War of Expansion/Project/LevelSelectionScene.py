from PySide6.QtWidgets import (
    QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem,
    QLineEdit, QGraphicsProxyWidget, QFileDialog
)
from PySide6.QtGui import QFont, QColor, QBrush, QPen, QLinearGradient, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRectF, Signal, QObject, QRegularExpression


class SceneSignals(QObject):
    level_selected = Signal(int)
    start_game = Signal(str, str)  # mode or path
    exit_game = Signal()


class FancyButton(QGraphicsRectItem):
    def __init__(self, text, width, height, callback, font_size=16):
        super().__init__(0, 0, width, height)
        self.callback = callback
        self.text = text

        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor("#4e9af1"))
        gradient.setColorAt(1, QColor("#1b65b8"))
        self.setBrush(QBrush(gradient))
        self.setPen(QPen(Qt.white, 2))
        self.setZValue(1)
        self.setAcceptHoverEvents(True)

        self.text_item = QGraphicsTextItem(text, self)
        self.text_item.setFont(QFont("Arial", font_size, QFont.Bold))
        self.text_item.setDefaultTextColor(Qt.white)
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos((width - text_rect.width()) / 2, (height - text_rect.height()) / 2)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor("#6fb1fc"))

    def hoverLeaveEvent(self, event):
        gradient = QLinearGradient(0, 0, 0, self.rect().height())
        gradient.setColorAt(0, QColor("#4e9af1"))
        gradient.setColorAt(1, QColor("#1b65b8"))
        self.setBrush(QBrush(gradient))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.callback:
            self.callback()


class MainMenuScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.signals = SceneSignals()
        self.setSceneRect(0, 0, 800, 600)
        self.setBackgroundBrush(QColor(30, 30, 40))

        self.selected_mode = "Single Player"

        title = QGraphicsTextItem("Tower Strategy")
        title.setFont(QFont("Georgia", 38, QFont.Bold))
        title.setDefaultTextColor(QColor("#aaccff"))
        title.setPos(200, 40)
        self.addItem(title)

        self.add_mode_selector("Single Player", 200)
        self.add_mode_selector("Local Two Players", 270)
        self.add_mode_selector("Network Game", 340)

        # IP/port input
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g. 192.168.0.1:1234")
        self.ip_input.setStyleSheet("color: white; background-color: #4e9af1; border: 1px solid white;")
        self.ip_input.setToolTip("Enter IP and port")

        regex = QRegularExpression(r"^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
                                   r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d):\d{1,5}$")
        self.ip_input.setValidator(QRegularExpressionValidator(regex))

        self.ip_proxy = QGraphicsProxyWidget()
        self.ip_proxy.setWidget(self.ip_input)
        self.ip_proxy.setPos(300, 410)
        self.addItem(self.ip_proxy)
        self.ip_proxy.setVisible(False)

        # Buttons
        start_button = FancyButton("Start Game", 200, 60, self.emit_start)
        start_button.setPos(300, 470)
        self.addItem(start_button)

        load_button = FancyButton("Load Save", 200, 60, self.load_game)
        load_button.setPos(300, 540)
        self.addItem(load_button)

        exit_button = FancyButton("Exit", 200, 60, self.signals.exit_game.emit)
        exit_button.setPos(300, 610)
        self.addItem(exit_button)

    def add_mode_selector(self, label, y):
        def on_click():
            self.selected_mode = label
            self.update_mode_buttons()
            self.ip_proxy.setVisible("Network" in label)

        btn = FancyButton(label, 300, 50, on_click, font_size=14)
        btn.setPos(250, y)
        self.addItem(btn)
        setattr(self, f"mode_btn_{label.replace(' ', '_')}", btn)

    def update_mode_buttons(self):
        for label in ["Single Player", "Local Two Players", "Network Game"]:
            btn = getattr(self, f"mode_btn_{label.replace(' ', '_')}")
            is_selected = (label == self.selected_mode)
            btn.setPen(QPen(Qt.green if is_selected else Qt.white, 3))

    def emit_start(self):
        ip = self.ip_input.text().strip() if "Network" in self.selected_mode else ""
        self.signals.start_game.emit(self.selected_mode, ip)

    def load_game(self):
        path, _ = QFileDialog.getOpenFileName(None, "Select Save File", "", "Save Files (*.json *.xml)")
        if path:
            self.signals.start_game.emit("LoadFromFile", path)


class LevelSelectionScene(QGraphicsScene):
    def __init__(self, levels=4):
        super().__init__()
        self.signals = SceneSignals()
        self.setSceneRect(0, 0, 800, 600)
        self.setBackgroundBrush(QColor(30, 30, 40))

        title = QGraphicsTextItem("Select Level")
        title.setFont(QFont("Georgia", 28, QFont.Bold))
        title.setDefaultTextColor(QColor("#aaccff"))
        title.setPos(270, 70)
        self.addItem(title)

        for i in range(levels):
            self.add_level_button(i + 1, 300, 170 + i * 80)

        back_button = FancyButton("Back to Menu", 200, 50, self.signals.exit_game.emit, font_size=14)
        back_button.setPos(300, 400 + levels * 60)
        self.addItem(back_button)

    def add_level_button(self, level_number, x, y):
        def on_click():
            self.signals.level_selected.emit(level_number)

        button = FancyButton(f"Level {level_number}", 200, 50, on_click, font_size=14)
        button.setPos(x, y)
        self.addItem(button)
