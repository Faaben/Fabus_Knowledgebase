import sqlite3
import os

class Datenbank:
    def __init__(self, db_name="Fäbus_KB.db"):
        # Speicherort der Datenbank im "Dokumente"-Verzeichnis des Benutzers
        self.db_folder = os.path.join(os.path.expanduser("~"), "Documents", "Fäbus_KB")
        os.makedirs(self.db_folder, exist_ok=True)  # Falls der Ordner nicht existiert, erstelle ihn
        
        self.db_name = os.path.join(self.db_folder, db_name)

        # Debug-Ausgabe, um sicherzustellen, dass der richtige Pfad verwendet wird
        print("Datenbank wird gespeichert unter:", self.db_name)

        # Falls die Datei nicht existiert, initialisiere die Datenbank
        if not os.path.exists(self.db_name):
            self.init_db()

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

    def update_note(self, note_id, title, content, image_blob=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        if image_blob:
            c.execute("UPDATE notes SET title = ?, content = ?, image = ? WHERE id = ?", (title, content, image_blob, note_id))
        else:
            c.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
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


    def get_note(self, note_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
        note = c.fetchone()
        conn.close()
        return note if note else (None, None)


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



