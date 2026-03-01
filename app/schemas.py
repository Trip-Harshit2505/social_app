from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostModel):
    pass

class userResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class Post(PostModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: userResponse

    model_config = {
        "from_attributes": True
    }

class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = {
        "from_attributes": True
    }

class createUser(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)