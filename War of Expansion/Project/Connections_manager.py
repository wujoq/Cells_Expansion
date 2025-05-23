from Connections import Connection
from Cell import *

class ConnectionsManager:
    def __init__(self):
        self.connections = []

    def add_connection(self, cell1, cell2, scene, by="player", player_color=None):
        if by == "player":
            if hasattr(scene, 'player_connection_used') and scene.player_connection_used:
                print("❌ Player already made a connection this turn.")
                return

            if player_color and cell1.is_enemy(player_color) and cell2.is_enemy(player_color):
                print("❌ Cannot connect two enemy towers.")
                return

            scene.player_connection_used = True

        if isinstance(cell1, SupportCell) or isinstance(cell2, SupportCell):
            return
        if isinstance(cell1, GeneratorCell) and cell2.is_enemy(cell1.color):
            return

        if self.count_sending_connections(cell1) >= 3:
            print(f"❌ {cell1} reached max outgoing connections.")
            return

        existing_connection = self.get_connection(cell1, cell2)

        if existing_connection:
            existing_connection.enable_sending_from(cell1)
        else:
            conn = Connection(cell1, cell2, self)
            self.connections.append(conn)
            scene.addItem(conn)
            conn.enable_sending_from(cell1)
            cell1.connections.append(cell2)
            cell2.connections.append(cell1)

            # 🔁 Synchronizacja z drugim graczem
            if hasattr(scene, "network") and scene.network:
                move = {
                    "action": "connect",
                    "from": [int(cell1.pos().x()), int(cell1.pos().y())],
                    "to": [int(cell2.pos().x()), int(cell2.pos().y())]
                }
                print("[SYNC] Broadcasting connection:", move)
                scene.network.send(move)


    def get_connection(self, cell1, cell2):
        for conn in self.connections:
            if (conn.cell1 == cell1 and conn.cell2 == cell2) or (conn.cell1 == cell2 and conn.cell2 == cell1):
                return conn
        return None

    def count_sending_connections(self, cell):
        count = 0
        for conn in self.connections:
            if conn.cell1 == cell and conn.sending_from_cell1:
                count += 1
            elif conn.cell2 == cell and conn.sending_from_cell2:
                count += 1
        return count

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

        if connection.cell2 in connection.cell1.connections:
            connection.cell1.connections.remove(connection.cell2)
        if connection.cell1 in connection.cell2.connections:
            connection.cell2.connections.remove(connection.cell1)

    def clear_connections(self):
        for connection in self.connections:
            connection.stop_all_sending()
            if connection.scene():
                connection.scene().removeItem(connection)
        self.connections.clear()
    def spawn_connection_animation(self, cell1, cell2, scene):
        existing = self.get_connection(cell1, cell2)
        if not existing:
            conn = Connection(cell1, cell2, self)
            self.connections.append(conn)
            scene.addItem(conn)
            cell1.connections.append(cell2)
            cell2.connections.append(cell1)
