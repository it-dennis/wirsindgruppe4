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