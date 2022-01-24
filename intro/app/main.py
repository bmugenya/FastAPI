from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from .model.post import Post
from .model.db import my_posts
from .model.func import *

from random import randrange

app = FastAPI()

@app.post("/posts")
def create_post(post:Post,response:Response):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    if post_dict:
        raise HTTPException(status_code=201)
    return {"data":post}

    return {"data":post_dict}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.get("/posts/latest")
def get_latest_posts():
    post = my_posts[len(my_posts) - 1]
    return {"data":post}


@app.get("/posts/{id}")
def get_post(id: int,response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404)
    return {"data":post}


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    post = update_post(id,post)
    return {"data":"updated post"}

@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int):
    delete_post(id)
    return Response(status_code=204)
