from .db_con import database_setup
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from . import schemas
from passlib.apps import custom_app_context
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class Model():

    def __init__(self):
        self.database = database_setup()
        self.cursor = self.database.cursor

    def create_access_token(self,data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


    def verify_access_token(self,token:str,credentials_exception):
        try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            username:str = payload.get('user_id')
            if username is None:
                raise credentials_exception
            token_data = schemas.TokenData(username=username[0])
        except JWTError:
            raise credentials_exception
        return token_data



    def get_current_user(self,token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # user = self.get_users(token.user_id)
        return self.verify_access_token(token,credentials_exception)

    def add_user(self,email,password):

        user = {
            "email": email,
            "password":custom_app_context.encrypt(password)
        }

        query = """INSERT INTO Users (email,password)
            VALUES(%(email)s, %(password)s);"""
        self.cursor.execute(query, user)
        self.database.conn.commit()
        return user

    def get_user(self, id):
        query = "SELECT email FROM Users WHERE user_id = '%s';" % (id)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user


    def get_users(self, email):
        query = "SELECT * FROM Users WHERE user_id = '%s';" % (email)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def login(self, email, password):

        query = "SELECT password FROM Users WHERE email = '%s';" % (email)
        self.cursor.execute(query)
        pwd = self.cursor.fetchone()

        if pwd:
            if custom_app_context.verify(password, pwd[0]):
                query = "SELECT email FROM Users WHERE email = '%s';" % (email)
                self.cursor.execute(query)
                users = self.cursor.fetchone()
                return users

    def get_posts(self):
        query = "SELECT * FROM post;"
        self.cursor.execute(query)
        posts = self.cursor.fetchall()
        return posts


    def get_post(self,id):
        query = "SELECT * FROM post WHERE post_id= '%s';" % (id)
        self.cursor.execute(query)
        post = self.cursor.fetchone()
        return post


    def add_post(self,title,content,email):

        post = {
            "title": title,
            "content": content,
            "email":email
        }

        query = """INSERT INTO post (title,content,email)
            VALUES(%(title)s,%(content)s,%(email)s);"""

        self.cursor.execute(query, post)
        self.database.conn.commit()
        return post


    def find_index_post(id):
        for i,p in enumerate(my_posts):
            if p["id"] == id:
                return i

    def update_post(self,id,title,content,email):
        query = "UPDATE post SET title = '%s',content = '%s' WHERE post_id = '%s' and email ='%s' ;"% (title,content,id,email)
        self.cursor.execute(query)
        self.database.conn.commit()


    def delete_post(self,id,email):
        query = "DELETE FROM post WHERE post_id = '%s' and email='%s';" % (id,email)
        self.cursor.execute(query)
        self.database.conn.commit()

