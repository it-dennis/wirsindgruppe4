import requests
import json

# Die URL deiner laufenden FastAPI
BASE_URL = "http://127.0.0.1:8000"

def test_full_workflow():
    print("--- Starte API Test-Workflow ---")

    # 1. User registrieren
    user_data = {"username": "test_user_1", "password": "sicherespasswort123"}
    response = requests.post(f"{BASE_URL}/users/register", params=user_data)
    user_1 = response.json()
    print(f"[1] User 1 registriert: {user_1}")

    # 2. Zweiter User für das Teilen registrieren
    user_2_data = {"username": "kollege_ab", "password": "geheimpasswort"}
    response = requests.post(f"{BASE_URL}/users/register", params=user_2_data)
    user_2 = response.json()
    print(f"[2] User 2 registriert: {user_2}")

    # 3. Ein Board für User 1 erstellen
    board_params = {"name": "Projekt Weltreise", "owner_id": user_1['id']}
    response = requests.post(f"{BASE_URL}/boards/", params=board_params)
    board = response.json()
    print(f"[3] Board erstellt: {board['name']} (ID: {board['id']})")

    # 4. Eine Notiz in das Board schreiben
    note_data = {
        "title": "Packliste",
        "content": "Reisepass, Kamera, Sonnencreme",
        "board_id": board['id']
    }
    response = requests.post(f"{BASE_URL}/notes/", params=note_data)
    print(f"[4] Notiz hinzugefügt: {response.json()['title']}")

    # 5. Das Board mit User 2 teilen
    share_url = f"{BASE_URL}/boards/{board['id']}/invite/{user_2['id']}"
    response = requests.post(share_url)
    print(f"[5] Board geteilt: {response.json()['message']}")

    # 6. Dashboard von User 2 prüfen (muss das geteilte Board sehen)
    response = requests.get(f"{BASE_URL}/users/{user_2['id']}/all-boards")
    dashboard = response.json()
    print(f"[6] Dashboard User 2: {len(dashboard['geteilte_boards'])} geteilte(s) Board(s) gefunden.")
    
    print("\n--- Test erfolgreich abgeschlossen! ---")

if __name__ == "__main__":
    try:
        test_full_workflow()
    except Exception as e:
        print(f"Fehler beim Testen: {e}")
        print("Stelle sicher, dass uvicorn läuft (uvicorn main:app --reload)")
