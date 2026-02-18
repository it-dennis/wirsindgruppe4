from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from typing import List, Optional
from fastapi import FastAPI, HTTPException

# --- Datenbank Setup ---
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

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
@app.post("/notes/")
def create_note(note: Note):
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note
    
# Notiz löschen (und aus allen Boards entfernen)
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if note == None:
            return {"ok": False, "message": "Notiz nicht gefunden"}
        session.delete(note)
        session.commit()
        return {"ok": True, "message": "Note gelöscht"}


# Alle Boards eines Nutzers inklusive Notizen abrufen
@app.get("/users/{user_id}/boards")
def read_user_boards(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        return user.boards
    
# Nutzer stellen
# Code hier

# Nutzer löschen / Nutzer aus Boards löschen / Boards ohne Nutzer löschen
# Code hier

# Board erstellen und einem Nutzer zuweisen
# Code hier

# Board updaten, einen neune Nutzer hinzufügen
# Code hier

# Board updaten, einen Nutzer entfernen / Boards ohne Nutzer löschen
# Code hier