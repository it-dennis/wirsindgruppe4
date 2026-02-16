# Globale Variablen:

alle_nutzer_liste = []
aktueller_nutzer = None
angemeldet = False
aktueller_versuch = 0
versuche = 3
linie = """
---------------------------------------------
"""

# Klassen:

class Nutzer:
    def __init__(
            self,
            id = 0, # ID ist noch unnötig, aber für die Zukunft...
            name = "",
            passwort = "",
            board_liste = []
            ):
        self.id = id
        self.name = name
        self.passwort = passwort
        self.board_liste = board_liste # Liste mit allen Boards, auf die der Nutzer Zugriff hat.
        alle_nutzer_liste.append(self) # Fügt sich beim Erstellen automatisch der Liste aller Nutzer hinzu.

    # Und hier kommen den so Funktionen hin wie Board hinzufügen/entfernen und so.

class Board:
    def __init__(
            self,
            id = 0,
            name = "",
            notizen_liste = []
            ):
        self.name = name
        self.id = id
        self.notizen_liste = notizen_liste # Liste mit allen Notizen, die in diesem Board sind.

    # Und hier kommen den so Funktionen hin wie Notiz hinzufügen/entfernen und so.

class Notiz:
    def __init__(
            self,
            id = 0,
            name = "",
            inhalt = ""
            ):
        self.id = id
        self.name = name
        self.inhalt = inhalt


# Ein paar Testdaten. Normalerweise werden die natürlich aus dem Backend abgefrufen / ins Backend geschrieben

testnutzer = Nutzer(1803, "Testnutzer", "Passwort")

notiz1 = Notiz(
    1,
    "Frontend-Krams",
    "Nützliche Notizen zum Frontend: Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."
    )
notiz2 = Notiz(
    2,
    "Datenbank-Krams",
    "Ein paar Infos zur Datenbankanbindung: At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. "
    )
notiz3 = Notiz(
    3,
    "Backend-Krams",
    "Hier ein paar Notizen zum Backend unseres Projektes und Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    )
notiz4 = Notiz(
    4,
    "Einkaufsliste",
    """1x Salz
7x Apfel
2x Nudeln
    """
    )

# Die Notizen den Boards hinzufügen

board1 = Board(1, "Gruppe 4", [notiz1, notiz2, notiz3])
board2 = Board(2, "Privat", [notiz4])

# Die Boards dem Nutzer hinzufügen

testnutzer.board_liste = [board1, board2]


# Ein paar Hilfefunktionen, ausgelagert, um den Code lesbarer zu machen:

def nutzer_check(eingabe_name):
    for nutzer in alle_nutzer_liste:
        if nutzer.name == eingabe_name:
            return True
    return False

def passwort_check(eingabe_name, eingabe_passwort):
    for nutzer in alle_nutzer_liste:
        if nutzer.name == eingabe_name:
            if nutzer.passwort == eingabe_passwort:
                return True
    return False

def get_Nutzer(eingabe_name):
    for nutzer in alle_nutzer_liste:
        if nutzer.name == eingabe_name:
            return nutzer
    print("Fehler im Code, Nutzer nicht gefunden")
    return


# Hier nun tatsächliche Anfang des Codes, der ausgeführt wird beim Aufrufen dieser Datei:

print()
print("Guten Tag in unserer App!")
print(linie)


# Login checken

while aktueller_versuch < versuche:
    eingabe_name = input("Nutzername eingeben: ")
    if nutzer_check(eingabe_name) == False:
        print("Es wurde kein Nutzer mit diesem Namen gefunden.")
        continue

    eingabe_passwort = input("Passwort eingeben: ")
    if passwort_check(eingabe_name, eingabe_passwort) == False:
        aktueller_versuch += 1
        print(f"Falsches Passwort. Noch {versuche - aktueller_versuch} Versuch(e).")
        continue

    aktueller_nutzer = get_Nutzer(eingabe_name)
    angemeldet = True
    print("Login erfolgreich!")
    break

if not angemeldet:
    print("Anmeldung gescheitert.")

print(linie)


# Wenn Login erfolgreich war, hier nun Daten ausgeben:

if angemeldet:
    print(f"Willkommen {aktueller_nutzer.name}!")
    print()
    print("Übersicht deiner Notizen:")
    for board in aktueller_nutzer.board_liste:
        print(linie)
        print(f"Board: {board.name}")
        print()
        for notiz in board.notizen_liste:
            print(notiz.name)
            print()
            print(notiz.inhalt)
            print()
        print()

print(linie)