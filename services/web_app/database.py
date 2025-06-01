import os
import sqlite3
from datetime import datetime

# What do I need to do here
"""
 - add a new user (YES)
 - query an existing user's data (YES)
 - delete a user (YES)
 - edit a field of an existing user 


 User table attributes
    - id
    - username (email)
    - password hash
    - tokens
    - total_generations
    - joined

"""

currdir = os.path.dirname(__file__)

DATABASE_PATH = currdir + "\\test.db"
TIMESTAMP_FMT = "%Y_%m_%d_%H_%M_%S"

def get_timestamp():
    return datetime.today().strftime(TIMESTAMP_FMT)


def connect_to_db(db_path = DATABASE_PATH):
    """
    Connect to the database (if DNE, create it)
    """
    db_path = str(db_path)
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        print("Connected to DB")


def does_users_table_exist(db_path = DATABASE_PATH):
    """
    Check if the users table exists
    """
    db_path = str(db_path)
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name=?
        """, ("Users",))
        result = cursor.fetchone()

        if result:
            return True
        else:
            return False


def create_users_table(db_path = DATABASE_PATH):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        # Create the Users table if it doesn't exist yet
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                tokens INTEGER NOT NULL,
                total_generations INTEGER NOT NULL,
                date_joined TEXT NOT NULL
            )
        """)
        connection.commit()


def query_specific_user_in_users_table(db_path = DATABASE_PATH, username = "", field = "id"):
    if not does_users_table_exist(db_path):
        return []
    
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        # Get the specific users data
        ans = cursor.execute(f"SELECT {field} FROM Users WHERE username = ?", (username,))
        ans = cursor.fetchone()
        if not ans:
            return []
    return ans[0]


def add_user_to_users_table(db_path, username, password_hash):
    # Create the table if DNE.
    create_users_table(db_path)
    
    # Make sure the user is not already in there.
    ans = query_specific_user_in_users_table(username)
    if len(ans) > 0:
        raise Exception("Error, there is already a user of this name")

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO Users (username, password_hash, tokens, total_generations, date_joined) VALUES (?,?,?,?,?)", (username,password_hash, 0, 0, get_timestamp()))

        # Commit the changes
        connection.commit()


def is_user_in_table(db_path = DATABASE_PATH, username = "joe"):
    # Is the user in the table
    ans = query_specific_user_in_users_table(db_path, username, "id")
    if ans == []:
        return False
    else:
        return True


def delete_a_user(db_path = DATABASE_PATH, username = "joe"):
    """
    Delete a user from the table
    """
    if not is_user_in_table(db_path, username):
        raise Exception("User is not present in the table")

    ans = query_specific_user_in_users_table(db_path, username)
    # user is in the table
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Users WHERE id = ?", (ans,))
        connection.commit()


def edit_field_of_user(db_path = DATABASE_PATH, username = "joe", field = "total_generations", new_value = "0"):
    # Get the user id
    id = query_specific_user_in_users_table(db_path, username, "id")

    assert id != []

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE Users SET {field} = ? WHERE id = ?",
            (new_value, id)
        )
        conn.commit()
    
    
if __name__ == "__main__":
    sampledb = "sample.db"


    add_user_to_users_table(sampledb, "ben", "oh")
    
    # ans = get_users_table(sampledb)
    # print(ans)
    
    # ans = query_specific_user_in_users_table(sampledb, "ben")
    # ans = query_specific_user_in_users_table(sampledb, "tommy")

    

# def get_users_table(db_path = DATABASE_PATH):
#     with sqlite3.connect(db_path) as connection:
#         cursor = connection.cursor()
#     cursor.execute("SELECT * FROM Users")
#     rows = cursor.fetchall()  # fetches all the rows in the resul
#     return rows