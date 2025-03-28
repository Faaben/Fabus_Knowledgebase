import customtkinter as ctk
from notizbuch_app import NotizbuchApp


ctk.set_appearance_mode("dark")  # "light" oder "dark"
ctk.set_default_color_theme("blue")  # Oder "green", "dark-blue", etc.

if __name__ == "__main__":
    root = ctk.CTk()  # Erstelle das Hauptfenster
    app = NotizbuchApp(root)  # Übergib das Fenster an die Klasse
    root.mainloop()  # Starte die Tkinter Hauptschleife
