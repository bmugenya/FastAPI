from fastapi import FastAPI,Response,status,HTTPException,APIRouter,Depends
from .. import schemas
from ..model import Model
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta


model = Model()

router = APIRouter(
    prefix='/users',
     tags=['Users']
    )

@router.post("/")
def create_user(user:schemas.User,response:Response):
    post_dict = user.dict()
    model.add_user(post_dict['email'],post_dict['password'])
    if post_dict:
        raise HTTPException(status_code=201)
    return post_dict


@router.post("/login",response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = model.login(form_data.username,form_data.password)
    if user:
        token = model.create_access_token(data = {"user_id":user})
        return {'access_token': token,'token_type': 'Bearer'}
    raise HTTPException(status_code=403,detail="Incorrect username or password")



@router.get("/{id}")
def get_user(id: int,response:Response):
    post = model.get_user(id)
    if not post:
        raise HTTPException(status_code=404)
    return post

