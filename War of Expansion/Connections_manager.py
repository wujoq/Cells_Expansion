from Connections import Connection

class ConnectionsManager:
    def __init__(self):
        self.connections = []

    def add_connection(self, cell1, cell2, scene):
        # Sprawdzamy, czy połączenie już istnieje
        for connection in self.connections:
            if (connection.cell1 == cell1 and connection.cell2 == cell2) or (connection.cell1 == cell2 and connection.cell2 == cell1):
                return

        connection = Connection(cell1, cell2)
        self.connections.append(connection)
        # Dodajemy obiekt Connection do sceny, aby był widoczny
        scene.addItem(connection)
        cell1.connections.append(cell2)
        cell2.connections.append(cell1)

    def remove_connection(self, cell1, cell2):
        for connection in self.connections:
            if (connection.cell1 == cell1 and connection.cell2 == cell2) or (connection.cell1 == cell2 and connection.cell2 == cell1):
                self.connections.remove(connection)
                cell1.connections.remove(cell2)
                cell2.connections.remove(cell1)
                return

    def clear_connections(self):
        self.connections.clear()
        # Usunięcie połączeń z komórek – metoda pomocnicza
        for cell in self.get_all_cells():
            cell.connections.clear()
