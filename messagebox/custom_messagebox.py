import customtkinter as ctk

class CustomMessagebox(ctk.CTkToplevel):
    def __init__(self, parent, title="Nachricht", message="Hier ist deine Nachricht", buttons=("OK",), icon=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("280x140")  # Fenstergröße
        self.resizable(False, False)
        self.result = None  # Speichert die Antwort

        # Nachricht anzeigen
        label = ctk.CTkLabel(self, text=message, font=("Arial", 14), wraplength=280)
        label.pack(pady=20)

        # Button-Frame für bessere Zentrierung
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Buttons erstellen (dynamisch aus der `buttons`-Liste)
        for btn_text in buttons:
            btn = ctk.CTkButton(button_frame, text=btn_text, width=100, command=lambda b=btn_text: self.on_button_click(b))
            btn.pack(side="left", padx=10)

        self.grab_set()  # Macht das Fenster modal

    def on_button_click(self, button_text):
        self.result = button_text  # Speichert, welcher Button gedrückt wurde
        self.destroy()
