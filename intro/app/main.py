from fastapi import FastAPI
from .routers import post,users
from .config import settings
app = FastAPI()


app.include_router(post.router)
app.include_router(users.router)



