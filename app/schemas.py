from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, conint

from datetime import datetime



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None


# ------------------------------


class User(BaseModel):
    email: EmailStr
    password: str


class UserCreate(User):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
        # orm_mode = True
        

# ------------------------------


class Post(BaseModel):
    title: str
    contents: str
    published: bool = True


class PostCreate(Post):
    pass


class PostUpdate(Post):
    pass


class PostResponse(BaseModel):
    id: int
    title: str
    contents: str
    created_at: datetime
    user_id: int
    handle: UserResponse

    class Config:
        from_attributes = True
        # orm_mode = True
        

# ------------------------------


class Vote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(strict=True, ge=0, le=1)]