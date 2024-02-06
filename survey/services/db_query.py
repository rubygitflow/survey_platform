from django.db import connection

# https://docs.djangoproject.com/en/5.0/topics/db/sql/

class DBQuery:
    def __init__(self, sql: str, attributes: list):     
        self.sql = sql
        self.attributes = attributes

    def easy_execute(self) -> tuple:
        result = ()
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            result = cursor.fetchall()
        return result

    def execute(self) -> list:
        result = []
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result

    def execute_with_id(self) -> dict:
        result = {}
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
              result[row[0]] = dict(zip(columns, row)) 
        return result

    def key_value(self) -> dict:
        result = {}
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
              result[row[0]] = row[1]
        return result
