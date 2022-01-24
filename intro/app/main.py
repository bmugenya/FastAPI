from fastapi import FastAPI,Response,status,HTTPException
from .model.post import Post
from .model.model import Model


app = FastAPI()

model = Model()
@app.post("/posts")
def create_post(post:Post,response:Response):
    post_dict = post.dict()
    model.add_post(post_dict['title'],post_dict['content'])
    if post_dict:
        raise HTTPException(status_code=201)
    return {"data":post_dict}

@app.get("/posts")
def get_posts():
    posts = model.get_posts()
    return {"data":posts}

@app.get("/posts/latest")
def get_latest_posts():
    posts = model.get_posts()
    post = posts[len(posts) - 1]
    return {"data":post}


@app.get("/posts/{id}")
def get_post(id: int,response:Response):
    post = model.get_post(id)
    if not post:
        raise HTTPException(status_code=404)
    return {"data":post}


@app.put("/posts/{id}")
def update_post(id:int,post:Post,response:Response):
    post_dict = post.dict()
    model.update_post(id,post_dict['title'],post_dict['content'])
    return {"data":"updated post"}

@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int):
    model.delete_post(id)
    return Response(status_code=204)
