# Fäbu's-Knowledgebase
Programmiert von Fabian Aeschimann

### Beschreibung des Projekts 
Ich habe mir in der Freizeit eine Knowledgebase erstellt und möchte diese nun weiter ausbauen. Ich will den bestehenden Code so anpassen, dass der Code der Obijektorientierten Programmierung entspricht.  
Folgende Punkte will ich umsetzen:  
#### Minimalziel 
- ✅ Code an die Objektorientierte Programmierung anpassen. Die KB hat nun eine grösse erreicht wo kleine Änderungen nicht mehr so einfach zum anpassen sind aus diesem Grund macht es Sinn die Struktur anzupassen. 
  Ich will 3 verschiedene Klassen aufbauen. Wenn ich wärend der Umsetzung merke, dass es noch weitere Klassen benötigt, werde ich diese erweitern. 
  - NotizbuchApp
  - Datenbank
  - Notiz
- ✅ Die Verwendung der KB soll einfacher werden aus diesem Grund soll die KB anhand einer Verlinkung aus dem Desktop gestartet werden können. Dafür will ich den PyInstaller verwenden.
  [PyInstaller](https://pyinstaller.org/en/stable/index.html)
- ✅ Da man manche dinge nicht so einfach mit dem Text beschreiben kann, ist es praktischer wenn man ein PrintScreen einfügen kann.
    Ich will mit ctrl + C und ctrl + v einen Screenshot einem KB Eintrag anfügen und abspeichern. Beim Suchen soll er dann auch wieder angezeit werden.

#### Erweiterte Ziele
- ✅ Das Layout vom GUI soll moderner wirken aus diesem Grund will ich das customtkinter in meinem Projekt integrieren
    - [Customtkinter Blog](https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22)
    - [Documentation Customtkinter](https://customtkinter.tomschimansky.com/)
    - [GitHub TomSchimansky](https://github.com/TomSchimansky/CustomTkinter)
- Ein CMD erstellen, damit ich das notizbuch mit dem Kurzbefehl "111" das notizbuch öffnen kann 
- Kategorien für die Notes erstellen, damit man die Suche besser eingrenzen kann.
- Screenshot mit ctrl + V einfügen. Damit ich eine weitere Funktion implementieren kann.
- Doppelklick auf das Image soll es in einem grösseren Format ausgeben. Das ist vorallem praktisch wenn das Bild kleine Details enthält welche man nicht so gut sieht.
- Dateien an einem Notiz anfügen
- Ein CMD erstellen, damit ich das notizbuch mit dem Kurzbefehl "111" das notizbuch öffnen kann
- In der KB eine 2 Lasche erstellen. Damit man auf der 2. ein kleines Game hat.  

###ToDo's
- ✅ Wenn ich die Grösse von meiner KB verändere, dann soll sich das ausgewählte Image sich automatisch der grösse anpassen.
- ✅ Wenn ich ein Notiz auswähle, und danach ein neuer erfassen will, sind die Eingabefelder mit einem Inhalt belegt. Ziel, wenn die Suchfunktion leer ist, dann sollen auch die Eingabefelder für Title, Content, Image wieder leer sein.
- ✅Wenn ich ein Notiz ausgewählt habe, dann erscheint ein Fehler wenn ich auf den Speichern anstatt auf den Aktualisieren Button klicke.


### Anleitung
#### PyInstaller
Wenn man eine .exe Datei erstellt hat und danach wieder am code etas anpasst, wird dies nicht übernommen. Das bedeutet, die Datei muss neu aufgebaut werden. 
Mit diesem Befehl Kann die .exe neu erstellt werden.  
``pyinstaller --onefile --windowed --noupx --clean --name "Fäbus_KB" main.py``

#### Datenbank  
Die Datenbank ist so eingestellt, das es einen Ordner "Fäbus_KB" im Dokumente Ordner vom User erstellt. Wenn es noch keinen hat wird eine Datei namens Fäbus_KB.db erstellt

### Journal

02.03.2025 Ich habe die OOP Programmierung umgesetzt und getestet.

05.03.2025 Ich habe heute die .exe mit pyinstaller erstellt. Hier gab es die schwirigkeit, das Windows die .exe immer wieder als Trojaner erkannt hat. Ich habe danach den pyinstaller noch einmal überprüft und es sollte alles korrekt sein. 
ChatGPT meint, dass dies ein gängiger Fehler by pyinstaller ist und durch den PyInstaller-Bootloader ausgelöst wird. 

08.03.2024 Ich habe heute die ganze Handhabung mit dem Aktualisieren von Notizen und Skalieren von der App verbessert. Ich habe auch das Feedback von Michael umgesetzt, dass ich die select_note funktion anpassen könnte, damit der Text vom Notiz nicht in das Feld results_text geladen wird sondern in die gleichen Felder wie beim Erfassen der Notiz title_entry und content_text. Das hat die ganze handhabung vom Notizbuch sehr vereinfacht und es macht eigendlich auch mehr Sinn. Nach der Umsetzung von der automatischen Skalierung des Screenshotes hatte ich danach grosse Performance Probleme, da es beim skalieren der App sehr gestockt hat. Der grund war, das es bei jeder Pixel bewegung das Bild neu angepasst hat. Ich ahbe das danach geändert indem ich eine verzögerung von 100ms eingebaut habe. 

11.03.2025 Ich habe die App auf das neue Design umgestellt. Hier gab es ein paar schwirigkeiten, vorallem das der Button Fett mit dem Customtkinter nicht mehr funktioniert da es das Bolt nicht unterstützt. Ich habe danach einen Mix von beiden gemacht, das meiste ist mit Customtkinter ausser die Textfelder sind weiterhin mit dem normalen tkinter. So kann ich die Formatierung besser steuern. 
