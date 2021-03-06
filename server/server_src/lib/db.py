import pg8000


class Db:
    def __init__(self, host):
        self.conn = pg8000.connect(
            database="blogscraper",
            user="postgres",
            password="postgres",
            host=host,
            port=5432
        )

        self.cur = self.conn.cursor()

    def execute(self, sql):
        data = None
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()

        except pg8000.Error as e:
            print("something went wrong:", e, sql)
            self.rollback()

        return data

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()
