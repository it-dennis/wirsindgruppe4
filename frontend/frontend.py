import requests

url = "http://127.0.0.1:8000"

print("Starte Frontend Test...\n")

# USER REGISTRIEREN
response = requests.post(
    f"{url}/users/register",
    json={
        "username": "Testnutzer",
        "password": "Passwort"
    }
)

user_data = response.json()
print("User Registrierung:", user_data)

user_id = user_data["id"]


# LOGIN TEST
login_response = requests.post(
    f"{url}/users/login",
    json={
        "username": "Testnutzer",
        "password": "Passwort"
    }
)

print("Login Antwort:", login_response.json(), "\n")


# BOARDS ERSTELLEN

board1 = requests.post(
    f"{url}/boards/",
    params={"name": "Gruppenarbeit", "owner_id": user_id}
).json()

board2 = requests.post(
    f"{url}/boards/",
    params={"name": "Privat", "owner_id": user_id}
).json()

print("Boards erstellt:", board1["name"], "und", board2["name"], "\n")

board1_id = board1["id"]
board2_id = board2["id"]


# NOTIZEN ERSTELLEN

notes = [
    {"title": "Frontend-Krams", "content": "Infos zum Frontend Projekt"},
    {"title": "Backend-Krams", "content": "Infos zum Backend Projekt"},
]

for note in notes:
    created = requests.post(
        f"{url}/notes/",
        params={
            "title": note["title"],
            "content": note["content"],
            "board_id": board1_id
        }
    ).json()

    print("Notiz ersetllt:", created["title"])


# Extra Notiz im Privat Board
requests.post(
    f"{url}/notes/",
    params={
        "title": "Einkaufsliste",
        "content": "1x Salz\n2x Nudeln\n7x Apfel",
        "board_id": board2_id
    }
)


# ALLE BOARDS AUSLESEN

boards = requests.get(f"{url}/users/{user_id}/all-boards").json()

print("\nAlle Boards vom User:\n")

print("Eigene Boards:")
for board in boards["eigene"]:
    print("-", board["name"])

print("\nGeteilte Boards:")
for board in boards["geteilte"]:
    print("-", board["name"])

print("\nFrontend Test abgeschlossen.")