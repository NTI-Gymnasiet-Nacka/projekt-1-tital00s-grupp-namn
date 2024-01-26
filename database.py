import sqlite3



class Database:

    def __init__(self, path="./db.db", **kwargs):
        self.path = "./db.db"
        self.schemas = {}
        for schema_name, schema in kwargs.items():
            self.schemas[schema_name] = schema 
        print(self.schemas)

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn
    
    def __exit__(self):
        self.conn.close()
        
    def add_data():
        pass

    def remove_data():
        pass

    def update_data():
        pass

    def get_data():
        pass

db = Database(reservation=["first_name", "last_name"])
    