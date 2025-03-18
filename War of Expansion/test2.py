import sys
from Cell import *
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem
from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QBrush, QPen, QColor


app = QApplication(sys.argv)
scene = QGraphicsScene()

# Obliczanie środka sceny
scene_width = 600  # Szerokość sceny
scene_height = 800  # Wysokość sceny
cell_size = 100  # Rozmiar komórki

# Obliczanie pozycji środka sceny
center_x = (scene_width - cell_size) / 2
center_y = (scene_height - cell_size) / 2

# Tworzenie obiektu Cell na środku sceny
cell = Cell(size=cell_size, position=QPointF(center_x, center_y), connections=2, max_connections=5, cells=10, cells_increase_speed=1, color=QColor(255, 0, 0))
enemy_cell = Cell(cell_size,QPointF(center_x, center_y+1.2*cell_size),color=QColor(0, 255, 0) )
# Dodanie komórki do sceny
scene.addItem(cell)
scene.addItem(enemy_cell)
# Tworzenie widoku
view = QGraphicsView(scene)
view.setFixedSize(scene_width + 50, scene_height + 50)  # Dostosowanie rozmiaru widoku
view.show()

# Uruchomienie pętli zdarzeń aplikacji
sys.exit(app.exec_())
