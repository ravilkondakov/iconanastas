from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    phone: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class PhotographerBase(BaseModel):
    """Добавьте поля для фотографа"""


class PhotographerCreate(PhotographerBase):
    pass


class Photographer(PhotographerBase):
    id: int

    class Config:
        from_attributes = True


class PhotoshootBase(BaseModel):
    """Добавьте поля для фотосессии"""


class PhotoshootCreate(PhotoshootBase):
    pass


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
    """Добавьте поля для комментария"""


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
