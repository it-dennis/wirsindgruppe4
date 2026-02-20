from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from typing import List, Optional
from fastapi import FastAPI, HTTPException


# --- Datenbank Setup ---
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- SQLModel Tabellen ---

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    # Beziehung: Ein Nutzer hat viele Boards
    boards: List["Board"] = Relationship(back_populates="user")

class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: int = Field(foreign_key="user.id") 
    # Beziehungen
    user: User = Relationship(back_populates="boards")
    notes: List["Note"] = Relationship(back_populates="board")

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    board_id: int = Field(foreign_key="board.id")
    # Beziehung: Eine Notiz gehört zu einem Board
    board: Board = Relationship(back_populates="notes")

# --- FastAPI App ---
app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Notiz erstellen (mit Board-Zuweisung)
@app.post("/boards/{board_id}/")
def create_note(board_id: int, note: Note):
    with Session(engine) as session:
        note.board_id = board_id
        session.add(note)
        session.commit()
        session.refresh(note)
        return note
    
# Notiz löschen (und aus allen Boards entfernen)
@app.delete("/notes/{note_id}/")
def delete_note(note_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        session.delete(note)
        session.commit()
        return {"ok": True, "message": "Note gelöscht"}


# Alle Boards eines Nutzers abrufen
@app.get("/users/{user_id}/boards")
def read_user_boards(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found") # Diskrepanz zwischen Errormeldungen #Errormeldungen "gleichgeschaltet mit HTTPException"
    
        return user.boards

# Alle Boards eines Nutzers inklusive Notizen abrufen
@app.get("/users/{user_id}/notes")
def read_user_boards(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found") # Diskrepanz zwischen Errormeldungen #Errormeldungen "gleichgeschaltet mit HTTPException"

        user_boards = session.exec(select(Board).where(Board.user_id == user_id)).all() # muss angepasst werden, falls user IDs in Boards anders gespeichert werden
        return_content = []
        for board in user_boards:
            notes = session.exec(select(Note).where(Note.board_id == board.id)).all()
            return_content.append({**board.dict(), "notes": [n.dict() for n in notes]})
        return return_content
    
# Nutzer stellen
@app.post("/users/")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

# Nutzer löschen / Nutzer aus Boards löschen / Boards ohne Nutzer löschen
# Code hier

# Board erstellen und einem Nutzer zuweisen
@app.post("/users/{user_id}/boards/")
def create_board(user_id: int, board: Board):
    with Session(engine) as session:
        board.user_id = user_id
        session.add(board)
        session.commit()
        session.refresh(board)
        return board

# Board updaten, einen neuen Nutzer hinzufügen
# Code hier

# Board updaten, einen Nutzer entfernen / Boards ohne Nutzer löschen
# Code hier

# Datenbank leeren, praktisch zum Testen.
@app.delete("/clear/")
def clear_database():
    with Session(engine) as session:
        session.exec(Note.__table__.delete())
        session.exec(Board.__table__.delete())
        session.exec(User.__table__.delete())
        session.commit()
    return {"ok": True, "message": "Database cleared"}