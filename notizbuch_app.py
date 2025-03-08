import config
import re
import io
import tkinter as tk
from tkinter import messagebox
from datenbank import Datenbank
from notiz import Notiz
from PIL import Image, ImageTk, ImageGrab


class NotizbuchApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fäbu's Knowledgebase")
        self.root.geometry("900x650")
        self.root.configure(bg=config.BG_COLOR)


        self.db = Datenbank()
        self.selected_note_id = None  # Speichert die ID der ausgewählten Notiz


        self.create_widgets()
        self.db.init_db()  # Datenbank initialisieren



    def create_widgets(self):

        # Spalten-Skalierung
        self.root.columnconfigure(0, weight=1)  # Linke Spalte (z. B. für "Aktualisieren"-Button)
        self.root.columnconfigure(1, weight=1)  # Aktualisieren Button
        self.root.columnconfigure(2, weight=1)  # Löschen Button
        self.root.columnconfigure(3, weight=1)  # Fett Button
        self.root.columnconfigure(4, weight=1)  # Rechte Spalte (Screenshot)

        # Zeilen-Skalierung
        self.root.rowconfigure(3, weight=1)  # Z. B. für das Notizfeld oder Suchbereich
        self.root.rowconfigure(10, weight=2)  # Größere Gewichtung für das Suchergebnis
    

        # Titel-Eingabe
        tk.Label(self.root, text="Titel:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_entry = tk.Entry(self.root, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.title_entry.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(10, 5), pady=5)

        # Notiz-Eingabe
        tk.Label(self.root, text="Notiz:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.content_text = tk.Text(self.root, height=10, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.content_text.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=(10,5), pady=5)

        # Suchfeld
        tk.Label(self.root, text="Suchen:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.search_entry = tk.Entry(self.root, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.search_entry.grid(row=8, column=0, columnspan=5, sticky="ew", padx=10, pady=5)

        self.search_entry.bind("<KeyRelease>", lambda event: self.search_notes())

        # Suchergebnisse
        tk.Label(self.root, text="Suchergebnisse:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=9, column=0, columnspan=3, sticky="w", padx=10, pady=5)
        self.results_text = tk.Text(self.root, height=30, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.results_text.grid(row=10, column=0, columnspan=5, sticky="nsew", padx=10, pady=5)

        self.results_text.bind("<ButtonRelease-1>", lambda event: (self.select_note(event), self.select_note_screenshot(event)))
        self.results_text.tag_configure("bold", font=("Arial", 10, "bold")) # Tag für Markdown-Fettformatierung setzen
        self.results_text.tag_configure("highlight", background=config.HIGHLIGHT_COLOR, foreground="black") # Wird fpr das Highlight verwendet


        # Screenshot-Anzeige
        tk.Label(self.root, text="Screenshot-Vorschau:", bg=config.BG_COLOR, fg=config.LABEL_TEXT_COLOR).grid(row=0, column=4, sticky="w", padx=10, pady=5)
        self.screenshot_canvas = tk.Canvas(self.root, bg="white", relief="solid", bd=1)
        self.screenshot_canvas.grid(row=1, column=4, rowspan=3, padx=(5,10), pady=5, sticky="nsew")

        self.screenshot_canvas.bind("<Button-1>", self.paste_screenshot)


        # Event für Fenstergröße-Änderung binden
        self.root.bind("<Configure>", self.resize_canvas)

        self.image_on_canvas = None  # Referenz für das Bild auf dem Canvas
        self.screenshot_tk = None  # Referenz für das skaliertes Bild
        self.temp_image_data = None  # Temporäre Speicherung des Bildes

        # Buttons
        # Frame für "Speichern"-Button erstellen
        save_frame = tk.Frame(self.root)
        save_frame.grid(row=4, column=0, pady=5)
        save_button = tk.Button(save_frame, text="Speichern", command=self.add_note, bg=config.BTN_COLOR, fg=config.BTN_TEXT_COLOR, width=15)
        save_button.pack(anchor="center")

        # Frame für "Aktualisieren"-Button erstellen
        update_frame = tk.Frame(self.root)
        update_frame.grid(row=4, column=1, pady=5)
        update_button = tk.Button(update_frame, text="Aktualisieren", command=self.update_note, bg=config.BTN_COLOR, fg=config.BTN_TEXT_COLOR, width=15)
        update_button.pack(anchor="center")

        # Frame für "Löschen"-Button erstellen
        delete_frame = tk.Frame(self.root)
        delete_frame.grid(row=4, column=2, pady=5)
        delete_button = tk.Button(delete_frame, text="Löschen", command=self.delete_note, bg=config.BTN_COLOR, fg=config.BTN_TEXT_COLOR, width=15)
        delete_button.pack(anchor="center")

        # Frame für "Fett"-Button erstellen
        bold_frame = tk.Frame(self.root)
        bold_frame.grid(row=4, column=3, pady=5)
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
            # **Schritt 1: Notiz speichern (ohne Screenshot)**
            note = Notiz(title, content)
            note_id = self.db.add_note(note)  # Notiz-ID abrufen



            # **Schritt 2: Prüfen, ob ein Screenshot in der Zwischenablage ist**
            screenshot_saved = False
            if hasattr(self, 'temp_image_data') and self.temp_image_data:
                self.db.speichere_screenshot(note_id, self.temp_image_data)
                screenshot_saved = True

            # **Schritt 3: Eingabefelder & Screenshot-Feld zurücksetzen**
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.screenshot_canvas.delete("all")  # Screenshot-Feld leeren
            self.temp_image_data = None  # Temporäre Bild-Daten entfernen


            # **Schritt 4: Erfolgsnachricht & UI-Aktualisierung**
            messagebox.showinfo("Erfolg", "Notiz und Screenshot gespeichert!" if screenshot_saved else "Notiz gespeichert!")

            self.search_notes()  # Notizliste aktualisieren


        else:
            messagebox.showwarning("Fehler", "Titel und Inhalt dürfen nicht leer sein!")



        # Notiz aktualisieren
    def update_note(self):
        if self.selected_note_id is None:
            messagebox.showwarning("Fehler", "Keine Notiz ausgewählt!")
            return
        
        # Hole die aktualisierten Werte aus den Eingabefeldern
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()


        # Falls ein Screenshot eingefügt wurde, diesen speichern
        image_blob = self.temp_image_data if hasattr(self, "temp_image_data") else None

        if title and content:
             # Notiz und ggf. Screenshot in der Datenbank aktualisieren
            self.db.update_note(self.selected_note_id, title, content, image_blob)

            messagebox.showinfo("Erfolg", "Notiz und Screenshot aktualisiert!")

            # Suche neu laden, damit die Änderung sichtbar ist
            self.search_notes()
            self.selected_note_id = None  # ID zurücksetzen
            self.title_entry.delete(0, tk.END)  # Titel-Feld leeren
            self.content_text.delete("1.0", tk.END)  # Inhalt-Feld leeren
            self.screenshot_canvas.delete("all")  # Canvas leeren
            self.temp_image_data = None  # Temporäre Bild-Daten entfernen
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
                        self.note_fully_selected = True  # Jetzt kann aktualisiert werden

                        # Lade die Notiz aus der Datenbank
                        title, content = self.db.get_note(self.selected_note_id)


                        if title and content:


                            # Eingabefelder aktualisieren
                            self.title_entry.delete(0, tk.END)
                            self.title_entry.insert(0, title)  # Titel setzen

                            self.content_text.delete("1.0", tk.END)
                            self.content_text.insert("1.0", content)  # Inhalt setzen

        except Exception as e:
            print("Fehler beim Auswählen der Notiz:", e)



    def select_note_screenshot(self, event):
        """Lädt den Screenshot der ausgewählten Notiz bei einfachem Klick."""
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

                        # Screenshot aus der Datenbank laden
                        image_blob = self.db.lade_screenshot(self.selected_note_id)

                        if image_blob:

                            image_data = io.BytesIO(image_blob)
                            img = Image.open(image_data)

                            # Temporäre Bilddaten speichern, damit es auch bei Resize funktioniert
                            with io.BytesIO() as output:
                                img.save(output, format="PNG")
                                self.temp_image_data = output.getvalue()

                            # Screenshot im Canvas anzeigen
                            self.display_screenshot(img)
                        else:
                            # Falls kein Screenshot vorhanden, Canvas leeren
                            self.screenshot_canvas.delete("all")
                            self.temp_image_data = None  # Keine Bilddaten gespeichert

        except Exception as e:
            print("Fehler beim Laden des Screenshots:", e)




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



        #Markiert den ausgewählten Text als fett (setzt ** darum) und formatiert ihn visuell.
    def make_bold(self):
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
    def insert_markdown_text(self, text_widget, content):

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




    def paste_screenshot(self, event=None):
        """Holt den Screenshot aus der Zwischenablage und speichert ihn."""
        img = ImageGrab.grabclipboard()  # Screenshot aus Zwischenablage holen

        if img: 
            # **Feld leeren, falls bereits ein Screenshot vorhanden ist**
            self.screenshot_canvas.delete("all")  
            self.temp_image_data = None  # Temporäre Bild-Daten entfernen

            with io.BytesIO() as output:
                img.save(output, format="PNG")
                self.temp_image_data = output.getvalue()  # **Temporär speichern, aber nicht in DB!**

            # Bild im Canvas anzeigen
            self.display_screenshot(img)

            print("Screenshot eingefügt, wird aber erst beim Speichern gesichert.")
        else:
            messagebox.showwarning("Fehler", "Kein Bild in der Zwischenablage gefunden!")


    def lade_und_zeige_screenshot(self):
        """Lädt den letzten Screenshot aus der Datenbank und zeigt ihn im Canvas an."""
        image_blob = self.db.lade_letzten_screenshot()
        if image_blob:
            image_data = io.BytesIO(image_blob)
            img = Image.open(image_data)
            self.display_screenshot(img)
        else:
            self.screenshot_canvas.delete("all")  # Falls kein Bild existiert, bleibt das Feld leer

    def display_screenshot(self, img):
        """Zeigt das übergebene Bild im Canvas an und skaliert es proportional."""
        canvas_width = self.screenshot_canvas.winfo_width()
        canvas_height = self.screenshot_canvas.winfo_height()

        if canvas_width < 1 or canvas_height < 1:
            return  # Verhindert Fehler, wenn das Fenster zu klein ist

        # Bild proportional skalieren
        img_ratio = img.width / img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        self.screenshot_tk = ImageTk.PhotoImage(img)

        # Altes Bild vom Canvas entfernen und neues zentriert hinzufügen
        self.screenshot_canvas.delete("all")
        x_center = canvas_width // 2
        y_center = canvas_height // 2
        self.screenshot_canvas.create_image(x_center, y_center, image=self.screenshot_tk, anchor="center")


    def resize_canvas(self, event):
        """ Verzögert die Neuskalierung, um Performance-Probleme zu vermeiden """
        if hasattr(self, "resize_after_id"):
            self.root.after_cancel(self.resize_after_id)  # Vorherigen Aufruf abbrechen

        self.resize_after_id = self.root.after(100, self._perform_resize)  # Nach 100ms skalieren

    def _perform_resize(self):
        """ Führt die tatsächliche Skalierung des Bildes durch """
        if self.temp_image_data:
            img = Image.open(io.BytesIO(self.temp_image_data))
            self.display_screenshot(img)  # Skaliert das Bild erneut




    def run(self):
        self.root.mainloop()
