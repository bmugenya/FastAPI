from .db_con import database_setup
from fastapi import HTTPException


class Model():

    def __init__(self):
        self.database = database_setup()
        self.cursor = self.database.cursor

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


    def add_post(self,title,content):

        post = {
            "title": title,
            "content": content
        }

        query = """INSERT INTO post (title,content)
            VALUES(%(title)s,%(content)s);"""

        self.cursor.execute(query, post)
        self.database.conn.commit()
        return post


    def find_index_post(id):
        for i,p in enumerate(my_posts):
            if p["id"] == id:
                return i

    def update_post(self,id,title,content):
        query = "UPDATE post SET title = '%s',content = '%s' WHERE post_id = '%s';"% (title,content,id)
        self.cursor.execute(query)
        self.database.conn.commit()


    def delete_post(self,id):
        query = "DELETE FROM post WHERE post_id = '%s';" % (id)
        self.cursor.execute(query)
        self.database.conn.commit()

