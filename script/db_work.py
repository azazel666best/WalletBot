import sqlite3


class DBWork:
    def __init__(self, name):
        self.conn = sqlite3.connect(f'../data_base/{name}.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS transacts(
           transact_id INTEGER PRIMARY KEY AUTOINCREMENT,
           sum real,
           category TEXT,
           date TEXT,
           description);""")
        self.conn.commit()

    def insert(self, *data):
        self.cur.execute(f'INSERT INTO transacts(sum, category, date, description) '
                         f'VALUES({", ".join("?" * len(data))});', data)
        self.conn.commit()

    def update(self, field_name, new_value, transact_id):
        self.cur.execute(f'UPDATE transacts '
                         f'SET {field_name} = {new_value} '
                         f'WHERE transact_id = {transact_id};')
        self.conn.commit()

    def delete(self, transact_id):
        self.cur.execute(f'DELETE FROM transacts WHERE transact_id = {transact_id};')
        self.conn.commit()

    def select(self, fields='*'):
        self.cur.execute(f"SELECT {fields} FROM transacts; ")
        return self.cur.fetchall()

    def select_distinct(self, fields='*'):
        self.cur.execute(f"SELECT DISTINCT {fields} FROM transacts; ")
        return self.cur.fetchall()

    def select_where(self, field_name, field_value, fields='*'):
        self.cur.execute(f"SELECT {fields} FROM transacts WHERE {field_name} = {field_value};")
        return self.cur.fetchall()

    def select_where_max(self, field_name, field_value, fields='*'):
        self.cur.execute(
            f"SELECT {fields} FROM transacts WHERE {field_name} = (SELECT MAX({field_value}) FROM transacts);")
        return self.cur.fetchall()

    def select_sort_by_date(self, fields='*'):
        res = self.cur.execute(f"SELECT date(date) FROM transacts; ")
        # res = list(map(lambda x: x[3].split('.'), self.cur.execute(f"SELECT {fields} FROM transacts; ")))
        # res.sort(key=lambda x: x[2])
        return res
