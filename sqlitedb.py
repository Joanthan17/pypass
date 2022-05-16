import os
import sqlite3

def clear_db():
    query = "DELETE FROM strings"
    runQuery(query)

def remove_task(string):
    query = "DELETE FROM strings WHERE string=?"
    delete_task_data = (string,)
    runQuery(query, delete_task_data)

def save_task(word):
    query = "INSERT INTO strings VALUES (?)"
    insert_task_data = (word,)
    runQuery(query, insert_task_data)

def load_tasks():
    query = "SELECT string FROM strings"
    return  runQuery(query, receive=True)


def runQuery(sql_query, data=None, receive=False):
    conn = create_connection("strings.db")
    cursor = conn.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)

    if receive:
        return cursor.fetchall()
    else:
        conn.commit()

    conn.close()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=3)
    except sqlite3.Error as e:
        print(e)
    return conn

def firstTimeDB():
    create_tables = "CREATE TABLE strings (string TEXT)"
    runQuery(create_tables)
    default_task_query = "INSERT INTO string VALUES (?)"
    default_task_data = ("DB",)
    runQuery(default_task_query, default_task_data)


if __name__ == "__main__":
    if not os.path.isfile("strings.db"):
        firstTimeDB()
    l = []
    # for i in range(10000):
    #     l.append(str(i))
    #
    # for word in l:
    #     save_task(word)

    print (len(load_tasks()))

    #clear_db()
    print(len(load_tasks()))
