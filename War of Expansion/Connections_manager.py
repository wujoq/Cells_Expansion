from Connections import Connection

class ConnectionsManager:
    def __init__(self):
        self.connections = []

    def add_connection(self, cell1, cell2):
        # Check if the connection already exists
        for connection in self.connections:
            if (connection.cell1 == cell1 and connection.cell2 == cell2) or (connection.cell1 == cell2 and connection.cell2 == cell1):
                return

        # Create a new connection if it doesn't already exist
        connection = Connection(cell1, cell2)
        self.connections.append(connection)
        cell1.connections.append(cell2)
        cell2.connections.append(cell1)

    def remove_connection(self, cell1, cell2):
        # Remove the connection from the list
        for connection in self.connections:
            if (connection.cell1 == cell1 and connection.cell2 == cell2) or (connection.cell1 == cell2 and connection.cell2 == cell1):
                self.connections.remove(connection)
                cell1.connections.remove(cell2)
                cell2.connections.remove(cell1)
                return

    def clear_connections(self):
        # Clear all connections
        self.connections.clear()
        for cell in self.get_all_cells():
            cell.connections.clear()

