from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List
import boards 

# Importe aus deinen eigenen Dateien
from boards import User, Board, Note, BoardUserLink
from security import get_password_hash, verify_password

# --- DB SETUP ---
sqlite_url = "sqlite:///notes_app.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(title="NoteShare Pro API")

# ... dein engine setup ...

@app.on_event("startup")
def on_startup():
    # Wir greifen direkt auf die Metadaten in boards zu, falls nötig
    print("Starte Datenbank-Initialisierung...")
    SQLModel.metadata.create_all(engine)
    print("Datenbank-Tabellen wurden (falls nicht vorhanden) erstellt.")

#@app.on_event("startup")
#def on_startup():
#    SQLModel.metadata.create_all(engine)

# --- USER ENDPUNKTE ---
@app.post("/users/register")
def register_user(username: str, password: str, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username vergeben")
    
    new_user = User(username=username, hashed_password=get_password_hash(password))
    session.add(new_user)
    session.commit()
    return {"status": "User erstellt", "id": new_user.id}

# --- BOARD ENDPUNKTE ---
@app.post("/boards/")
def create_board(name: str, owner_id: int, session: Session = Depends(get_session)):
    board = Board(name=name, owner_id=owner_id)
    session.add(board)
    session.commit()
    session.refresh(board)
    return board

@app.get("/users/{user_id}/all-boards")
def list_user_boards(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return {
        "eigene": user.owned_boards,
        "geteilte": user.shared_boards
    }

# --- COLLABORATION ---
@app.post("/boards/{board_id}/invite/{user_id}")
def invite_user(board_id: int, user_id: int, session: Session = Depends(get_session)):
    link = BoardUserLink(board_id=board_id, user_id=user_id)
    session.add(link)
    session.commit()
    return {"message": "Board geteilt"}

# --- NOTIZEN ---
@app.post("/notes/")
def create_note(title: str, content: str, board_id: int, session: Session = Depends(get_session)):
    note = Note(title=title, content=content, board_id=board_id)
    session.add(note)
    session.commit()
    return note
