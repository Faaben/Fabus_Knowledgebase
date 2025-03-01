import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

# Farben definieren
BG_COLOR = "#9DBABA"  # Türkis aus dem Bild
BTN_COLOR = "#59999A"  # Abgestufter Türkis-Ton
BTN_TEXT_COLOR = "white"
ENTRY_BG = "white"
ENTRY_FG = "black"
LABEL_TEXT_COLOR = "white"
HIGHLIGHT_COLOR = "yellow"  # Gelb für Markierungen
selected_note_id = None  # Globale Variable zum Speichern der ausgewählten Notiz-ID

# Datenbank initialisieren
def init_db():
    conn = sqlite3.connect("notizbuch.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

# Notiz hinzufügen
def add_note():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    if title and content:
        conn = sqlite3.connect("notizbuch.db")
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        messagebox.showinfo("Erfolg", "Notiz gespeichert!")
        search_notes()
    else:
        messagebox.showwarning("Fehler", "Titel und Inhalt dürfen nicht leer sein!")





# Notiz aktualisieren
def update_note():
    global selected_note_id
    if selected_note_id is None:
        messagebox.showwarning("Fehler", "Keine Notiz ausgewählt!")
        return
    
    # Extrahiere die geänderten Inhalte aus results_text
    content = results_text.get("1.0", tk.END).strip()

    if content:
        conn = sqlite3.connect("notizbuch.db")
        c = conn.cursor()
        c.execute("UPDATE notes SET content = ? WHERE id = ?", (content, selected_note_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Erfolg", "Notiz aktualisiert!")

        # Suche neu laden, damit die Änderung sichtbar ist
        search_notes()
        selected_note_id = None  # ID zurücksetzen
    else:
        messagebox.showwarning("Fehler", "Inhalt darf nicht leer sein!")








# Notiz löschen
def delete_note():
    global selected_note_id
    if selected_note_id is None:
        messagebox.showwarning("Fehler", "Keine Notiz ausgewählt!")
        return
    
    # Sicherheitsabfrage, um versehentliches Löschen zu verhindern
    confirm = messagebox.askyesno("Löschen bestätigen", "Möchtest du diese Notiz wirklich löschen?")
    
    if confirm:
        conn = sqlite3.connect("notizbuch.db")
        c = conn.cursor()
        c.execute("DELETE FROM notes WHERE id = ?", (selected_note_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Erfolg", "Notiz gelöscht!")

        # Suchergebnisse aktualisieren
        search_notes()

        # ID zurücksetzen, damit kein weiterer falscher Löschvorgang passiert
        selected_note_id = None

        # Eingabefelder leeren
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        results_text.delete("1.0", tk.END)  # Falls die Notiz direkt im Suchfeld bearbeitet wurde, auch hier löschen





# Notizen suchen
def search_notes():
    query = search_entry.get().strip().lower()
    results_text.tag_remove("highlight", "1.0", tk.END)  # Vorherige Markierungen entfernen
    results_text.delete("1.0", tk.END)  # Alte Suchergebnisse löschen

    if not query:
        results_text.insert(tk.END, "Bitte einen Suchbegriff eingeben.\n")
        return

    conn = sqlite3.connect("notizbuch.db")
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM notes WHERE LOWER(title) LIKE ? OR LOWER(content) LIKE ?", 
              (f"%{query}%", f"%{query}%"))
    results = c.fetchall()
    conn.close()

    if not results:
        results_text.insert(tk.END, "Keine Notizen gefunden.\n")
        return

    # Ergebnisse anzeigen und Highlight setzen
    for note_id, title, content in results:
        start_index = results_text.index(tk.END)  # Startposition im Text

        # ID normal einfügen
        results_text.insert(tk.END, f"ID: {note_id} | Titel: ", "normal")

        # Titel fett machen
        title_start = results_text.index(tk.END)
        results_text.insert(tk.END, title + "\n", "bold")

        # Hier wird Markdown für den Inhalt angewendet:
        insert_markdown_text(results_text, content)

        results_text.insert(tk.END, f"\n\n {'-'*40}\n\n")

        # Hervorhebung durchführen
        search_and_highlight(query, start_index)






# Notizen Highlighten        
def search_and_highlight(query, start_index):
    end_index = results_text.index(tk.END)  # Ende des Textfelds

    pos = results_text.search(query, start_index, stopindex=end_index, nocase=True)
    while pos:
        end_pos = f"{pos}+{len(query)}c"
        results_text.tag_add("highlight", pos, end_pos)
        pos = results_text.search(query, end_pos, stopindex=end_index, nocase=True)


# Notiz auswählen, damit man weiss welchen Teil man aktuallisieren will.
def select_note(event):
    global selected_note_id
    try:
        # Bestimme, welche Zeile angeklickt wurde
        index = results_text.index("@%d,%d" % (event.x, event.y))  
        line_start = results_text.index(index + " linestart")
        line_end = results_text.index(index + " lineend")
        line_text = results_text.get(line_start, line_end).strip()

        # Prüfen, ob die Zeile eine ID enthält (Format: "ID: X | Titel: XYZ")
        if line_text.startswith("ID:"):
            parts = line_text.split("|")
            if len(parts) > 1:
                note_id = parts[0].replace("ID:", "").strip()
                
                if note_id.isdigit():
                    selected_note_id = int(note_id)

                    # Lade die Notiz aus der Datenbank
                    conn = sqlite3.connect("notizbuch.db")  # Verbindung zur SQLite-Datenbank öffnen
                    c = conn.cursor()  # Cursor-Objekt erstellen, um SQL-Befehle auszuführen
                    c.execute("SELECT content FROM notes WHERE id = ?", (selected_note_id,))  
                    note = c.fetchone()  # Das erste Ergebnis der Abfrage abrufen
                    conn.close()  # Datenbankverbindung schließen


                    if note:
                        results_text.delete("1.0", tk.END)  # Alte Notiz entfernen
                        results_text.insert("1.0", note[0])  # Neue Notiz einfügen
    except Exception as e:
        print("Fehler beim Auswählen der Notiz:", e)




# Funktion zum Fettschreiben des markierten Textes
def make_bold():
    try:
        selected_text = content_text.tag_ranges(tk.SEL)
        if selected_text:
            content_text.tag_add("bold", *selected_text)
    except:
        messagebox.showwarning("Fehler", "Bitte Text markieren, um ihn fett zu machen!")



# Markdown Formatierung für Fett
def insert_markdown_text(text_widget, content):
    bold_pattern = r"\*\*(.*?)\*\*|__(.*?)__"
    
    last_index = 0  # Position im Originaltext
    for match in re.finditer(bold_pattern, content):
        start, end = match.span()  # Position des Matches im String
        
        # Normalen Text vor dem fettgedruckten Bereich einfügen
        normal_text = content[last_index:start]
        text_widget.insert(tk.END, normal_text)  

        # Fettgedruckten Text einfügen & formatieren
        bold_text = match.group(1) if match.group(1) else match.group(2)  
        bold_start_index = text_widget.index(tk.END)  
        text_widget.insert(tk.END, bold_text, "bold")

        # Position nach dem fettgedruckten Bereich aktualisieren
        last_index = end

    # Falls nach dem letzten fettgedruckten Wort noch normaler Text existiert
    remaining_text = content[last_index:]
    if remaining_text:
        text_widget.insert(tk.END, remaining_text)


# GUI erstellen
root = tk.Tk()
root.title("Fäbu's Knowledgebase")
root.geometry("1000x800")
root.configure(bg=BG_COLOR)

# Spalten-Skalierung
root.columnconfigure(0, weight=1)  # Linke Spalte (z. B. für "Aktualisieren"-Button)
root.columnconfigure(1, weight=1)  # Rechte Spalte (z. B. für "Löschen"-Button)

# Zeilen-Skalierung
root.rowconfigure(3, weight=1)  # Z. B. für das Notizfeld oder Suchbereich
root.rowconfigure(10, weight=2)  # Größerer Gewichtung für das Suchergebnis



# Titel-Eingabe
tk.Label(root, text="Titel:", bg=BG_COLOR, fg=LABEL_TEXT_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
title_entry = tk.Entry(root, bg=ENTRY_BG, fg=ENTRY_FG)
title_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

# Notiz-Eingabe
tk.Label(root, text="Notiz:", bg=BG_COLOR, fg=LABEL_TEXT_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
content_text = tk.Text(root, height=5, bg=ENTRY_BG, fg=ENTRY_FG)
content_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
content_text.tag_configure("bold", font=("Arial", 10, "bold"))  # Text-Tag für fette Schrift definieren

# Suchfeld
tk.Label(root, text="Suchen:", bg=BG_COLOR, fg=LABEL_TEXT_COLOR).grid(row=7, column=0, sticky="w", padx=10, pady=5)
search_entry = tk.Entry(root, bg=ENTRY_BG, fg=ENTRY_FG)
search_entry.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

# Suchergebnisse (editierbar)
tk.Label(root, text="Suchergebnisse:", bg=BG_COLOR, fg=LABEL_TEXT_COLOR).grid(row=9, column=0, sticky="w", padx=10, pady=5)
results_text = tk.Text(root, height=10, bg=ENTRY_BG, fg=ENTRY_FG)
results_text.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
results_text.tag_configure("bold", font=("Arial", 10, "bold"))  # Text-Tag für fette Schrift definieren (nach der Erstellung von results_text)



# Buttons
# "Speichern-Button Frame für den Button erstellen
button_frame = tk.Frame(root)
button_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# "Speichern-Button" in den Frame setzen mit fester Breite
save_button = tk.Button(button_frame, text="Speichern", command=add_note, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, width=15)  # Breite ca. 5 cm
save_button.pack()

# "Speichen-Button" Frame auf feste Größe setzen (Bleibt über zwei Spalten mittig)
button_frame.grid_propagate(False)
button_frame.configure(width=120, height=30)  # Breite für 2 Spalten (~6 cm)

# Frame für den "Aktualisieren"-Button erstellen
update_frame = tk.Frame(root)
update_frame.grid(row=11, column=0, padx=10, pady=5)

# "Aktualisieren"-Button in den Frame setzen mit fester Breite
update_button = tk.Button(update_frame, text="Aktualisieren", command=update_note, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, width=15)
update_button.pack(anchor="center")

# "Aktuallisieren" Frame auf feste Größe setzen
update_frame.grid_propagate(False)
update_frame.configure(width=120, height=30)  # Breite ~6 cm

# Frame für den "Löschen"-Button erstellen
delete_frame = tk.Frame(root)
delete_frame.grid(row=11, column=1, padx=10, pady=5)

# "Löschen"-Button in den Frame setzen mit fester Breite
delete_button = tk.Button(delete_frame, text="Löschen", command=delete_note, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, width=15)
delete_button.pack(anchor="center")

# "Löschen" Frame auf feste Größe setzen
delete_frame.grid_propagate(False)
delete_frame.configure(width=120, height=30)  # Breite ~6 cm

# Fett-Button hinzufügen
bold_button = tk.Button(root, text="Fett", command=make_bold, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, width=10)
bold_button.grid(row=4, column=1, columnspan=2, pady=5)




# Live-Suche aktivieren (bei jeder Tasteneingabe wird search_notes() aufgerufen)
search_entry.bind("<KeyRelease>", lambda event: search_notes())

# Markierungsstil setzen (Jetzt nach der Erstellung von results_text!)
results_text.tag_config("highlight", background=HIGHLIGHT_COLOR, foreground="black")

# Event-Binding für das Anklicken einer Notiz
results_text.bind("<ButtonRelease-1>", select_note)



# Datenbank initialisieren
init_db()

# GUI starten
root.mainloop()
