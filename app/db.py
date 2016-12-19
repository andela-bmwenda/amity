import sqlite3


class AmityDb(object):
    """
    Class that defines methods for writing
    and reading Amity data to the database
    """

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def create_tables(self):
        with self.conn:
            self.c.executescript("""
                DROP TABLE IF EXISTS rooms;
                CREATE TABLE IF NOT EXISTS rooms
                        (room_name CHAR(10),
                         room_type CHAR(10),
                         capacity INT,
                         occupants TEXT
                         );

                DROP TABLE IF EXISTS persons;
                CREATE TABLE IF NOT EXISTS persons
                        (identifier INT,
                         person_name CHAR(50),
                         role CHAR(10),
                         current_room CHAR(20)
                         );

                DROP TABLE IF EXISTS session;
                CREATE TABLE IF NOT EXISTS session
                        (data BLOB);

                """)

    def write_data(self, amity_rooms, allocated, unallocated, state):
        with self.conn:
            self.c.executemany(
                "INSERT INTO rooms VALUES (?, ?, ?, ?)", amity_rooms)
            self.c.executemany(
                "INSERT INTO persons VALUES (?, ?, ?, ?)", allocated)
            self.c.executemany(
                "INSERT INTO persons VALUES (?, ?, ?, ?)", unallocated)
            self.c.execute("INSERT INTO session VALUES (?)", (state, ))

    def read_data(self):
        with self.conn:
            self.c.execute("SELECT * FROM session ORDER BY data DESC LIMIT 1")
            try:
                data = self.c.fetchone()[0]
            except Exception:
                return None
            return data
