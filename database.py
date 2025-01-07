import sqlite3
from abc import ABC, abstractmethod

DATABASE_PATH = "travel_database.sqlite"

class SQLMethodHandler(ABC):
    def __init__(self, connection):
        self.connection = connection

    @abstractmethod
    def handle(self, query, params=None):
        pass

class SelectHandler(SQLMethodHandler):
    def handle(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results

class InsertHandler(SQLMethodHandler):
    def handle(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Insert error: {e}")
            return False

class SQLDispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.handlers = {
            'select': SelectHandler(connection),
            'insert': InsertHandler(connection),
        }

    def execute(self, query, params=None):
        command = query.strip().split(' ')[0].lower()
        handler = self.handlers.get(command)

        if handler:
            return handler.handle(query, params)
        else:
            raise Exception(f"Unknown command: {command}")

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

dispatcher = SQLDispatcher(get_connection())