# Fäbu's-Knowledgebase
Programmiert von Fabian Aeschimann

### Beschreibung des Projekts 
Ich habe mir in der Freizeit eine Knowledgebase erstellt und möchte diese nun weiter ausbauen. Ich will den bestehenden Code so anpassen, dass der Code der Obijektorientierten Programmierung entspricht.  
Folgende Punkte will ich umsetzen:  
#### Minimalziel 
  - Code an die Objektorientierte Programmierung anpassen. Die KB hat nun eine grösse erreicht wo kleine Änderungen nicht mehr so einfach zum anpassen sind aus diesem Grund macht es Sinn die Struktur anzupassen. 
    Ich will 3 verschiedene Klassen aufbauen. Wenn ich wärend der Umsetzung merke, dass es noch weitere Klassen benötigt, werde ich diese erweitern. 
      - NotizbuchApp
      - Datenbank
      - Notiz
  - Die Verwendung der KB soll einfacher werden aus diesem Grund soll die KB anhand einer Verlinkung aus dem Desktop gestartet werden können. Dafür will ich den PyInstaller verwenden. 
 https://pyinstaller.org/en/stable/index.html
  - Da man manche dinge nicht so einfach mit dem Text beschreiben kann, ist es praktischer wenn man ein PrintScreen einfügen kann.
    Ich will mit ctrl + C und ctrl + v einen Screenshot einem KB Eintrag anfügen und abspeichern. Beim Suchen soll er dann auch wieder angezeit werden.
#### Erweiterte Ziele
  - Das Layout vom GUI soll moderner wirken aus diesem Grund will ich das customtkinter in meinem Projekt integrieren [Customtkinter](https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22)

### Anleitung
#### PyInstaller
Wenn man eine .exe Datei erstellt hat und danach wieder am code etas anpasst, wird dies nicht übernommen. Das bedeutet, die Datei muss neu aufgebaut werden. 
Mit diesem Befehl Kann die .exe neu erstellt werden.  
``pyinstaller --onefile --windowed --noupx --clean --name "Fabus_Knowledgebase" main.py``


### Journal

02.03.2025 Ich habe die OOP Programmierung umgesetzt und getestet.

05.03.2025 Ich habe heute die .exe mit pyinstaller erstellt. Hier gab es die schwirigkeit, das Windows die .exe immer wieder als Trojaner erkannt hat. Ich habe danach den pyinstaller noch einmal überprüft und es sollte alles korrekt sein. 
ChatGPT meint, dass dies ein gängiger Fehler by pyinstaller ist und durch den PyInstaller-Bootloader ausgelöst wird. 
