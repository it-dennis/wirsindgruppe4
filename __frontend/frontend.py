import requests

url = "http://127.0.0.1:8000"


# Datenbank leeren (Sonst würde man beim Testen immer wieder die gleichen Inhalte in die Datenbank schreiben)

response = requests.delete(f"{url}/clear/")
print(response.json())


# Nutzer erstellen

payload = {"username": "Testnutzer", "password": "Passwort"}

response = requests.post(f"{url}/users/", json=payload)
# print(response.json())


# Und user ID auslesen

user = response.json()
user_id = user["id"]
# print(user_id)


# Boards erstellen und zuweisen mit user ID, board IDS speichern

response = requests.post(f"{url}/users/{user_id}/boards/", json={"name": "Gruppenarbeit"}).json()
board_gruppenarbeit_id = response["id"]

response = requests.post(f"{url}/users/{user_id}/boards/", json={"name": "Privat"}).json()
board_privat_id = response["id"]


# Boards füllen

notiz1 = {"title": "Frontend-Krams", "content": "Nützliche Notizen zum Frontend: Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."}
notiz2 = {"title": "Datenbank-Krams", "content": "Ein paar Infos zur Datenbankanbindung: At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."}
notiz3 = {"title": "Backend-Krams", "content": "Hier ein paar Notizen zum Backend unseres Projektes und Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."}
notiz4 = {"title": "Einkaufslist", "content": """1x Salz
7x Apfel
2x Nudeln
    """}


# Notizen Boards hinzufügen mit board IDs

payload = [notiz1, notiz2, notiz3]

for notiz in payload:
    response = requests.post(f"{url}/boards/{board_gruppenarbeit_id}/", json=notiz)
    print(response.json())

response = requests.post(f"{url}/boards/{board_privat_id}/", json=notiz4)
print(response.json())


# Alle Boards und Notizen für unseren Nutzer auslesen

response = requests.get(f"{url}/users/{user_id}/notes").json()


# Alle Boards und Notizen printen

print(f"Ausgabe aller Boards und Notizen für User mit ID {user_id}:")
print()

for board in response:
    print(f"Board: {board['name']}")
    print()

    notes = board.get("notes", [])

    for note in notes:
        print(f"Notiz: {note['title']}")
        print()
        print(f"Inhalt: {note['content']}")
        print()