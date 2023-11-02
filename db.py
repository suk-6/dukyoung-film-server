import sqlite3

conn = sqlite3.connect('images.sqlite', check_same_thread=False)

c = conn.cursor()

if not c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='images'").fetchone():
    c.execute('''CREATE TABLE images
                (id text, time text, image text)''')

def insertImage(id, time, image):
    c.execute("INSERT INTO images VALUES (?, ?, ?)", (id, time, image))
    conn.commit()

def selectImage(id):
    return c.execute("SELECT * FROM images WHERE id=?", (id,)).fetchone()

def getImageAll():
    return c.execute("SELECT * FROM images ORDER BY time DESC")