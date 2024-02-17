""" Accessing the database using an sql query """
# pylint: disable=missing-class-docstring

from django.db import connection

# https://docs.djangoproject.com/en/5.0/topics/db/sql/

class DBQuery:
    def __init__(self, sql: str, attributes: list):
        self.sql = sql
        self.attributes = attributes

    def easy_execute(self) -> tuple:
        """ The simplest query without data conversion """
        result = ()
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            result = cursor.fetchall()
        return result

    def execute(self) -> list:
        """ conversion: query to a named dictionary """
        result = []
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result

    def execute_with_id(self) -> dict:
        """ conversion: query to an indexed dictionary """
        result = {}
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                result[row[0]] = dict(zip(columns, row))
        return result

    def key_value(self) -> dict:
        """ conversion: query to an Id-Value dictionary"""
        result = {}
        with connection.cursor() as cursor:
            cursor.execute(self.sql, self.attributes)
            for row in cursor.fetchall():
                result[row[0]] = row[1]
        return result
