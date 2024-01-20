from typing import List, Optional, Dict

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    phone: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    username: str
    password: str


class PhotographerBase(BaseModel):
    user_id: int
    insta_name: str
    title: str


class Photographer(PhotographerBase):
    id: int

    class Config:
        from_attributes = True


class PhotographerCreate(PhotographerBase):
    pass


class PhotoshootBase(BaseModel):
    limit: int
    description: str
    title: str

    class Config:
        from_attributes = True


class PhotoshootCreate(PhotoshootBase):
    photoshoots: List[PhotographerBase]

    class Config:
        from_attributes = True


class Photoshoot(PhotoshootBase):
    id: int

    class Config:
        from_attributes = True


class PhotoBase(BaseModel):
    """Добавьте поля для фотографии"""


class PhotoCreate(PhotoBase):
    pass


class Photo(PhotoBase):
    id: int

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    """Добавьте поля для отзыва"""


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    user_id: int
    photoshoot_id: int
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    """Добавьте поля для сообщения"""


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int

    class Config:
        from_attributes = True
