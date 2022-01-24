from .db import my_posts
from fastapi import HTTPException

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p



def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

def update_post(id,post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=404)
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}


def delete_post(id):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=204)
    my_posts.pop(index)
    return {'message':'Post was succesfully deleted'}
