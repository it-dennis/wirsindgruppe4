import os
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from typing import List, Optional

# --- DB SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlite_path = os.path.join(BASE_DIR, "notes_app.db")
sqlite_url = f"sqlite:///{sqlite_path}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

# --- MODELLE (Datenbank-Tabellen) ---

class BoardUserLink(SQLModel, table=True):
    board_id: Optional[int] = Field(default=None, foreign_key="board.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    owned_boards: List["Board"] = Relationship(back_populates="owner")
    shared_boards: List["Board"] = Relationship(back_populates="members", link_model=BoardUserLink)

class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="owned_boards")
    notes: List["Note"] = Relationship(back_populates="board", cascade_delete=True)
    members: List[User] = Relationship(back_populates="shared_boards", link_model=BoardUserLink)

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    board_id: int = Field(foreign_key="board.id")
    board: Board = Relationship(back_populates="notes")

# --- APP ---
app = FastAPI(title="Profi Notiz-App API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# --- ENDPUNKTE ---

# 1. USER: Erstellen und Auflisten
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    user.id = None
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

# 2. BOARDS: Erstellen und Abrufen
@app.post("/boards/", response_model=Board)
def create_board(board: Board, session: Session = Depends(get_session)):
    board.id = None
    session.add(board)
    session.commit()
    session.refresh(board)
    return board

@app.get("/users/{user_id}/all-boards")
def get_user_boards(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return {
        "eigene_boards": user.owned_boards,
        "geteilte_boards": user.shared_boards
    }

# 3. TEILEN: Board für anderen User freigeben
@app.post("/boards/{board_id}/share-with/{user_id}")
def share_board(board_id: int, user_id: int, session: Session = Depends(get_session)):
    link = BoardUserLink(board_id=board_id, user_id=user_id)
    session.add(link)
    session.commit()
    return {"status": "Erfolgreich geteilt"}

# 4. NOTIZEN: Erstellen und Board-Inhalt anzeigen
@app.post("/notes/", response_model=Note)
def create_note(note: Note, session: Session = Depends(get_session)):
    note.id = None
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@app.get("/boards/{board_id}/notes", response_model=List[Note])
def get_notes_from_board(board_id: int, session: Session = Depends(get_session)):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board nicht gefunden")
    return board.notes
