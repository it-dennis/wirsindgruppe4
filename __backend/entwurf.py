from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel):
    id: int
    titel: str
    content: str

notes = []

@app.get("/notizen")
def get_notes():
    print("Hole alle Notizen")
    return notes

@app.post("/notiz_hinzufuegen")
def add_note(note: Note):
    notes.append(note)
    return {"message": "Notiz hinzugefügt"}
