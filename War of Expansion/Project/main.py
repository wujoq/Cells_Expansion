from PySide6.QtWidgets import QApplication, QGraphicsView,QMainWindow
from Game_scene import *
import sys
from Cell import *
from LevelSelectionScene import LevelSelectionScene


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tower Game - Level Select")
        self.view = QGraphicsView()
        self.setCentralWidget(self.view)
        self.resize(820, 840)
        self.init_level_menu()

    def init_level_menu(self):
        self.level_menu = LevelSelectionScene()
        self.level_menu.signals.level_selected.connect(self.load_level)
        self.view.setScene(self.level_menu)

    def load_level(self, level_number):
        scene = GameScene(level_number, self)
        self.view.setScene(scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
