import sys
import resources_rc
from Cell import *
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem
from PySide6.QtGui import QPixmap, QPainter, QBrush, QPen, QFont, QColor
from PySide6.QtCore import QRectF, QPointF, QTimer, Qt




# Example usage
if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    view.setFixedSize(800, 600)
    scene.setBackgroundBrush(QBrush(QColor(81,171,179)))
    # Create instances of each cell type and add to the scene.
    attack_cell = AttackCell(size=128, position=QPointF(0, 50), color=QColor("red"))
    support_cell = SupportCell(size=128, position=QPointF(150, 50), color=QColor("green"))
    generator_cell = GeneratorCell(size=128, position=QPointF(300, 50), color=QColor("blue"))

    scene.addItem(attack_cell)
    scene.addItem(support_cell)
    scene.addItem(generator_cell)

    view.show()
    sys.exit(app.exec())
