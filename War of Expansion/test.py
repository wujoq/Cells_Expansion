import sys
import Cell
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QPen, QColor

app = QApplication(sys.argv)

# Tworzenie pędzla i pióra
red_brush = QBrush(QColor(255, 0, 0))  # Czerwony pędzel
black_pen = QPen(QColor(0, 0, 0))  # Czarny kontur

cell1 = Cell()



# Tworzenie sceny
scene = QGraphicsScene()
scene.setSceneRect(QRectF(0, 0, 600, 800))

# Dodanie elipsy (koła) z pędzlem i piórem
scene.addEllipse(100, 100, 100, 100, black_pen, red_brush)

# Tworzenie widoku i ustawienie rozmiaru
view = QGraphicsView(scene)
view.setFixedSize(650, 850)
view.show()

# Uruchomienie pętli zdarzeń aplikacji
sys.exit(app.exec_())
