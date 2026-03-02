from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column
from datetime import datetime

class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int | None = Field(default = None, primary_key=True)
    title: str
    content: str 
    published: bool = Field(
        default = True,
        sa_column_kwargs={"server_default": "true"}
    )
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    )
    owner_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
    owner: "User" = Relationship()

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default = None, primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    password: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    )

class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    user_id: int = Field(foreign_key="users.id", primary_key=True, ondelete="CASCADE")
    post_id: int = Field(foreign_key="posts.id", primary_key=True, ondelete="CASCADE")
