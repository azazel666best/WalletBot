import sqlite3


class DBWork:
    def __init__(self, name):
        self.conn = sqlite3.connect(f'{name}.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS wallet(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT);
        """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS transact(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           wallet_id INT,
           sum_of_money real,
           category TEXT,
           date TEXT,
           description);""")
        self.conn.commit()

    def insert(self, table_name, *data):
        fields_to_insert = ", ".join([description[0] for description
                                      in self.conn.execute(f"select * from {table_name}").description][1:])
        self.cur.execute(f'INSERT INTO {table_name}({fields_to_insert}) VALUES({", ".join("?" * len(data))})', data)
        self.conn.commit()

    def select(self, table_name, fields='*'):
        self.cur.execute(f"SELECT {fields} FROM {table_name};")
        return self.cur.fetchall()


