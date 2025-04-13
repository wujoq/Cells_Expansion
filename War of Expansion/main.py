from PySide6.QtWidgets import QApplication, QGraphicsView, QMainWindow
from Game_scene import GameScene
from LevelSelectionScene import MainMenuScene, LevelSelectionScene
from game_loader import load_game_state
import sys

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tower Strategy")
        self.view = QGraphicsView()
        self.setCentralWidget(self.view)
        self.resize(820, 840)

        self.mode = "Single Player"
        self.ip_address = ""

        self.init_main_menu()

    def set_scene(self, scene):
        current = self.view.scene()
        if isinstance(current, GameScene):
            current.set_active(False)
        self.view.setScene(scene)
        if isinstance(scene, GameScene):
            scene.set_active(True)

    def init_main_menu(self):
        self.menu_scene = MainMenuScene()
        self.menu_scene.signals.start_game.connect(self.apply_config)
        self.menu_scene.signals.exit_game.connect(self.close)
        self.set_scene(self.menu_scene)

    def apply_config(self, mode, ip):
        self.mode = mode
        self.ip_address = ip
        if mode == "LoadFromFile":
            self.load_game_from_file(ip)
        else:
            self.init_level_menu()

    def init_level_menu(self):
        self.level_menu = LevelSelectionScene()
        self.level_menu.signals.level_selected.connect(self.load_level)
        self.level_menu.signals.exit_game.connect(self.init_main_menu)
        self.set_scene(self.level_menu)

    def load_level(self, level_number):
        scene = GameScene(level_number, self)
        self.set_scene(scene)

    def load_game_from_file(self, path):
        level, turn, cells, connections, build_spots = load_game_state(path)
        scene = GameScene(level_number=level, window=self, from_save=True)

        # Dodaj wieże
        scene.cells = cells
        for cell in cells:
            scene.addItem(cell)

        # Dodaj build spoty (te, które NIE są zajęte)
        scene.build_spots = [s for s in build_spots if not getattr(s, "is_ai", False)]
        scene.ai_build_spots = [s for s in build_spots if getattr(s, "is_ai", False)]
        for spot in scene.build_spots + scene.ai_build_spots:
            scene.addItem(spot)

        # Dodaj połączenia bez ograniczeń
        for cell1, cell2 in connections:
            if cell2 not in cell1.connections:
                cell1.connections.append(cell2)
            if cell1 not in cell2.connections:
                cell2.connections.append(cell1)
            scene.connections_manager.spawn_connection_animation(cell1, cell2, scene)

        # Przywróć numer tury i odśwież tekst
        scene.turn_counter = turn
        scene.turn_counter_text.setPlainText(f"Turn: {turn}")
        scene.remaining_time = 5
        scene.turn_timer_text.setPlainText("Time: 5")

        # Uruchomienie tury i AI
        scene.turn_timer.start()
        scene.turn_active = True
        scene.set_active(True)

        self.set_scene(scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
