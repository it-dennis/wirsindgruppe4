from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

# Die Brücke: Welcher User gehört zu welchem Board?
class UserBoardLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    board_id: Optional[int] = Field(default=None, foreign_key="board.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    # n:m Beziehung zu Boards
    boards: List["Board"] = Relationship(back_populates="users", link_model=UserBoardLink)

class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # n:m Beziehung zu Usern
    users: List[User] = Relationship(back_populates="boards", link_model=UserBoardLink)
    notes: List["Note"] = Relationship(back_populates="board")

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    board_id: int = Field(foreign_key="board.id")
    board: Board = Relationship(back_populates="notes")