import config
import re
import io
import tkinter as tk
from tkinter import *
import customtkinter as ctk
from datenbank import Datenbank
from notiz import Notiz
from PIL import Image, ImageTk, ImageGrab
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
        self.search_notes()
    


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
        self.content_text = tk.Text(self.root, height=10, bg=config.ENTRY_BG, fg=config.ENTRY_FG, insertbackground=config.INSERT, font=config.FONT)
        self.content_text.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=(10,5), pady=5)

        # Suchfeld
        ctk.CTkLabel(self.root, text="Suchen:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.search_entry = ctk.CTkEntry(self.root)
        self.search_entry.grid(row=8, column=0, columnspan=5, sticky="ew", padx=10, pady=5)

        self.search_entry.bind("<KeyRelease>", lambda event: self.search_notes())

        # Suchergebnisse
        ctk.CTkLabel(self.root, text="Suchergebnisse:").grid(row=9, column=0, columnspan=3, sticky="w", padx=10, pady=5)
        self.results_text = tk.Text(self.root, height=30, bg=config.ENTRY_BG, fg=config.ENTRY_FG, font=config.FONT)
        self.results_text.grid(row=10, column=0, columnspan=5, sticky="nsew", padx=10, pady=5)

        self.results_text.bind("<ButtonRelease-1>", lambda event: self.select_note(event))
        self.results_text.tag_configure("bold", font=(config.FONT_FAMILY, config.FONT_SIZE, "bold")) # Tag für Markdown-Fettformatierung setzen
        self.results_text.tag_configure("italic", font=(config.FONT_FAMILY, config.FONT_SIZE, "italic"))  # Tag für Markdown-Kursivformatierung
        self.results_text.tag_configure("underline", font=(config.FONT_FAMILY, config.FONT_SIZE, "underline"))  # Tag für Markdown-Underlineformatierung
        self.results_text.tag_configure("highlight", background=config.HIGHLIGHT_COLOR, foreground="black") # Wird fpr das Highlight verwendet

        # Screenshot-Anzeige
        ctk.CTkLabel(self.root, text="Screenshot-Vorschau:",).grid(row=0, column=4, sticky="w", padx=10, pady=5)
        self.screenshot_canvas = ctk.CTkCanvas(self.root, bg="black", width=200, height=150)
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

        ctk.CTkButton(button_frame, text="Speichern", command=self.save_note, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Löschen", command=self.delete_note, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Underline", command=self.make_underline, width=80).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Kursiv", command=self.make_italic, width=80).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Fett", command=self.make_bold, width=80).pack(side="right", padx=5)


    def save_note(self):  # Neue Methode: Speichern oder Aktualisieren
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", "end").strip()
        image = self.temp_image_data if hasattr(self, "temp_image_data") else None

        if not title or not content:
            self.show_false_message("Titel und Inhalt dürfen nicht leer sein!")
            return

        note = Notiz(title, content, image)

        note_id = self.selected_note_id if self.selected_note_id is not None else None
        new_id = self.db.save_note(note_id, note)


        if note_id is None:
            self.show_success_message("Notiz erfolgreich gespeichert!")
        else:
            self.show_success_message("Notiz wurde aktualisiert!")

        self.clear_input_fields()
        self.search_notes()

        
    def search_notes(self):  # Notizen suchen
        query = self.search_entry.get().strip().lower()
        self.results_text.tag_remove("highlight", "1.0", "end")  # Vorherige Markierungen entfernen
        self.results_text.delete("1.0", "end")  # Alte Suchergebnisse löschen
   
        #if not query:  # Falls das Suchfeld leer ist → Eingabefelder zurücksetzen
            #self.clear_input_fields()  # Alle Inputfelder leeren
            #return

        results = self.db.search_notes(query)

        for note_id, title, content in results:  # Ergebnisse anzeigen und Highlight setzen
            start_index = self.results_text.index("end")  # Startposition im Text           
            self.results_text.insert("end", f"ID: {note_id} | ", "bold")  # ID normal einfügen
            self.results_text.insert("end", f"{title}\n", "bold")  # Titel fett machen
            self.insert_markdown_text(self.results_text, content)  # Hier wird Markdown für den Inhalt angewendet:
            # self.insert_italic_text(self.results_text, content)  # Hier wird Kursiv eingefügt
            self.results_text.insert("end", f"\n\n {'-'*40}\n\n")  # Abstand zwischen Notizen einfügen  

            if query:    
                self.search_and_highlight(query, start_index)  # Hervorhebung durchführen


    def select_note(self, event):  #Notiz auswählen
        # Bestimme, welche Zeile angeklickt wurde
        index = self.results_text.index("@%d,%d" % (event.x, event.y))  
        line_start = self.results_text.index(index + " linestart")
        line_end = self.results_text.index(index + " lineend")
        line_text = self.results_text.get(line_start, line_end).strip()

        if line_text.startswith("ID:"):  # Prüfen, ob die Zeile eine ID enthält (Format: "ID: X | Titel: XYZ")
            parts = line_text.split("|")
            if len(parts) > 1:
                note_id = parts[0].replace("ID:", "").strip()     
                
                if note_id.isdigit():
                    note = self.db.get_note(int(note_id))
                    #self.selected_note_id = int(note_id)  # Speichert die ausgewählte Notiz-ID
                    #title, content = self.db.get_note(self.selected_note_id)  # Lade die Notiz aus der Datenbank
                    #image_blob = self.db.lade_screenshot(self.selected_note_id)  # Screenshot aus der Datenbank laden

                    if note:
                        self.selected_note_id = note.id  # 👉 Speichert die ID im GUI-State
                        self.title_entry.delete(0, "end")  #Titel leeren
                        self.title_entry.insert(0, note.title)  # Titel einfügen

                        self.content_text.delete("1.0", "end")  #Content leeren
                        self.content_text.insert("1.0", note.content)  # Content einfügen

                        if note.image:
                            image_data = io.BytesIO(note.image)
                            img = Image.open(image_data)

                            with io.BytesIO() as output:
                                img.save(output, format="PNG")
                                self.temp_image_data = output.getvalue() # Bild temporär speichern, damit es auch bei Resize funktioniert

                            self.display_screenshot(img)  # Screenshot im Canvas anzeigen

                        else:
                            self.screenshot_canvas.delete("all") # Wenn es kein Bild hat, dann Canvas leeren
                            self.temp_image_data = None  # Keine Bilddaten gespeichert


    def delete_note(self):  # Notiz löschen
        if self.selected_note_id is None:
            self.show_false_message("Keine Notiz ausgewählt!")
            return

        confirm = self.show_confirmation("Möchtest du diese Notiz wirklich löschen?")
        if confirm == "Ja":
            self.db.delete_note(self.selected_note_id)
            self.clear_input_fields() # Eingabefelder ID löschen 
            self.show_success_message("Notiz gelöscht!")
            self.search_notes() # Suchergebnisse aktualisieren

     
    def search_and_highlight(self, query, start_index):  # Notizen Highlighten    
        end_index = self.results_text.index("end")  # Ende des Textfelds
        pos = self.results_text.search(query, start_index, stopindex=end_index, nocase=True)

        while pos:
            end_pos = f"{pos}+{len(query)}c"
            self.results_text.tag_add("highlight", pos, end_pos)
            pos = self.results_text.search(query, end_pos, stopindex=end_index, nocase=True)

        
    def make_bold(self):  # Fett markierung einfügen oder entfernen mit dem Fett-Button
        selected_range = self.content_text.tag_ranges(tk.SEL)
        if len(selected_range) == 2:  # Prüfen, ob Start- und Endposition vorhanden sind
            start, end = selected_range
            selected_text = self.content_text.get(start, end)
           
            if selected_text.strip().startswith("**") and selected_text.strip().endswith("**"):  # Prüfen, ob der Text bereits fett ist (enthält **)
                new_text = selected_text[2:-2] # Falls ja, entferne die Markdown-Sternchen und Fett-Tag

            else:       
                new_text = f"**{selected_text}**" # Falls nicht, füge ** hinzu und setze die Fett-Markierung     

            self.content_text.delete(start, end)  # Markierten Text löschen
            self.content_text.insert(start, new_text)  # Formatierter Text einfügen

        else:
            self.show_false_message("Kein Text markiert!")


    def make_italic(self):  # Kursiv-Markierung einfügen oder entfernen
        selected_range = self.content_text.tag_ranges(tk.SEL)
        if len(selected_range) == 2:
            start, end = selected_range
            selected_text = self.content_text.get(start, end)

            if selected_text.strip().startswith("*") and selected_text.strip().endswith("*"):
                new_text = selected_text[1:-1]  # Falls ja, entferne das Markdown-Sternchen

            else:
                new_text = f"*{selected_text}*"  # Falls nicht, füge * hinzu

            self.content_text.delete(start, end)
            self.content_text.insert(start, new_text)

        else:
            self.show_false_message("Kein Text markiert!")

    def make_underline(self):  # Unterstreichung mit Markdown (Alternative: _Text_)
        selected_range = self.content_text.tag_ranges(tk.SEL)
        if len(selected_range) == 2:
            start, end = selected_range
            selected_text = self.content_text.get(start, end)

            if selected_text.strip().startswith("__") and selected_text.strip().endswith("__"):
                new_text = selected_text[1:-1]  # Falls ja, entferne die Unterstriche

            else:
                new_text = f"__{selected_text}__"  # Falls nicht, füge _ hinzu

            self.content_text.delete(start, end)
            self.content_text.insert(start, new_text)

        else:
            self.show_false_message("Kein Text markiert!")


    def insert_markdown_text(self, text_widget, content):
        # Kombiniertes Muster für ***bolditalic***, **bold**, *italic*
        pattern = r"\*\*\*(.*?)\*\*\*|\*\*(.*?)\*\*|\*(.*?)\*|__(.*?)__"

        last_index = 0
        for match in re.finditer(pattern, content):
            start, end = match.span()

            # Text vor dem Match einfügen
            normal_text = content[last_index:start]
            text_widget.insert(tk.END, normal_text)

            if match.group(1):  # ***bolditalic***
                text_widget.insert(tk.END, match.group(1), ("bold", "italic"))
            elif match.group(2):  # **bold**
                text_widget.insert(tk.END, match.group(2), "bold")
            elif match.group(3):  # *italic*
                text_widget.insert(tk.END, match.group(3), "italic")
            elif match.group(4):  # __underline__
                text_widget.insert(tk.END, match.group(4), "underline")

            last_index = end

        # Falls nach dem letzten fettgedruckten Wort noch normaler Text existiert
        remaining_text = content[last_index:]
        if remaining_text:
            text_widget.insert(tk.END, remaining_text)


    def paste_screenshot(self, event=None):
        # Holt den Screenshot aus der Zwischenablage und speichert ihn.
        img = ImageGrab.grabclipboard()  # Screenshot aus Zwischenablage holen

        if img: 
            self.screenshot_canvas.delete("all")  # Feld leeren, falls bereits ein Screenshot vorhanden ist
            self.temp_image_data = None  # Temporäre Bild-Daten entfernen

            with io.BytesIO() as output:
                img.save(output, format="PNG")
                self.temp_image_data = output.getvalue()  # Temporär speichern, aber nicht in DB!

            self.display_screenshot(img)  # Bild im Canvas anzeigen ist aber noch nicht in der DB gespeichert!
            self.clear_clipboard()  # Zwischenablage leeren

        else:
            self.show_false_message("Kein Bild in der Zwischenablage gefunden!")


    def display_screenshot(self, img):
        # Zeigt das übergebene Bild im Canvas an und skaliert es proportional.
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
        # Verzögert die Neuskalierung, um Performance-Probleme zu vermeiden
        if hasattr(self, "resize_after_id"):
            self.root.after_cancel(self.resize_after_id)  # Vorherigen Aufruf abbrechen

        self.resize_after_id = self.root.after(10, self._perform_resize)  # Nach 10ms skalieren


    def _perform_resize(self):
        """ Führt die tatsächliche Skalierung des Bildes durch """
        if self.temp_image_data:
            img = Image.open(io.BytesIO(self.temp_image_data))
            self.display_screenshot(img)  # Skaliert das Bild erneut


    def clear_input_fields(self):
        # Leert die Eingabefelder für einen neuen Notizeintrag.
        self.title_entry.delete(0, "end")  # Titel-Feld leeren
        self.content_text.delete("1.0", "end")  # Inhalt-Feld leeren
        self.screenshot_canvas.delete("all")  # Screenshot-Feld leeren
        self.temp_image_data = None  # Temporäre Bild-Daten entfernen
        self.selected_note_id = None  # Ausgewählte ID entfernen


    def show_success_message(self, text):
        """Zeigt eine Erfolg OK-Messagebox"""
        msgbox = CustomMessagebox(self.root, title="Erfolg", message=text, buttons=("OK",))
        self.root.wait_window(msgbox)  # Warten, bis das Fenster geschlossen wird


    def show_false_message(self, text):
        """Zeigt eine Fehler OK-Messagebox"""
        msgbox = CustomMessagebox(self.root, title="Fehler", message=text, buttons=("OK",))
        self.root.wait_window(msgbox)  # Warten, bis das Fenster geschlossen wird


    def show_confirmation(self, text):
        # eigt eine Ja/Nein-Messagebox und gibt das Ergebnis zurück
        msgbox = CustomMessagebox(self.root, title="Bestätigung", message=text, buttons=("Ja", "Nein"))
        self.root.wait_window(msgbox)  # Warten, bis das Fenster geschlossen wird
        return msgbox.result  # Gibt "Ja" oder "Nein" zurück
    
    def clear_clipboard(self):
        # Zwischenablage leeren
        self.root.clipboard_clear()  # Inhalt löschen
        self.root.clipboard_append("")  # Sicherstellen, dass nichts mehr drin ist
        self.root.update()  # Änderungen an der Zwischenablage sofort übernehmen



    def run(self):
        self.root.mainloop()
