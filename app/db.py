import sqlite3
conn = sqlite3.connect("amity_db.db")
global c
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS rooms")
c.execute("""CREATE TABLE IF NOT EXISTS rooms
          (room_name CHAR(10),
           room_type CHAR(10),
           capacity INT,
           occupants TEXT);""")

c.execute("DROP TABLE IF EXISTS persons")
c.execute("""CREATE TABLE IF NOT EXISTS persons
          (identifier INT,
           person_name CHAR(50),
           role CHAR(10),
           current_room CHAR(20));""")

c.execute("DROP TABLE IF EXISTS session")
c.execute("""CREATE TABLE IF NOT EXISTS session
          (data BLOB);""")


def write_data(amity_rooms, allocated, unallocated, state):
    with conn:
        c.executemany("INSERT INTO rooms VALUES (?, ?, ?, ?)", amity_rooms)
        c.executemany("INSERT INTO persons VALUES (?, ?, ?, ?)", allocated)
        c.executemany("INSERT INTO persons VALUES (?, ?, ?, ?)", unallocated)
        c.execute("INSERT INTO session VALUES (?)", (state, ))


def read_data():
    with conn:
        c.execute("SELECT * FROM session ORDER BY data DESC LIMIT 1")
        try:
          data = c.fetchone()[0]
        except Exception:
          return None
        return data
