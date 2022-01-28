import psycopg2
from .config import settings
url = f"dbname={settings.DB_NAME} user={settings.DB_USER} host={settings.DB_HOSTNAME} port={settings.DB_PORT} password={settings.DB_PASSWORD}"



class database_setup(object):

    def __init__(self):
        self.conn = psycopg2.connect(url)
        self.cursor = self.conn.cursor()

    def destroy_tables(self):
        self.cursor.execute("""DROP TABLE IF EXISTS user CASCADE;""")

        self.conn.commit()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL NOT NULL,
            registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
            email VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            PRIMARY KEY (email)
        );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Post(
            post_id SERIAL NOT NULL,
            title VARCHAR(255) NOT NULL,
            post_date DATE NOT NULL DEFAULT CURRENT_DATE,
            content VARCHAR(255) NOT NULL,
            email VARCHAR(50) REFERENCES Users(email),
            PRIMARY KEY (post_id)
        );""")




