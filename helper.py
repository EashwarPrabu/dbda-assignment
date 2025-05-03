import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
import bcrypt
import time
from queries import QUERY_MAP
from db import connect_to_db, insert_data, create_table, check_and_add_foreign_key_constraint_exist

console = Console()
connection = connect_to_db()

def create_stored_procedure():
    cursor = None
    try:
        procedure_sql = """
            CREATE PROCEDURE insert_vote_and_mark_voted(
                IN p_voter_id INT,
                IN p_candidate_id INT,
                IN p_constituency_id INT
            )
            BEGIN
                INSERT INTO Vote (voter_id, candidate_id, constituency_id)
                VALUES (p_voter_id, p_candidate_id, p_constituency_id);

                UPDATE Voter
                SET has_voted = TRUE
                WHERE voter_id = p_voter_id;
            END
        """
        cursor = connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS insert_vote_and_mark_voted;")
        cursor.execute(procedure_sql)
        connection.commit()
    except Exception as e:
        print(f"Error creating procedure:\n{e}")
    finally:
        cursor.close()

def init_tables():
    tables = ["create_constituency", "create_party", "create_voter", "create_admin", "create_candidate", "create_contests_in", "create_vote"]
    for table in tables:
        create_table(connection, table)
    check_and_add_foreign_key_constraint_exist(connection, "check_if_voter_fk_constraint_exists", "add_voter_fk_constraint")
    create_stored_procedure()

def populate_table():
    insertion_data = {
        "insert_constituency": {
            "name": "Central Park", 
            "district": "New York"
        },
        "insert_party": {
            "name": "Green Party", 
            "symbol": "GP", 
            "leader": "Alice Green"
        },
        "insert_voter": {
            "aadhar": "123456789000",
            "name": "John Doe",
            "dob": "1990-01-01",
            "gender": "M",
            "address": "123 Main St",
            "constituency_id": 1
        },
        "insert_candidate": {
            "voter_id": 1,
            "party_id": 1,
            "constituency_id": 1
        },
        "insert_contests_in": {
            "party_id": 1,
            "constituency_id": 1
        },
    }
    for queryName, content in insertion_data.items():
        insert_data(connection, queryName, content)

def add_admin():
    questions = [
        inquirer.Text('email', message='Email'),
        inquirer.Password('pwd', message='Password'),
        inquirer.Text('voter_id', message='Voter ID'),
    ]
    answers = inquirer.prompt(questions)
    answers['pwd'] = bcrypt.hashpw(answers['pwd'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    console.print("\n[bold cyan]Voter Information[/bold cyan]")
    insert_data(connection, "insert_admin", answers)

def database_helper():
    console.print(Panel("[bold cyan]Initializing Database[/bold cyan]"))
    with console.status("[green]Starting setup...", spinner="dots") as status:
        status.update("[green]Creating tables, constraints, and stored procedure...")
        init_tables()
        time.sleep(0.75)
        console.print("[bold green]Tables, Constraints and Stored Procedures created successfully[/bold green]")

        status.update("[green]Inserting sample data...")
        populate_table()
        time.sleep(0.75)
        console.print("[bold green]Sample Data inserted successfully[/bold green]\n")

    console.print(Panel("[bold cyan]Please enter Admin details[/bold cyan]"))
    add_admin()
    console.print("[bold green]Admin inserted successfully[/bold green]\n")

    console.print("[bold green]Database initialization complete![/bold green]")
    console.print("[bold green]Sample data has been populated in the tables![/bold green]")

if __name__ == "__main__":
    database_helper()