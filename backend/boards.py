from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class BoardUserLink(SQLModel, table=True):
    board_id: Optional[int] = Field(default=None, foreign_key="board.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    owned_boards: List["Board"] = Relationship(back_populates="owner")
    shared_boards: List["Board"] = Relationship(back_populates="members", link_model=BoardUserLink)

      
class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="owned_boards")
    members: List[User] = Relationship(back_populates="shared_boards", link_model=BoardUserLink)
    notes: List["Note"] = Relationship(back_populates="board", cascade_delete=True)

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    board_id: int = Field(foreign_key="board.id")
    board: Board = Relationship(back_populates="notes")
