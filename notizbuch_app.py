import config
import re
import io
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import customtkinter as ctk
from datenbank import Datenbank
from notiz import Notiz
from PIL import Image, ImageTk, ImageGrab
from CTkMessagebox import CTkMessagebox  # Importiere die CustomTkinter Messagebox
from custom_messagebox import CustomMessagebox

class NotizbuchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fäbu's Knowledgebase")
        self.root.geometry("900x650")

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
        ctk.CTkLabel(self.root, text="Titel:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_entry = ctk.CTkEntry(self.root)
        self.title_entry.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(10, 5), pady=5)

        # Notiz-Eingabe
        ctk.CTkLabel(self.root, text="Notiz:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.content_text = tk.Text(self.root, height=10, bg=config.ENTRY_BG, fg=config.ENTRY_FG, insertbackground=config.INSERT)
        self.content_text.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=(10,5), pady=5)

        # Suchfeld
        ctk.CTkLabel(self.root, text="Suchen:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.search_entry = ctk.CTkEntry(self.root)
        self.search_entry.grid(row=8, column=0, columnspan=5, sticky="ew", padx=10, pady=5)

        self.search_entry.bind("<KeyRelease>", lambda event: self.search_notes())

        # Suchergebnisse
        ctk.CTkLabel(self.root, text="Suchergebnisse:").grid(row=9, column=0, columnspan=3, sticky="w", padx=10, pady=5)
        self.results_text = tk.Text(self.root, height=30, bg=config.ENTRY_BG, fg=config.ENTRY_FG)
        self.results_text.grid(row=10, column=0, columnspan=5, sticky="nsew", padx=10, pady=5)

        self.results_text.bind("<ButtonRelease-1>", lambda event: self.select_note(event))
        self.results_text.tag_configure("bold", font=("Arial", 10, "bold")) # Tag für Markdown-Fettformatierung setzen
        self.results_text.tag_configure("highlight", background=config.HIGHLIGHT_COLOR, foreground="black") # Wird fpr das Highlight verwendet

        # Screenshot-Anzeige
        ctk.CTkLabel(self.root, text="Screenshot-Vorschau:",).grid(row=0, column=4, sticky="w", padx=10, pady=5)
        self.screenshot_canvas = ctk.CTkCanvas(self.root, bg="white", width=200, height=150)
        self.screenshot_canvas.grid(row=1, column=4, rowspan=4, padx=(5,10), pady=5, sticky="nsew")
        self.screenshot_canvas.bind("<Button-1>", self.paste_screenshot)

        # Event für Fenstergröße-Änderung binden
        self.root.bind("<Configure>", self.resize_canvas)

        self.image_on_canvas = None  # Referenz für das Bild auf dem Canvas
        self.screenshot_tk = None  # Referenz für das skaliertes Bild
        self.temp_image_data = None  # Temporäre Speicherung des Bildes

        # Buttons in einem Frame
        button_frame = ctk.CTkFrame(self.root)
        button_frame.grid(row=4, column=0, columnspan=4, pady=5, sticky="ew")

        ctk.CTkButton(button_frame, text="Speichern", command=self.add_note, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Aktualisieren", command=self.update_note, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Löschen", command=self.delete_note, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Fett", command=self.make_bold, width=80).pack(side="right", padx=5)



        # Notiz hinzufügen
    def add_note(self):
        # Falls eine Notiz ausgewählt ist → Fehlermeldung anzeigen
        if self.selected_note_id is not None:
            CTkMessagebox(title="Fehler", message="Eine bestehende Notiz kann nicht gespeichert werden! Bitte aktualisiere sie stattdessen.", icon="warning", option_1="OK")
            return
        
        title = self.title_entry.get()
        content = self.content_text.get("1.0", "end").strip() 
        # self.content_text ist dein Tkinter Text-Widget (wo der Benutzer seine Notiz eingibt).
        # "1.0" → Beginn des Textfelds (erste Zeile, erstes Zeichen)
        # ."end" → Ende des Textfelds (alles bis zum letzten Zeichen).

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
            self.title_entry.delete(0, "end")
            self.content_text.delete("1.0", "end")
            self.screenshot_canvas.delete("all")  # Screenshot-Feld leeren
            self.temp_image_data = None  # Temporäre Bild-Daten entfernen

            # **Schritt 4: Erfolgsnachricht & UI-Aktualisierung**
            #message = "Notiz und Screenshot gespeichert!" if screenshot_saved else "Notiz gespeichert!"
            #CTkMessagebox(title="Erfolg", message=message, icon="check", option_1="OK")
            self.show_success_message("Notiz erfolgreich gespeichert!")


            self.search_notes()  # Notizliste aktualisieren

        else:
            CTkMessagebox(title="Fehler", message="Titel und Inhalt dürfen nicht leer sein!", icon="warning", option_1="OK")


        # Notiz aktualisieren
    def update_note(self):
        if self.selected_note_id is None:
            CTkMessagebox(title="Fehler", message="Keine Notiz ausgewählt!", icon="warning", option_1="OK")
            return
        
        # Hole die aktualisierten Werte aus den Eingabefeldern
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", "end").strip()

        # Falls ein Screenshot eingefügt wurde, diesen speichern
        image_blob = self.temp_image_data if hasattr(self, "temp_image_data") else None

        if title and content:
             # Notiz und ggf. Screenshot in der Datenbank aktualisieren
            self.db.update_note(self.selected_note_id, title, content, image_blob)

            #CTkMessagebox(title="Erfolg", message="Notiz und Screenshot aktualisiert!", icon="check", option_1="OK")
            self.show_success_message("Notiz wurde aktualisiert!")

            # Suche neu laden, damit die Änderung sichtbar ist
            self.search_notes()
            self.selected_note_id = None  # ID zurücksetzen
            self.title_entry.delete(0, "end")  # Titel-Feld leeren
            self.content_text.delete("1.0", "end")  # Inhalt-Feld leeren
            self.screenshot_canvas.delete("all")  # Canvas leeren
            self.temp_image_data = None  # Temporäre Bild-Daten entfernen
        else:
            CTkMessagebox(title="Fehler", message="Inhalt darf nicht leer sein!", icon="warning", option_1="OK")


        # Notizen suchen
    def search_notes(self):
        query = self.search_entry.get().strip().lower()
        self.results_text.tag_remove("highlight", "1.0", "end")  # Vorherige Markierungen entfernen
        self.results_text.delete("1.0", "end")  # Alte Suchergebnisse löschen

        # Falls das Suchfeld leer ist → Eingabefelder zurücksetzen
        if not query:
            self.clear_input_fields()  # Neue Methode, die Titel, Inhalt & Screenshot leert
            return

        results = self.db.search_notes(query)

        # Ergebnisse anzeigen und Highlight setzen
        for note_id, title, content in results:
            start_index = self.results_text.index("end")  # Startposition im Text

            # ID normal einfügen
            self.results_text.insert("end", f"ID: {note_id} | Titel: ")

            # Titel fett machen
            self.results_text.insert("end", f"{title}\n", "bold")

            # Hier wird Markdown für den Inhalt angewendet:
            self.insert_markdown_text(self.results_text, content)

            self.results_text.insert("end", f"\n\n {'-'*40}\n\n")

            # Hervorhebung durchführen
            self.search_and_highlight(query, start_index)


    def clear_input_fields(self):
        """Leert die Eingabefelder für einen neuen Notizeintrag."""
        self.title_entry.delete(0, "end")  # Titel-Feld leeren
        self.content_text.delete("1.0", "end")  # Inhalt-Feld leeren
        self.screenshot_canvas.delete("all")  # Screenshot-Feld leeren
        self.temp_image_data = None  # Temporäre Bild-Daten entfernen


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
                            self.title_entry.delete(0, "end")
                            self.title_entry.insert(0, title)  # Titel setzen

                            self.content_text.delete("1.0", "end")
                            self.content_text.insert("1.0", content)  # Inhalt setzen

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
            print("Fehler beim Laden der Notiz/Screenshot:", e)


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
        return self.results_text.get("1.0", "end").strip()


        # Notiz löschen
    def delete_note(self):
        if self.selected_note_id is None:
            CTkMessagebox(title="Fehler", message="Keine Notiz ausgewählt!", icon="warning", option_1="OK")
            return
        
        # Sicherheitsabfrage: Bestätigt der Nutzer das Löschen?
        #confirm = CTkMessagebox(
            #title="Löschen bestätigen",
            #message="Möchtest du diese Notiz wirklich löschen?",
            #icon="warning",
            #option_1="Ja",
            #option_2="Nein"
        #).get()
        confirm = self.show_confirmation("Möchtest du diese Notiz wirklich löschen?")
        if confirm == "Ja":
            self.db.delete_note(self.selected_note_id)
            self.show_success_message("Notiz gelöscht!")


        
        #if confirm:
            #self.db.delete_note(self.selected_note_id)
            #CTkMessagebox(title="Erfolg", message="Notiz gelöscht!", icon="check", option_1="OK")



            # Suchergebnisse aktualisieren
            self.search_notes()

            # ID zurücksetzen, damit kein weiterer falscher Löschvorgang passiert
            self.selected_note_id = None

            # Eingabefelder leeren
            self.title_entry.delete(0, "end")
            self.content_text.delete("1.0", "end")
            self.results_text.delete("1.0", "end")  # Falls die Notiz direkt im Suchfeld bearbeitet wurde, auch hier löschen


        # Notizen Highlighten        
    def search_and_highlight(self, query, start_index):
        end_index = self.results_text.index("end")  # Ende des Textfelds
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
            CTkMessagebox(title="Fehler", message="Kein Bild in der Zwischenablage gefunden!", icon="warning", option_1="OK")


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



    def show_success_message(self, text):
        """Zeigt eine OK-Messagebox"""
        msgbox = CustomMessagebox(self.root, title="Erfolg", message=text, buttons=("OK",))
        self.root.wait_window(msgbox)  # Warten, bis das Fenster geschlossen wird

    def show_confirmation(self, text):
        #Zeigt eine Ja/Nein-Messagebox und gibt das Ergebnis zurück
        msgbox = CustomMessagebox(self.root, title="Bestätigung", message=text, buttons=("Ja", "Nein"))
        self.root.wait_window(msgbox)  # Warten, bis das Fenster geschlossen wird
        return msgbox.result  # Gibt "Ja" oder "Nein" zurück



    def run(self):
        self.root.mainloop()
