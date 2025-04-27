import customtkinter as ctk
from app import App


ctk.set_appearance_mode("dark")  # "light" oder "dark"
ctk.set_default_color_theme("blue")  # Oder "green", "dark-blue", etc.

if __name__ == "__main__":
    root = ctk.CTk()  # Erstelle das Hauptfenster
    app = App(root)  # Übergib das Fenster an die Klasse
    root.mainloop()  # Starte die Tkinter Hauptschleife