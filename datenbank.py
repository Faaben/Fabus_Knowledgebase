import sqlite3

class Datenbank:
    def __init__(self, db_name="notizbuch.db"):
        self.db_name = db_name

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, image BLOB)''')
        conn.commit()
        conn.close()

    def add_note(self, note, image_data=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content, image) VALUES (?, ?, ?)", (note.title, note.content, image_data))
        conn.commit()
        note_id = c.lastrowid  # **Hier wird die ID der neu erstellten Notiz gespeichert**
        conn.close()
        return note_id  # **Notiz-ID zurückgeben**

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
    








    def speichere_screenshot(self, note_id, image_data):
        """Speichert oder aktualisiert einen Screenshot für eine bestehende Notiz."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("UPDATE notes SET image = ? WHERE id = ?", (image_data, note_id))
        conn.commit()
        conn.close()

    def lade_letzten_screenshot(self):
        """Lädt das Bild der letzten gespeicherten Notiz."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT image FROM notes WHERE image IS NOT NULL ORDER BY id DESC LIMIT 1")
        record = c.fetchone()
        conn.close()
        return record[0] if record else None  # Gibt den BLOB-Datenwert zurück
    
    def get_last_note_id(self):
        """Holt die ID der zuletzt gespeicherten Notiz."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id FROM notes ORDER BY id DESC LIMIT 1")  # Letzte Notiz-ID abrufen
        result = c.fetchone()
        conn.close()
        return result[0] if result else None  # Falls keine Notiz existiert, gebe `None` zurück
    
    def lade_screenshot(self, note_id):
        """Lädt den Screenshot einer bestimmten Notiz aus der Datenbank."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT image FROM notes WHERE id = ?", (note_id,))
        record = c.fetchone()
        conn.close()
        return record[0] if record and record[0] else None  # Falls kein Bild vorhanden ist, gebe `None` zurück



