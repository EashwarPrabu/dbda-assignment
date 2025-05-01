import mysql.connector
from dotenv import load_dotenv
import os
from queries import QUERY_MAP, QUERY_PARAM_ORDER, QUERY_HEADERS
from rich.table import Table
from rich import box

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
    cursor = None
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

# --- Retrieve All Function ---
def select_all_data(connection, query_key):
    cursor = None
    try:
        query = QUERY_MAP.get(query_key)
        if not query:
            raise ValueError(f"Query not found for key: {query_key}")

        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error occured during retrieval:\n{e}")
        return None
    finally:
        cursor.close()

# --- Insert Function ---
def insert_data(connection, query_key, params_dict):
    cursor = None
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

# --- Build Table using Fetched data ---
def build_table_from_query_result(data, query_key, table_name):
    headers = QUERY_HEADERS.get(query_key)
    if not headers:
        raise ValueError(f"No column headers defined for query key: {query_key}")

    # Define a list of colors to cycle through
    colors = ["cyan", "magenta", "green", "yellow", "blue", "bright_cyan", "bright_magenta"]
    table = Table(title=table_name, box=box.ROUNDED, header_style="bold white")

    # Add columns with color and alignment
    for i, header in enumerate(headers):
        style = colors[i % len(colors)]
        justify = "right" if "id" in header.lower() else "left"
        table.add_column(header, style=style, justify=justify)

    # Add rows
    for row in data:
        row_values = [str(value) if value is not None else "" for value in row.values()]
        table.add_row(*row_values)

    return table