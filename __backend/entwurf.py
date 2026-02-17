from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

nutzer_liste = []
board_liste = []
notiz_liste = []

@app.get("/")
def root():
    return {"title": "Notiz App", "body": "Willkommen"} 

@app.post("/neuer_nutzer")
def neuer_nutzer(nutzer: Nutzer):
    nutzer_liste.append(nutzer)
    return {"message": "Nutzer erstellt"}

@app.get("/nutzer")
def get_nutzer():
    return nutzer_liste
@app.post("/neues_board")
def neues_board(board: Board):
    board_liste.append(board)
    return {"message": "Board erstellt"}

@app.get("/boards")
def get_boards():
    return board_liste

@app.post("/neue_notiz")
def neue_notiz(notiz: Notiz):
    notiz_liste.append(notiz)
    return {"message": "Notiz erstellt"}

@app.get("/notizen")
def get_notizen():
    return notiz_liste
