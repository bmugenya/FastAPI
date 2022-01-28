from fastapi import FastAPI,Response,status,HTTPException,APIRouter,Depends
from typing import Optional
from .. import schemas
from ..model import Model

model = Model()

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
    )

@router.post("/",response_model=schemas.Post)
def create_post(post:schemas.Post,response:Response,username: str = Depends(model.get_current_user)):
    post_dict = post.dict()
    model.add_post(post_dict['title'],post_dict['content'],username.username)
    if post_dict:
        raise HTTPException(status_code=201)
    return post_dict

@router.get("/")
def get_posts():
    posts = model.get_posts()
    return posts

@router.get("/latest")
def get_latest_posts(limit:int = 1,skip:int = 0,search:Optional[str]=""):
    posts = model.get_posts()
    post = posts[len(posts) - 1]
    return post


@router.get("/{id}")
def get_post(id: int,response:Response):
    post = model.get_post(id)
    if not post:
        raise HTTPException(status_code=404)
    return post


@router.put("/{id}")
def update_post(id:int,post:schemas.Post,response:Response,username: str = Depends(model.get_current_user)):
    post_dict = post.dict()
    model.update_post(id,post_dict['title'],post_dict['content'],username.username)
    return post_dict

@router.delete("/{id}")
def delete_post(id:int,response:Response,username: str = Depends(model.get_current_user)):
    model.delete_post(id,username.username)
    return Response(status_code=204)
