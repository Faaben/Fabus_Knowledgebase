import sqlite3
import os
from model.notiz import Notiz

class Datenbank:
    def __init__(self, db_name="Fäbus_KB.db"):
        self.db_folder = os.path.join(os.path.expanduser("~"), "Documents", "Fäbus_KB") # Speicherort der Datenbank im "Dokumente"-Verzeichnis des Benutzers
        os.makedirs(self.db_folder, exist_ok=True)  # Falls der Ordner nicht existiert, erstelle ihn
        self.db_name = os.path.join(self.db_folder, db_name)
        print("Datenbank wird gespeichert unter:", self.db_name) # Debug-Ausgabe, um sicherzustellen, dass der richtige Pfad verwendet wird
        
        if not os.path.exists(self.db_name): # Falls die Datei nicht existiert, initialisiere die Datenbank
            self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, image BLOB)''')
        conn.commit()
        conn.close()


    def save_note(self, note_id, note):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        if note_id is None:
            # Neue Notiz einfügen
            c.execute(
                "INSERT INTO notes (title, content, image) VALUES (?, ?, ?)",
                (note.title, note.content, note.image)
            )
            note_id = c.lastrowid
        else:
            # Bestehende Notiz aktualisieren
            if note.image:
                c.execute(
                    "UPDATE notes SET title = ?, content = ?, image = ? WHERE id = ?",
                    (note.title, note.content, note.image, note_id)
                )
            else:
                c.execute(
                    "UPDATE notes SET title = ?, content = ? WHERE id = ?",
                    (note.title, note.content, note_id)
                )

        conn.commit()
        conn.close()
        return note_id  # Gibt immer eine ID zurück – entweder neue oder bestehende


    def delete_note(self, note_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()


    def search_notes(self, query):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        if not query:  # Wenn die Suchanfrage leer ist → Alle Notizen abrufen
            c.execute("SELECT id, title, content FROM notes ORDER BY id ASC")
        else:
            c.execute("SELECT id, title, content FROM notes WHERE LOWER(title) LIKE ? OR LOWER(content) LIKE ?", 
                    (f"%{query}%", f"%{query}%"))
        results = c.fetchall()
        conn.close()
        return results


    def get_note(self, note_id: int) -> Notiz | None:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT title, content, image FROM notes WHERE id = ?", (note_id,))
        row = c.fetchone()
        conn.close()
        if row:
            title, content, image = row
            return Notiz(title=title, content=content, image=image, note_id=note_id)  # bezieht sich direkt auf deine Klasse
        return None
        #return note if note else (None, None)





    #def add_note(self, note):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content, image) VALUES (?, ?, ?)", (note.title, note.content, note.image))
        conn.commit()
        note_id = c.lastrowid  # **Hier wird die ID der neu erstellten Notiz gespeichert**
        conn.close()
        return note_id  # **Notiz-ID zurückgeben**


    #def update_note(self, note_id, note):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        if note.image:
            c.execute("UPDATE notes SET title = ?, content = ?, image = ? WHERE id = ?", (note.title, note.content, note.image, note_id))
        else:
            c.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (note.title, note.content, note_id))
        conn.commit()
        conn.close()


    #def lade_letzten_screenshot(self):
        """Lädt das Bild der letzten gespeicherten Notiz."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT image FROM notes WHERE image IS NOT NULL ORDER BY id DESC LIMIT 1")
        record = c.fetchone()
        conn.close()
        return record[0] if record else None  # Gibt den BLOB-Datenwert zurück
    

    #def get_last_note_id(self):
        """Holt die ID der zuletzt gespeicherten Notiz."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id FROM notes ORDER BY id DESC LIMIT 1")  # Letzte Notiz-ID abrufen
        result = c.fetchone()
        conn.close()
        return result[0] if result else None  # Falls keine Notiz existiert, gebe `None` zurück
    

    #def lade_screenshot(self, note_id):
        """Lädt den Screenshot einer bestimmten Notiz aus der Datenbank."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT image FROM notes WHERE id = ?", (note_id,))
        record = c.fetchone()
        conn.close()
        return record[0] if record and record[0] else None  # Falls kein Bild vorhanden ist, gebe `None` zurück


    #def speichere_screenshot(self, note_id, image_data):
        """Speichert oder aktualisiert einen Screenshot für eine bestehende Notiz."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("UPDATE notes SET image = ? WHERE id = ?", (image_data, note_id))
        conn.commit()
        conn.close()


