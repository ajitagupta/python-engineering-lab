import sqlite3


con = sqlite3.connect("workouts.db")

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS workouts(id INTEGER PRIMARY KEY, sport TEXT, distance_km REAL, duration_min REAL)")
cur.execute("""
    INSERT INTO workouts (sport, distance_km, duration_min) VALUES
        ('run', 5.0, 30.0),
        ('bike', 10.0, 60.0),
        ('swim', 1.0, 45.0),
        ('rest', NULL, NULL)
""")
con.commit()
for row in cur.execute("SELECT * FROM workouts ORDER BY id"):
    print(row)
con.close()