# Functions for interacting with SQLite database

import sqlite3
from datetime import datetime

DB_NAME = "rag_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_application_logs():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS application_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT,
            gpt_response TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """ 
    )

    conn.close()

# This is a new function that is not in the basics.ipynb 
def create_document_store():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS document_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.close()


# Functions to manage Chat Logs in the database
def insert_application_logs(session_id, user_query, gpt_response, model):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO application_logs (session_id, user_query, gpt_response, model) VALUES (?, ?, ?, ?)",
        (session_id, user_query, gpt_response, model)
    )

    conn.commit()
    conn.close()  

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend(
            [
                {"role": "human", "content": row["user_query"]},
                {"role": "ai", "content": row["gpt_response"]}
            ]
        )

    conn.close()
    return messages

# Functions to manage Document Store in the database
def insert_document_record(filename):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO document_store (filename) VALUES (?)', (filename,))
    file_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return file_id

def delete_document_record(file_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM document_store WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    return True

def get_all_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, upload_timestamp FROM document_store ORDER BY upload_timestamp DESC')
    documents = cursor.fetchall()
    conn.close()
    return [dict(doc) for doc in documents]


#initialize the database tables
create_application_logs()
create_document_store()
    
# TODO: Add and refine the documentation for this file
'''
------------------------------------------------------------------------------------------------
The code above defines functions to interact with the SQLite database. The functions include: 

get_db_connection : This function establishes a connection to the SQLite database. 
create_application_logs : This function creates the  application_logs  table in the database. 
create_document_store : This function creates the  document_store  table in the database. 
insert_application_logs : This function inserts a new record into the  application_logs  table. 
get_chat_history : This function retrieves the chat history for a given session ID from the  application_logs  table. 
insert_document_record : This function inserts a new record into the  document_store  table. 
delete_document_record : This function deletes a record from the  document_store  table. 
get_all_documents : This function retrieves all documents from the  document_store  table. 

The database tables are initialized by calling the  create_application_logs  and  create_document_store  functions. 
Step 6: Implement the FastAPI Endpoints 
Now that we have defined the database functions, we can implement the FastAPI endpoints for the RAG application. 
Create a new file named  main.py  in the  rag_app  directory and add the following code:
------------------------------------------------------------------------------------------------
'''