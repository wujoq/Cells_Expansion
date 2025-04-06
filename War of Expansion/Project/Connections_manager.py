from Connections import Connection
from Cell import *

class ConnectionsManager:
    def __init__(self):
        self.connections = []

    def add_connection(self, cell1, cell2, scene, by="player"):
        if by == "player":
            if hasattr(scene, 'player_connection_used') and scene.player_connection_used:
                print("❌ Player already made a connection this turn.")
                return
            if cell1.is_enemy(QColor("blue")) and cell2.is_enemy(QColor("blue")):
                print("❌ Cannot connect two enemy towers.")
                return
            scene.player_connection_used = True

        if len(cell1.connections) >= 3:
            print("❌ Cell 1 reached max connections.")
            return
        if len(cell2.connections) >= 3:
            print("❌ Cell 2 reached max connections.")
            return

        if isinstance(cell1, SupportCell) or isinstance(cell2, SupportCell):
            return
        if isinstance(cell1, GeneratorCell) and cell2.is_enemy(cell1.color):
            return

        is_enemy_pair = cell1.is_enemy(cell2.color) or cell2.is_enemy(cell1.color)

        exists_1_to_2 = any(c.cell1 == cell1 and c.cell2 == cell2 for c in self.connections)
        exists_2_to_1 = any(c.cell1 == cell2 and c.cell2 == cell1 for c in self.connections)

        if not exists_1_to_2:
            conn1 = Connection(cell1, cell2, self)
            self.connections.append(conn1)
            scene.addItem(conn1)
            cell1.connections.append(cell2)

        if is_enemy_pair and not exists_2_to_1:
            conn2 = Connection(cell2, cell1, self)
            self.connections.append(conn2)
            scene.addItem(conn2)
            cell2.connections.append(cell1)

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

        if connection.cell2 in connection.cell1.connections:
            connection.cell1.connections.remove(connection.cell2)
        if connection.cell1 in connection.cell2.connections:
            connection.cell2.connections.remove(connection.cell1)

    def clear_connections(self):
        for connection in self.connections:
            connection.sendingTimer.stop()
            if connection.scene():
                connection.scene().removeItem(connection)
        self.connections.clear()
