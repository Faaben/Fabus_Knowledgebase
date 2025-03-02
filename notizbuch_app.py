import config
import re
import tkinter as tk
from tkinter import messagebox
from datenbank import Datenbank
from notiz import Notiz


class NotizbuchApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fäbu's Knowledgebase")
        self.root.geometry("1000x800")
        self.root.configure(bg=config.BG_COLOR)


        self.db = Datenbank()
        self.selected_note_id = None  # Speichert die ID der ausgewählten Notiz

        self.create_widgets()
        self.db.init_db()  # Datenbank initialisieren

    def create_widgets(self):

        # Spalten-Skalierung
        self.root.columnconfigure(0, weight=1)  # Linke Spalte (z. B. für "Aktualisieren"-Button)
        self.root.columnconfigure(1, weight=1)  # Rechte Spalte (z. B. für "Löschen"-Button)

        # Zeilen-Skalierung
        self.root.rowconfigure(3, weight=1)  # Z. B. für das Notizfeld oder Suchbereich
        self.root.rowconfigure(10, weight=2)  # Größere Gewichtung für das Suchergebnis

        # Titel-Eingabe
        tk.Label(self.root, text="Titel:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_entry = tk.Entry(self.root, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.title_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Notiz-Eingabe
        tk.Label(self.root, text="Notiz:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.content_text = tk.Text(self.root, height=5, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.content_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.content_text.tag_configure("bold", font=("Arial", 10, "bold")) # Tag für Fett-Markierung im Eingabefeld setzen!

        # Suchfeld
        tk.Label(self.root, text="Suchen:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.search_entry = tk.Entry(self.root, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.search_entry.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.search_entry.bind("<KeyRelease>", lambda event: self.search_notes())

        # Suchergebnisse
        tk.Label(self.root, text="Suchergebnisse:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=9, column=0, sticky="w", padx=10, pady=5)
        self.results_text = tk.Text(self.root, height=10, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.results_text.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.results_text.bind("<ButtonRelease-1>", self.select_note)
        self.results_text.tag_configure("bold", font=("Arial", 10, "bold")) # Tag für Markdown-Fettformatierung setzen
        self.results_text.tag_configure("highlight", background=config.HIGHLIGHT_COLOR, foreground="black") # Wird fpr das Highlight verwendet

        # Buttons
        # Frame für "Speichern"-Button erstellen
        save_frame = tk.Frame(self.root)
        save_frame.grid(row=4, column=0, pady=5)
        save_button = tk.Button(save_frame, text="Speichern", command=self.add_note, bg=config.BTN_COLOR, fg=config.BTN_TEXT_COLOR, width=15)
        save_button.pack(anchor="center")

        # Frame für "Aktualisieren"-Button erstellen
        update_frame = tk.Frame(self.root)
        update_frame.grid(row=11, column=1, pady=5)
        update_button = tk.Button(update_frame, text="Aktualisieren", command=self.update_note, bg=config.BTN_COLOR, fg=config.BTN_TEXT_COLOR, width=15)
        update_button.pack(anchor="center")

        # Frame für "Löschen"-Button erstellen
        delete_frame = tk.Frame(self.root)
        delete_frame.grid(row=11, column=0, pady=5)
        delete_button = tk.Button(delete_frame, text="Löschen", command=self.delete_note, bg=config.BTN_COLOR, fg=config.BTN_TEXT_COLOR, width=15)
        delete_button.pack(anchor="center")

        # Frame für "Fett"-Button erstellen
        bold_frame = tk.Frame(self.root)
        bold_frame.grid(row=4, column=1, pady=5)
        bold_button = tk.Button(bold_frame, text="Fett", command=self.make_bold, bg=config.BTN_COLOR, fg=config.BTN_TEXT_COLOR, width=10)
        bold_button.pack(anchor="center")




        # Notiz hinzufügen
    def add_note(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip() 
        
        # self.content_text ist dein Tkinter Text-Widget (wo der Benutzer seine Notiz eingibt).
        # "1.0" → Beginn des Textfelds (erste Zeile, erstes Zeichen)
        # .tk.END → Ende des Textfelds (alles bis zum letzten Zeichen).

        if title and content:
            note = Notiz(title, content)
            self.db.add_note(note) # Speichert Notiz in der Datenbank

            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            messagebox.showinfo("Erfolg", "Notiz gespeichert!")
            self.search_notes()
        else:
            messagebox.showwarning("Fehler", "Titel und Inhalt dürfen nicht leer sein!")



        # Notiz aktualisieren
    def update_note(self):
        global selected_note_id
        if self.selected_note_id is None:
            messagebox.showwarning("Fehler", "Keine Notiz ausgewählt!")
            return
        
        # Extrahiere die geänderten Inhalte aus results_text
        content = self.results_text.get("1.0", tk.END).strip()

        if content:
            self.db.update_note(self.selected_note_id, content)
            messagebox.showinfo("Erfolg", "Notiz aktualisiert!")

            # Suche neu laden, damit die Änderung sichtbar ist
            self.search_notes()
            self.selected_note_id = None  # ID zurücksetzen
        else:
            messagebox.showwarning("Fehler", "Inhalt darf nicht leer sein!")




        # Notizen suchen
    def search_notes(self):
        query = self.search_entry.get().strip().lower()
        self.results_text.tag_remove("highlight", "1.0", tk.END)  # Vorherige Markierungen entfernen
        self.results_text.delete("1.0", tk.END)  # Alte Suchergebnisse löschen

        if not query:
            self.results_text.insert(tk.END, "Bitte einen Suchbegriff eingeben.\n")
            return

        results = self.db.search_notes(query)

        if not results:
            self.results_text.insert(tk.END, "Keine Notizen gefunden.\n")
            return

        # Ergebnisse anzeigen und Highlight setzen
        for note_id, title, content in results:
            start_index = self.results_text.index(tk.END)  # Startposition im Text

            # ID normal einfügen
            self.results_text.insert(tk.END, f"ID: {note_id} | Titel: ")

            # Titel fett machen
            self.results_text.insert(tk.END, f"{title}\n", "bold")

            # Hier wird Markdown für den Inhalt angewendet:
            self.insert_markdown_text(self.results_text, content)

            self.results_text.insert(tk.END, f"\n\n {'-'*40}\n\n")

            # Hervorhebung durchführen
            self.search_and_highlight(query, start_index)


        # Notiz auswählen, damit man weiss welchen Teil man aktuallisieren will.
    def select_note(self, event):
        try:
            # Bestimme, welche Zeile angeklickt wurde
            index = self.results_text.index("@%d,%d" % (event.x, event.y))  
            line_start = self.results_text.index(index + " linestart")
            line_end = self.results_text.index(index + " lineend")
            line_text = self.results_text.get(line_start, line_end).strip()

            # Prüfen, ob die Zeile eine ID enthält (Format: "ID: X | Titel: XYZ")
            if line_text.startswith("ID:"):
                parts = line_text.split("|")
                if len(parts) > 1:
                    note_id = parts[0].replace("ID:", "").strip()
                    
                    # Speichert die ausgewählte Notiz-ID
                    if note_id.isdigit():
                        self.selected_note_id = int(note_id)

                        # Lade die Notiz aus der Datenbank
                        note_content = self.db.get_note_content(self.selected_note_id)


                        if note_content:
                            self.results_text.delete("1.0", tk.END)  # Alte Notiz entfernen

                            # Fett-Markierung in `**text**` umwandeln
                            note_content = self.convert_bold_to_markdown(note_content)


                            # Wichtig: Den umgewandelten Text wieder anzeigen!
                            self.results_text.insert("1.0", note_content)

                            # self.insert_markdown_text(self.results_text, note_content)  # Markdown-Formatierung anwenden
        except Exception as e:
            print("Fehler beim Auswählen der Notiz:", e)




    def convert_bold_to_markdown(self, content):
        """Erkennt Fett-Markierungen im Tkinter-Text und ersetzt sie durch **text** für Markdown."""
        
        # Alle fett markierten Textstellen finden
        bold_ranges = self.results_text.tag_ranges("bold")
        
        # Falls keine fett formatierten Bereiche vorhanden sind, einfach den Inhalt zurückgeben
        if not bold_ranges:
            return content

        # Durch alle fett markierten Bereiche gehen
        for i in range(0, len(bold_ranges), 2):
            start = bold_ranges[i]   # Startposition
            end = bold_ranges[i + 1] # Endposition

            # Extrahiere den fett markierten Text
            bold_text = self.results_text.get(start, end)

            # Ersetze den fett formatierten Bereich durch **text**
            self.results_text.delete(start, end)
            self.results_text.insert(start, f"**{bold_text}**")

        # Rückgabe des vollständigen, umgewandelten Inhalts als Markdown
        return self.results_text.get("1.0", tk.END).strip()











        # Notiz löschen
    def delete_note(self):
        if self.selected_note_id is None:
            messagebox.showwarning("Fehler", "Keine Notiz ausgewählt!")
            return
        
        # Sicherheitsabfrage, um versehentliches Löschen zu verhindern
        confirm = messagebox.askyesno("Löschen bestätigen", "Möchtest du diese Notiz wirklich löschen?")
        
        if confirm:
            self.db.delete_note(self.selected_note_id)
            messagebox.showinfo("Erfolg", "Notiz gelöscht!")

            # Suchergebnisse aktualisieren
            self.search_notes()

            # ID zurücksetzen, damit kein weiterer falscher Löschvorgang passiert
            self.selected_note_id = None

            # Eingabefelder leeren
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.results_text.delete("1.0", tk.END)  # Falls die Notiz direkt im Suchfeld bearbeitet wurde, auch hier löschen




        # Notizen Highlighten        
    def search_and_highlight(self, query, start_index):
        end_index = self.results_text.index(tk.END)  # Ende des Textfelds

        pos = self.results_text.search(query, start_index, stopindex=end_index, nocase=True)
        while pos:
            end_pos = f"{pos}+{len(query)}c"
            self.results_text.tag_add("highlight", pos, end_pos)
            pos = self.results_text.search(query, end_pos, stopindex=end_index, nocase=True)




    def make_bold(self):
        """Markiert den ausgewählten Text als fett (setzt ** darum) und formatiert ihn visuell."""
        try:
            selected_range = self.content_text.tag_ranges(tk.SEL)
            if selected_range:
                start, end = selected_range
                selected_text = self.content_text.get(start, end)


                # Prüfen, ob der Text bereits fett ist (enthält ** oder __)
                if selected_text.startswith("**") and selected_text.endswith("**"):
                    # Falls ja, entferne die Markdown-Sternchen und Fett-Tag
                    new_text = selected_text[2:-2]

                else:
                    # Falls nicht, füge ** hinzu und setze die Fett-Markierung
                    new_text = f"**{selected_text}**"



                    # Ersetze den markierten Text durch die neue Markdown-Formatierung           
                    self.content_text.delete(start, end)
                    self.content_text.insert(start, new_text)



            else:
                print("Kein Text markiert!")

        except:
            messagebox.showwarning("Fehler", "Bitte Text markieren, um ihn fett zu machen!")




    # Markdown Formatierung für Fett
    def insert_markdown_text(self, text_widget, content, from_make_bold=False):

        bold_pattern = r"\*\*(.*?)\*\*|__(.*?)__"
        
        last_index = 0  # Position im Originaltext
        for match in re.finditer(bold_pattern, content): # Suche nach dem **fett**
            start, end = match.span()  # Position des Matches im String
            
            # Normalen Text vor dem fettgedruckten Bereich einfügen
            normal_text = content[last_index:start]
            text_widget.insert(tk.END, normal_text)  

            # Fettgedruckten Text einfügen & formatieren
            bold_text = match.group(1) if match.group(1) else match.group(2)
            text_widget.insert(tk.END, bold_text, "bold") # Fett markieren

            # Position nach dem fettgedruckten Bereich aktualisieren
            last_index = end

        # Falls nach dem letzten fettgedruckten Wort noch normaler Text existiert
        remaining_text = content[last_index:]
        if remaining_text:
            text_widget.insert(tk.END, remaining_text)


    def run(self):
        self.root.mainloop()
