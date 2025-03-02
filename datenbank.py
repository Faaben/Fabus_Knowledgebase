import sqlite3

class Datenbank:
    def __init__(self, db_name="notizbuch.db"):
        self.db_name = db_name

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
        conn.commit()
        conn.close()

    def add_note(self, note):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (note.title, note.content))
        conn.commit()
        conn.close()

    def update_note(self, note_id, content):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("UPDATE notes SET content = ? WHERE id = ?", (content, note_id))
        conn.commit()
        conn.close()

    def delete_note(self, note_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()

    def search_notes(self, query):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, title, content FROM notes WHERE LOWER(title) LIKE ? OR LOWER(content) LIKE ?", 
                (f"%{query}%", f"%{query}%"))
        results = c.fetchall()
        conn.close()
        return results


    def get_note_content(self, note_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT content FROM notes WHERE id = ?", (note_id,))
        note = c.fetchone()
        conn.close()
        return note[0] if note else None
