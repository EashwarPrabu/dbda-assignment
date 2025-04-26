import mysql.connector
from dotenv import load_dotenv
import os
from queries import QUERY_MAP, QUERY_PARAM_ORDER

load_dotenv()

# --- Connection Setup ---
def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# --- Retrieve Function ---
def select_data(connection, query_key, params_dict):
    try:
        query = QUERY_MAP.get(query_key)
        if not query:
            raise ValueError(f"Query not found for key: {query_key}")

        keys = QUERY_PARAM_ORDER[query_key]
        values = tuple(params_dict[k] for k in keys)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, values)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error occured during retrieval:\n{e}")
        return None
    finally:
        cursor.close()

# --- Insert Function ---
def insert_data(connection, query_key, params_dict):
    try:
        query = QUERY_MAP.get(query_key)
        if not query:
            raise ValueError(f"Query not found for key: {query_key}")

        keys = QUERY_PARAM_ORDER[query_key]
        values = tuple(params_dict[k] for k in keys)

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error occured during insertion:\n{e}")
        return None
    finally:
        cursor.close()