# Fäbu's-Knowledgebase
Programmiert von Fabian Aeschimann

## Beschreibung des Projekts 
In meiner Freizeit habe ich eine eigene Knowledgebase entwickelt, um wichtige Informationen und Notizen übersichtlich zu speichern.  
Jetzt möchte ich das Projekt weiter ausbauen und verbessern.  
Ein Schwerpunkt dabei ist, den bestehenden Code auf objektorientierte Programmierung (OOP) umzustellen, um die Struktur klarer, wartbarer und einfacher erweiterbar zu machen.  
Das Projekt entsteht im Rahmen eines Schulprojekts im 4. Semester meiner Ausbildung zum Wirtschaftsinformatiker HF und dient dazu, meine Kenntnisse in moderner Softwareentwicklung und sauberer Programmierung weiter zu vertiefen.

## Anleitung App
### 1. Schnellstart mit der Fäbus_KB App
Die Fäbus_KB App ist super einfach zu nutzen – du brauchst keine zusätzlichen Pakete oder Bibliotheken zu installieren.  
Geh einfach in den Ordner "dist" und lade dir die Datei Fäbus_KB.exe herunter.  
Manchmal meckert der Browser und stuft die Datei als unsicher ein – das kannst du getrost ignorieren. Die App ist natürlich sicher! 😉
![Anleitung1](https://github.com/user-attachments/assets/178f1b7b-efb9-406f-afc5-c09b91473487)

### 2. Loslegen
Sobald du die Fäbus_KB.exe heruntergeladen hast, kannst du sie ganz einfach per Doppelklick starten – genau wie jede andere Anwendung auch. 🚀

### 3. Neue Notiz erfassen
Um eine neue Notiz abzuspeichern, musst du einfach einen Titel und einen Notiztext eingeben.  
Das Einfügen eines Screenshots ist optional. Wenn du einen Screenshot in der Zwischenablage hast, klick einfach mit der Maus in das Feld der Screenshot-Vorschau – der Screenshot wird dann automatisch eingefügt. 🖼️  
Bist du zufrieden mit deiner Notiz, kannst du sie ganz einfach über den "Speichern"-Button speichern. 💾  
Außerdem kannst du deinen Notiztext auch bearbeiten: Markiere einfach den gewünschten Text und formatiere ihn fett, kursiv oder unterstrichen – je nachdem, was du brauchst! ✍️
![Anleitung6](https://github.com/user-attachments/assets/85fab752-8dc7-41f9-a3e6-8f98c8841a31)

### 4. Notiz suchen
Im unteren Bereich der App kannst du mit einer Volltextsuche nach beliebigen Begriffen suchen.
Es werden dann nur noch die Notizen angezeigt, in denen dein Suchbegriff vorkommt – und damit du ihn schneller findest, wird er gelb markiert. 🔍✨
![Anleitung7](https://github.com/user-attachments/assets/c7e9a96b-b1f8-45cc-834f-c741a32dcf0b)

### 5. Notiz aktualisieren
Willst du eine bestehende Notiz ergänzen oder ändern, klick einfach auf den Titel der Notiz.  
Die Inhalte werden dann automatisch in den Erfassungsbereich geladen, und du kannst sie wie gewohnt bearbeiten und speichern. 🔄📝
![Anleitung8](https://github.com/user-attachments/assets/e4d50724-9466-4121-ac4f-a79c24a0cb27)

### 6. Notiz löschen
Möchtest du eine bestehende Notiz löschen, klick einfach auf den Titel der Notiz und dann auf den "Löschen"-Button.  
Für alle kleinen Tollpatsche da draußen: Keine Sorge, du wirst nochmal gefragt, ob du die Notiz wirklich löschen möchtest. 😉

### 7. Infos zur Datenbank
Die App checkt automatisch, ob sich im "Dokumente"-Ordner deines Benutzers schon eine Fäbus_KB.db-Datenbank befindet.  
Falls noch keine vorhanden ist, wird beim ersten Start einfach eine neue Datenbank erstellt.  
Wenn schon eine existiert, wird natürlich die bestehende verwendet – ganz automatisch und ohne, dass du etwas tun musst. 📂✨  
Wichtig: Ändere den Namen der Datei Fäbus_KB.db bitte nicht, sonst kann die App die Datenbank nicht mehr finden! 🚫

## Entwicklung
### Minimalziel 
- ✅ Code an die Objektorientierte Programmierung anpassen. Die KB hat nun eine grösse erreicht wo kleine Änderungen nicht mehr so einfach zum anpassen sind aus diesem Grund macht es Sinn die Struktur anzupassen. 
  Ich will 3 verschiedene Klassen aufbauen. Wenn ich wärend der Umsetzung merke, dass es noch weitere Klassen benötigt, werde ich diese erweitern. 
  - NotizbuchApp
  - Datenbank
  - Notiz
- ✅ Die Verwendung der KB soll einfacher werden aus diesem Grund soll die KB anhand einer Verlinkung aus dem Desktop gestartet werden können. Dafür will ich den PyInstaller verwenden.
  [PyInstaller](https://pyinstaller.org/en/stable/index.html)
- ✅ Da man manche dinge nicht so einfach mit dem Text beschreiben kann, ist es praktischer wenn man ein PrintScreen einfügen kann.
    Ich will mit ctrl + C und ctrl + v einen Screenshot einem KB Eintrag anfügen und abspeichern. Beim Suchen soll er dann auch wieder angezeit werden.

### Erweiterte Ziele
- ✅ Das Layout vom GUI soll moderner wirken aus diesem Grund will ich das customtkinter in meinem Projekt integrieren
    - [Customtkinter Blog](https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22)
    - [Documentation Customtkinter](https://customtkinter.tomschimansky.com/)
    - [GitHub TomSchimansky](https://github.com/TomSchimansky/CustomTkinter)
- Kategorien für die Notes erstellen, damit man die Suche besser eingrenzen kann.
- Doppelklick auf das Image soll es in einem grösseren Format ausgeben. Das ist vorallem praktisch wenn das Bild kleine Details enthält welche man nicht so gut sieht.
- Dateien an einem Notiz anfügen
- Ein CMD erstellen, damit ich das notizbuch mit dem Kurzbefehl "111" das notizbuch öffnen kann
- In der KB eine 2 Lasche erstellen. Damit man auf der 2. ein kleines Game hat.
- ✅ Button für Kursiv und Underline erstellen
- ✅ Speichern und Aktuallisieren Button zusammenführen.

### ToDo's
- ✅ Wenn ich die Grösse von meiner KB verändere, dann soll sich das ausgewählte Image sich automatisch der grösse anpassen.
- ✅ Wenn ich ein Notiz auswähle, und danach ein neuer erfassen will, sind die Eingabefelder mit einem Inhalt belegt. Ziel, wenn die Suchfunktion leer ist, dann sollen auch die Eingabefelder für Title, Content, Image wieder leer sein.
- ✅ Wenn ich ein Notiz ausgewählt habe, dann erscheint ein Fehler wenn ich auf den Speichern anstatt auf den Aktualisieren Button klicke.
- ✅ Zwischenablage vom Screenshot nach dem einfügen wieder leeren.
- ✅ Wenn ein Notiz gelöscht wird, dann wird das Screenshot Feld nicht aktuallisiert.
- ✅ Messageboxen einheitlich gestalten
- ✅ Resize_canvas optimieren, damit sich das Bild schneller anpasst beim skallieren.
- ✅ Kursiv und Underline Funktion erstellt, allerdings fehlt noch die Funktion wo den Text dann visuell kursiv oder underline darstellt.
- ✅ Besprechung mit Michael: Bei der Datenbank abfrage schauen das ich immer mit der Klasse Note arbeite. Add, Update, Delete angepasst
- ✅ Wenn Suchfeld leer, dann sollen alle Notizen angezeigt werden.
- Wenn man einen Notiz auswählt aber nicht erneut speichert, wird die Eingabemaske nicht geleert. --> Lösung 1 Button für leeren Lösung 2 Wenn das Suchfeld leer ist, soll es die eingabemaske leeren
   
### Anleitung PyInstaller
Wenn man eine .exe Datei erstellt hat und danach wieder am Code etwas anpasst, wird dies nicht übernommen.  
Das bedeutet, die Datei muss neu aufgebaut werden.  
Navigiere im Terminal zum Ordner Fabus_Knowledgebase, wenn du die gesamte Struktur von GitHub übernommen hast, und gib folgenden Befehl ein:
``pyinstaller --onefile --windowed --icon=C:\Users\Fabian\Documents\Feusi\OOP_und_Softwarearchitektur\Fabus_Knowledgebase\others\Images\logo.ico --noupx --clean --name "Fäbus_KB" app.py``

## Journal
### 02.03.2025  
- Ich habe die OOP-Programmierung umgesetzt und getestet.

### 05.03.2025  
- Ich habe heute die .exe mit PyInstaller erstellt. Hier gab es die Schwierigkeit, dass Windows die .exe immer wieder als Trojaner erkannt hat.  
  Ich habe danach den PyInstaller noch einmal überprüft, und es sollte alles korrekt sein.  
  ChatGPT meint, dass dies ein gängiger Fehler bei PyInstaller ist und durch den PyInstaller-Bootloader ausgelöst wird.

### 08.03.2025  
- Ich habe heute die ganze Handhabung mit dem Aktualisieren von Notizen und dem Skalieren der App verbessert.  
- Ich habe auch das Feedback von Michael umgesetzt, dass ich die select_note-Funktion anpassen könnte, damit der Text der Notiz nicht in das Feld results_text geladen wird, sondern in die gleichen Felder wie beim Erfassen der Notiz (title_entry und content_text).
Das hat die ganze Handhabung vom Notizbuch sehr vereinfacht und es macht eigentlich auch mehr Sinn.  
- Nach der Umsetzung der automatischen Skalierung des Screenshots hatte ich große Performance-Probleme, da es beim Skalieren der App sehr gestockt hat.
  Der Grund war, dass es bei jeder Pixelbewegung das Bild neu angepasst hat.
  Ich habe das danach geändert, indem ich eine Verzögerung von 100 ms eingebaut habe.

### 11.03.2025  
- Ich habe die App auf das neue Design umgestellt. Hier gab es ein paar Schwierigkeiten, vor allem, dass der Button "Fett" mit CustomTkinter nicht mehr funktioniert hat, da es "Bold" nicht unterstützt.  
Ich habe danach einen Mix aus beidem gemacht: Das meiste ist mit CustomTkinter, außer die Textfelder – diese sind weiterhin mit dem normalen Tkinter umgesetzt.  
So kann ich die Formatierung besser steuern.

### 15.03.2025  
- Ich habe das Projekt mit Michael besprochen. Dabei ist noch ein Bug aufgetaucht, dass sich das Image-Feld nicht geleert hat, wenn man eine Notiz gelöscht hat.  
Diesen Bug habe ich noch korrigiert. Zusätzlich habe ich die Messagebox optimiert und einheitlich gestaltet.

### 29.03.2025
- Ich habe den Code noch mit den Funktionen italic und underline ergänzt, damit die Buttons funktionieren.
- Feedback von Michael: Ich habe auch noch die Funktionen add_note und update_note zusammengeführt zur Funktion save_note. Sowohl in der Datenbank als auch im GUI. So habe ich nur noch einen Button auf der Maske.
- Feedback von Michael: Wenn das Suchfeld leer war, dann gab es auch keine KBs. Ich habe es jetzt so eingestellt, dass, wenn ich das Programm starte, alle Einträge geladen werden, und wenn das Feld leer ist, dann sind auch alle Einträge ersichtlich.

### 25.04.2025
- Finale .exe für die Abgabe des Projektes erstellt.
- .exe auf einer neu erstellten VM mit Windows 11 getestet, ob man irgendwelche Pakete oder Bibliotheken installieren muss oder nicht:
Die .exe konnte ohne zusätzliche Installationen gestartet werden. Die Datenbank wurde korrekt unter "Dokumente" erstellt.

