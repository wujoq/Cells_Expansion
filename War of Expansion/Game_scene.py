from PySide6.QtWidgets import (
    QGraphicsTextItem, QGraphicsRectItem, QGraphicsLineItem
)
from PySide6.QtCore import Qt, QPointF, QRectF, QLineF, QTimer
from PySide6.QtGui import QPixmap, QBrush, QColor, QFont, QPen
import random
from Cell import *
from Event_handler import EventHandler
from BuildSpot import BuildSpot
from TowerSelector import TowerSelector
from Connections_manager import ConnectionsManager
from history_logger import save_game_history

class GameScene(EventHandler):
    def __init__(self, level_number, window, from_save=False):
        super().__init__(size=100)
        self.setSceneRect(0, 0, 800, 800)
        self.selector = TowerSelector(self)
        self.window = window
        self.level_number = level_number
        self.cells = []
        self.build_spots = []
        self.ai_build_spots = []
        self.connection_lines = []
        self.connections_manager = ConnectionsManager()
        self.player_connection_used = False
        self.ai_connection_used = False
        self.turn_active = False
        self.turn_counter = 0
        self.remaining_time = 15
        self.active = False

        self.initBackground()
        self.add_control_buttons()
        self.add_turn_display()

        if not from_save:
            if level_number == 1:
                self.initBuildSpots_Level1()
            elif level_number == 2:
                self.initBuildSpots_Level2()
            self.start_pregame_build()

        self.turn_timer = QTimer()
        self.turn_timer.setInterval(1000)
        self.turn_timer.timeout.connect(self.update_turn_timer)
    def set_active(self, value: bool):
        self.active = value

    def initBackground(self):
        pixmap = QPixmap(":/tiles/FieldsTile_38.png")
        if pixmap.isNull():
            print("Failed to load background image!")
            return
        self.setBackgroundBrush(QBrush(pixmap))

    def initBuildSpots_Level1(self):
        spots = [QPointF(200, 200), QPointF(400, 300), QPointF(600, 200)]
        for pos in spots:
            spot = BuildSpot(pos, self.size, self)
            self.build_spots.append(spot)
            self.addItem(spot)

        ai_spots = [QPointF(150, 100), QPointF(500, 100)]
        for pos in ai_spots:
            spot = BuildSpot(pos, self.size, self)
            self.ai_build_spots.append(spot)
            self.addItem(spot)

    def initBuildSpots_Level2(self):
        spots = [QPointF(200, 300), QPointF(240, 300), QPointF(500, 350), QPointF(600, 100)]
        for pos in spots:
            spot = BuildSpot(pos, self.size, self)
            self.build_spots.append(spot)
            self.addItem(spot)

        ai_spots = [QPointF(100, 300), QPointF(700, 300)]
        for pos in ai_spots:
            spot = BuildSpot(pos, self.size, self)
            self.ai_build_spots.append(spot)
            self.addItem(spot)

    def start_pregame_build(self):
        self.turn_counter_text.setPlainText("Build Phase")
        self.turn_timer_text.setPlainText("Waiting...")

        self.ai_timer = QTimer()
        self.ai_timer.setInterval(1000)
        self.ai_timer.timeout.connect(self.ai_build_turn)
        self.ai_timer.start()

    def ai_build_turn(self):
        if not self.ai_build_spots:
            self.ai_timer.stop()
            if not self.build_spots:
                self.start_next_turn()
            return

        spot = random.choice(self.ai_build_spots)
        unit_type = random.choice(["attacking"] * 5 + ["generating", "supporting"])
        self.place_ai_tower(spot, unit_type)

        if not self.ai_build_spots and not self.build_spots:
            self.start_next_turn()

    def show_tower_selector(self, spot):
        if self.turn_active:
            return
        self.selector.show(spot)

    def place_tower(self, spot, unit_type):
        offset = QPointF(self.size / 2, self.size / 2)
        pos = spot.pos() - offset
        if unit_type == "attacking":
            tower = AttackCell(self.size, pos, QColor("blue"))
        elif unit_type == "generating":
            tower = GeneratorCell(self.size, pos, QColor("blue"))
        elif unit_type == "supporting":
            tower = SupportCell(self.size, pos, QColor("blue"))
        else:
            return
        self.cells.append(tower)
        self.addItem(tower)
        self.removeItem(spot)
        self.build_spots.remove(spot)

        if not self.ai_build_spots and not self.build_spots:
            self.start_next_turn()

    def place_ai_tower(self, spot, unit_type):
        offset = QPointF(self.size / 2, self.size / 2)
        pos = spot.pos() - offset

        if unit_type == "attacking":
            tower = AttackCell(self.size, pos, QColor("red"), resource_path=":/towers/attacking_unit_enemy.png")
        elif unit_type == "generating":
            tower = GeneratorCell(self.size, pos, QColor("red"), resource_path=":/towers/generating_unit_enemy.png")
        elif unit_type == "supporting":
            tower = SupportCell(self.size, pos, QColor("red"), resource_path=":/towers/support_unit_enemy.png")
        else:
            return

        self.cells.append(tower)
        self.addItem(tower)
        self.removeItem(spot)
        self.ai_build_spots.remove(spot)

    def add_control_buttons(self):
        self.add_button("Reset", self.reset_level, QPointF(10, 10))
        self.add_button("Menu", self.window.init_main_menu, QPointF(10, 60))
        self.add_holdable_button("Connections", QPointF(10, 110))

    def add_turn_display(self):
        self.turn_counter_text = QGraphicsTextItem("Turn: 0")
        self.turn_counter_text.setDefaultTextColor(Qt.white)
        self.turn_counter_text.setFont(QFont("Arial", 14))
        self.turn_counter_text.setPos(640, 10)
        self.addItem(self.turn_counter_text)

        self.turn_timer_text = QGraphicsTextItem("Time: 15")
        self.turn_timer_text.setDefaultTextColor(Qt.white)
        self.turn_timer_text.setFont(QFont("Arial", 14))
        self.turn_timer_text.setPos(640, 40)
        self.addItem(self.turn_timer_text)

    def update_turn_timer(self):
        if not self.active:
            return
        self.remaining_time -= 1
        self.turn_timer_text.setPlainText(f"Time: {self.remaining_time}")
        if self.remaining_time <= 0:
            self.start_next_turn()

    def add_button(self, label, callback, pos):
        button = QGraphicsRectItem(QRectF(0, 0, 130, 40))
        button.setPos(pos)
        button.setBrush(QBrush(QColor(70, 70, 200)))
        button.setPen(QPen(Qt.black))
        button.setZValue(10)
        button.setToolTip(label)

        text = QGraphicsTextItem(label)
        text.setParentItem(button)
        text.setDefaultTextColor(Qt.white)
        text.setFont(QFont("Arial", 12))
        text.setPos(15, 10)
        text.setZValue(11)

        def on_click(event):
            if event.button() == Qt.LeftButton and callback:
                callback()

        button.mousePressEvent = on_click
        self.addItem(button)

    def add_holdable_button(self, label, pos):
        button = QGraphicsRectItem(QRectF(0, 0, 130, 40))
        button.setPos(pos)
        button.setBrush(QBrush(QColor(70, 70, 200)))
        button.setPen(QPen(Qt.black))
        button.setZValue(10)
        button.setToolTip(label)

        text = QGraphicsTextItem(label)
        text.setParentItem(button)
        text.setDefaultTextColor(Qt.white)
        text.setFont(QFont("Arial", 12))
        text.setPos(15, 10)
        text.setZValue(11)

        def on_press(event):
            if event.button() == Qt.LeftButton:
                self.highlight_connections()

        def on_release(event):
            self.clear_highlighted_connections()

        button.mousePressEvent = on_press
        button.mouseReleaseEvent = on_release
        self.addItem(button)

    def reset_level(self):
        self.window.load_level(self.level_number)

    def highlight_connections(self):
        self.connection_lines.clear()
        for i, cell1 in enumerate(self.cells):
            for j, cell2 in enumerate(self.cells):
                if i >= j:
                    continue
                if isinstance(cell1, SupportCell) or isinstance(cell2, SupportCell):
                    continue
                if isinstance(cell1, GeneratorCell) and cell2.is_enemy(cell1.color):
                    continue
                if isinstance(cell2, GeneratorCell) and cell1.is_enemy(cell2.color):
                    continue
                if len(cell1.connections) >= 3 or len(cell2.connections) >= 3:
                    continue
                already_connected = cell2 in cell1.connections or cell1 in cell2.connections
                if already_connected:
                    continue
                line = QGraphicsLineItem(QLineF(
                    cell1.pos() + QPointF(self.size / 2, self.size / 2),
                    cell2.pos() + QPointF(self.size / 2, self.size / 2)))
                line.setPen(QPen(Qt.green, 2, Qt.DashLine))
                line.setZValue(-2)
                self.connection_lines.append(line)
                self.addItem(line)

    def clear_highlighted_connections(self):
        for line in self.connection_lines:
            self.removeItem(line)
        self.connection_lines.clear()

    def start_next_turn(self):
        if not self.active:
            return

        self.turn_active = True
        self.player_connection_used = False
        self.ai_connection_used = False
        self.turn_counter += 1
        self.turn_counter_text.setPlainText(f"Turn: {self.turn_counter}")
        self.remaining_time = 5
        self.turn_timer_text.setPlainText("Time: 5")
        self.ai_timer = QTimer()
        self.ai_timer.timeout.connect(self.run_enemy_ai)
        self.ai_timer.start(100)
        self.turn_timer.start()

        conn_pairs = []
        for cell in self.cells:
            for connected in cell.connections:
                if (connected, cell) not in conn_pairs:
                    conn_pairs.append((cell, connected))

        save_game_history(
            level_number=self.level_number,
            game_mode=self.window.mode,
            ip_address=self.window.ip_address,
            cells=self.cells,
            connections=conn_pairs,
            build_spots=self.build_spots + self.ai_build_spots,
            save_to_json=True,
            save_to_xml=True
        )

    def run_enemy_ai(self):
        if not self.active or self.ai_connection_used:
            return

        red_towers = [c for c in self.cells if isinstance(c, AttackCell) and c.color == QColor("red") and c.army > 10]
        blue_targets = [c for c in self.cells if c.color != QColor("red")]

        if not red_towers or not blue_targets:
            return

        for red in red_towers:
            blue_targets.sort(key=lambda c: (c.pos() - red.pos()).manhattanLength())
            for blue in blue_targets:
                if blue not in red.connections:
                    self.connections_manager.add_connection(red, blue, self, by="ai")
                    self.ai_connection_used = True
                    return

    def try_player_connection(self, source, target):
        if not self.turn_active or self.player_connection_used:
            return
        if target in source.connections:
            return
        if source.is_enemy(QColor("blue")) and target.is_enemy(QColor("blue")):
            print("❌ Cannot connect two enemy towers.")
            return
        self.connections_manager.add_connection(source, target, self, by="player")
