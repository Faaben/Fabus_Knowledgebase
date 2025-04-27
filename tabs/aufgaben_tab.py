import config
import tkinter as tk
from tkinter import *
import customtkinter as ctk
from datenbank.datenbank import Datenbank
from model.notiz import Notiz
from PIL import Image, ImageTk, ImageGrab
from messagebox.custom_messagebox import CustomMessagebox




class AufgabenTab:

    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.create_widgets()


    def create_widgets(self):
        # Inhalt des Aufgaben-Tabs
        ctk.CTkLabel(self.frame, text="Hier kannst du Aufgaben verwalten!").pack(padx=10, pady=10)