from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Klassen vom pydantic BaseModel bauen.

class Nutzer(BaseModel):
    id: int
    name: str
    passwort: int
    board_liste: list

class Board(BaseModel):
    id: int
    name: str
    notizen_liste: list

class Notiz(BaseModel):
    id: int
    name: str
    inhalt: str

@app.get("/")
def root():
    return ({"title": "Eine Webseite mit Notizen", "body": ""})

@app.post("/login")
def login(nutzername: str, passwort: str):
    return # alle daten des Nutzers

@app.get("/boards")
def root():
    return # boards des aktuellen Nutzers mit allen Notizen

@app.post("/neuer_nutzer")
def post_neuer_nutzer(nutzer: Nutzer):
    pass

@app.delete("/entferne_nutzer")
def delete_nutzer(nutzer: Nutzer):
    pass

@app.post("/neues_board")
def post_neues_board(board: Board):
    pass

@app.delete("/entferne_board")
def delete_board(board: Board):
    pass

@app.post("/neue_notiz")
def post_neue_notiz(notiz: Notiz):
    pass

@app.delete("/entferne_notiz")
def delete_notiz(notiz: Notiz):
    pass

@app.patch("/notiz_zu_board_hinzufuegen")
def patch_notiz_into_board(notiz: Notiz, board: Board):
    pass

@app.patch("/notiz_von_board_entfernen")
def patch_notiz_from_board(notiz: Notiz, board: Board):
    pass

@app.patch("/board_zu_nutzer_hinzufuegen")
def patch_board_into_nutzer(board: Board, nutzer: Nutzer):
    pass

@app.patch("/board_von_nutzer_entfernen")
def patch_board_from_nutzer(board: Board, nutzer: Nutzer):
    pass