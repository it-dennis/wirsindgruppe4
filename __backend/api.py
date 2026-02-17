from sqlmodel import SQLModel, Field
from typing import Optional
from fastapi import FastAPI, Depends
from sqlmodel import Session, create_engine, select

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str



app = FastAPI()
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/notes/")
def create_note(note: Note):
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

@app.get("/notes/")
def read_notes():
    with Session(engine) as session:
        return session.exec(select(Note)).all()
    
#==============================================================================================
#Dateien main.py (Backend) und api.py zusammen gefügt, erste Idee.

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

# Beispiel: Notiz erstellen (mit Board-Zuweisung)
@app.post("/notes/")
def create_note(note: Note):
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

# Beispiel: Alle Boards eines Nutzers inklusive Notizen abrufen
@app.get("/users/{user_id}/boards")
def read_user_boards(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        return user.boards
