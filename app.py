import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from notizen_tab import NotizenTab
from aufgaben_tab import AufgabenTab

ctk.set_appearance_mode("dark")  # "light" oder "dark"
ctk.set_default_color_theme("blue")  # Oder "green", "dark-blue", etc.

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fäbu's Knowledgebase")
        self.root.geometry("900x650")

        # Notebook hinzufügen
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Tabs (Frames) erstellen
        self.notizen_tab = NotizenTab(self.notebook)
        self.aufgaben_tab = AufgabenTab(self.notebook)

        self.notebook.add(self.notizen_tab.frame, text="Notizen")
        self.notebook.add(self.aufgaben_tab.frame, text="Aufgaben")

if __name__ == "__main__":
    root = ctk.CTk()  # Erstelle das Hauptfenster
    app = App(root)  # Übergib das Fenster an die Klasse
    root.mainloop()  # Starte die Tkinter Hauptschleife