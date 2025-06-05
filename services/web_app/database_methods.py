"""
Reattempting to make really nice Sqlite methods to
make simple database operations easy

What functions do I need for my app?
- Add a user to the table [DONE]
- Query a specific field from the user [DONE]
- Edit a specific field of the user
- Delete a user

What functions for development?
- Query all info from a user on a table


"""

import os
import sqlite3
from datetime import datetime

# class Database():
#     def __init__(self):

TIMESTAMP_FMT = "%Y_%m_%d_%H_%M_%S"


def get_timestamp():
    return datetime.today().strftime(TIMESTAMP_FMT)


class UsersTable:
    """
    id
    username
    password
    tokens
    total_generations
    joined
    """

    def __init__(self, database_path):
        database_path = str(database_path)
        assert ".db" in database_path
        self.database_path = database_path

        # Define the schema
        self.fields = [
            "id",
            "username",
            "password_hash",
            "tokens",
            "total_generations",
            "date_joined",
        ]
        self.field_formats = [
            "INTEGER PRIMARY KEY AUTOINCREMENT",
            "TEXT NOT NULL",
            "TEXT NOT NULL",
            "INTEGER NOT NULL",
            "INTEGER NOT NULL",
            "TEXT NOT NULL",
        ]

    def does_database_exist(self):
        if os.path.exists(self.database_path):
            return True
        else:
            return False

    def does_users_table_exist(self):
        if not self.does_database_exist():
            return False
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table' AND name=?
            """,
                ("Users",),
            )
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False

    def create_users_table(self):
        """
        Creates a table if DNE
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()

            # Create the Users table if it doesn't exist yet
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    tokens INTEGER NOT NULL,
                    total_generations INTEGER NOT NULL,
                    date_joined TEXT NOT NULL
                )
            """
            )
            connection.commit()

    def generate_add_query_string(self):
        query_string = "INSERT INTO Users ("
        question_marks = "("
        for field in self.fields:
            if field == "id":
                continue  # skip the id
            if field != self.fields[-1]:
                query_string += field + ", "
                question_marks += "?,"
            else:
                question_marks += "?)"
                query_string += field
        query_string += f") VALUES {question_marks}"
        return query_string

    def generate_specific_user_query(self, field):
        assert field in self.fields
        query_string = f"SELECT {field} FROM Users WHERE username = ?"

        return query_string

    def generate_edit_query(self, field):
        assert field in self.fields
        assert field != "id"
        query_string = f"UPDATE Users SET {field} = ? WHERE id = ?"
        return query_string

    def add_user(self, username, password_hash):
        if not self.does_users_table_exist():
            self.create_users_table()

        # TODO - Make sure the user is not already in there
        ans = self.query_specific_user_data(username, "id")
        if ans != []:
            raise Exception("Error! User already in the database!")

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()

            # Create the SQL string
            query_string = self.generate_add_query_string()

            # print(query_string)
            # "INSERT INTO Users (username, password_hash, tokens, total_generations, date_joined) VALUES (?,?,?,?,?)"
            cursor.execute(
                query_string, (username, password_hash, 0, 0, get_timestamp())
            )

            # Commit the changes
            connection.commit()

    def query_specific_user_data(self, username, field):
        if not self.does_users_table_exist():
            return []

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()

            # Generate the query string
            query_string = self.generate_specific_user_query(field)
            # print(query_string)

            # Get the specific users data
            cursor.execute(query_string, (username,))
            ans = cursor.fetchone()
            if not ans:
                return []
            else:
                return ans[0]

        return []

    def edit_field_of_user(self, username, field, value):
        # Get the user id
        id = self.query_specific_user_data(username, "id")
        if id == []:
            raise Exception("Error, User not in database!")

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()

            query_string = self.generate_edit_query(field)
            cursor.execute(query_string, (value, id))
            connection.commit()

    def delete_user(self, username):
        """
        Delete a user from the table
        """
        id = self.query_specific_user_data(username, "id")
        if id == []:
            print("Warning! User is not present in the DB")
            print("Nothing to delete")
            return

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
            connection.commit()

        print(f"Deleted : {username}")


if __name__ == "__main__":
    a = UsersTable("sample3.db")
    # a.add_user("ben2", "123")
    ans = a.query_specific_user_data("tommy", "password_hash")
    print(ans)
