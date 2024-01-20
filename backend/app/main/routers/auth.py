from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from backend.app.main.crud.user import UserCRUD
from backend.app.main.models import User
from backend.app.main.schemas import UserAuth

router = APIRouter()

SECRET_KEY = "omg_iconanastas!"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Функция для создания JWT токена
def create_jwt_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# Функция для чтения токена из запроса и верификации
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user_id


@router.post("/token")
async def login(user: UserAuth):
    user_id = await UserCRUD.get_user(username=user.username)
    if user.password == user.password and user.username == user.username:
        user_data = {"sub": str(user_id.id)}
        token = create_jwt_token(user_data)
        return {"access_token": token, "token_type": "bearer"}
    print(user)
    return {"ERROR": "user not found"}


# Пример защищенного маршрута
@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You are in a protected route!", "user": current_user}
