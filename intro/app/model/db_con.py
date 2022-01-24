import psycopg2

url = "dbname='fastapi' user='postgres' host='localhost' port=5432 password='Qw12Er34'"

class database_setup(object):

    def __init__(self):
        self.conn = psycopg2.connect(url)
        self.cursor = self.conn.cursor()

    def destroy_tables(self):
        self.cursor.execute("""DROP TABLE IF EXISTS user CASCADE;""")

        self.conn.commit()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Post(
            post_id SERIAL NOT NULL,
            title VARCHAR(255) NOT NULL,
            post_date DATE NOT NULL DEFAULT CURRENT_DATE,
            content VARCHAR(255) NOT NULL,
            PRIMARY KEY (post_id)
            );""")
