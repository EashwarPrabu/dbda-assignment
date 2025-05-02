import inquirer
from rich.console import Console
from rich.panel import Panel
import bcrypt
from queries import QUERY_MAP
from db import connect_to_db, insert_data, select_data, build_table_from_query_result

console = Console()
connection = connect_to_db()

console.print(Panel("[bold green]Admin Helper[/bold green]"))
questions = [
    inquirer.Text('email', message='Email'),
    inquirer.Password('pwd', message='Password'),
    inquirer.Text('voter_id', message='Voter ID'),
]
answers = inquirer.prompt(questions)
answers['pwd'] = bcrypt.hashpw(answers['pwd'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
console.print("\n[bold cyan]Voter Information[/bold cyan]")
insert_data(connection, "insert_admin", answers)
data = select_data(connection, "show_inserted_admin", {"email": answers["email"]})
table = build_table_from_query_result(data, "show_inserted_admin", "Admin")
console.print(table)