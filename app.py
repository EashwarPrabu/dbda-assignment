import inquirer
from rich.console import Console
from rich.panel import Panel
from time import sleep
import bcrypt
from db import connect_to_db, select_data, insert_data, select_all_data, build_table_from_query_result, create_table, check_and_add_foreign_key_constraint_exist

console = Console()
connection = connect_to_db()

def login_menu():
    questions = [
        inquirer.List('role',
                      message="Login as",
                      choices=['Admin', 'Voter', 'Exit'])
    ]
    answers = inquirer.prompt(questions)
    return answers['role']

def show_admin_menu():
    questions = [
        inquirer.List('action',
                      message="Admin Menu - Select a functionality",
                      choices=[
                          'Add a new Voter to the DB',
                          'Add a new Party to the DB',
                          'Add a new Candidate to the DB',
                          'Add a new Constituency to the DB',
                          'Add a new Admin to the DB',
                          'Exit to Main Menu'
                      ])
    ]
    answers = inquirer.prompt(questions)
    return answers['action']

def show_user_menu():
    questions = [
        inquirer.List('action',
                      message="Voter Menu - Select an option",
                      choices=[
                          'Cast Vote',
                          'See Results',
                          'Candidate Information',
                          'Party Presence',
                          'Enquire Admin Details',
                          'Logout to Main Menu'
                      ])
    ]
    answers = inquirer.prompt(questions)
    return answers['action']

def add_admin():
    console.print(Panel("[bold green]Add a New Admin[/bold green]"))
    questions = [
        inquirer.Text('email', message='Email'),
        inquirer.Password('pwd', message='Password'),
        inquirer.Text('voter_id', message='Voter ID'),
    ]
    answers = inquirer.prompt(questions)
    answers['pwd'] = bcrypt.hashpw(answers['pwd'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    console.print("\n[bold cyan]Voter Information[/bold cyan]")
    insert_data(connection, "insert_admin", answers)
    print_table("show_inserted_admin", "Inserted Admin Details", {"email": answers["email"]})
    console.log(answers)

def authenticate_admin(admin_id, admin_pwd):
    admin = select_data(connection, "find_admin_by_id", {"admin_id": admin_id})
    if admin:
        stored_hashed_pwd = admin[0]['pwd'].encode('utf-8')
        if bcrypt.checkpw(admin_pwd.encode('utf-8'), stored_hashed_pwd):
            console.print("[green]Authentication successful![/green]\n")
            return True
        else:
            console.print("[red]Authentication failed! Incorrect password.[/red]\n")
            return False
    else:
        console.print("[red]Authentication failed! Admin not found.[/red]\n")

def print_table(query_name, table_name, params=None):
    data = None
    if params:
        data = select_data(connection, query_name, params)
    else:
        data = select_all_data(connection, query_name)
    table = build_table_from_query_result(data, query_name, table_name)
    console.print(table)

def add_voter():
    console.print(Panel("[bold green]Add a New Voter[/bold green]"))
    print_table("select_all_constituencies", "Constituencies")
    questions = [
        inquirer.Text('aadhar', message='Aadhar Number'),
        inquirer.Text('name', message='Full name'),
        inquirer.Text('dob', message='Date of Birth (YYYY-MM-DD)'),
        inquirer.List('gender', message='Gender', choices=['M', 'F', 'O']),
        inquirer.Text('address', message='Address'),
        inquirer.Text('constituency_id', message='Enter Constituency id from the above table'),
    ]
    answers = inquirer.prompt(questions)
    console.print("\n[bold cyan]Voter Information[/bold cyan]")
    insert_data(connection, "insert_voter", answers)
    print_table("show_inserted_voter", "Inserted Voter Details", {"aadhar": answers["aadhar"]})
    console.log(answers)

def add_party():
    console.print(Panel("[bold green]Add a New Party[/bold green]"))
    questions = [
        inquirer.Text('name', message='Party name'),
        inquirer.Text('symbol', message='Party symbol'),
        inquirer.Text('leader', message='Party leader'),
    ]
    answers = inquirer.prompt(questions)
    console.print("\n[bold cyan]Party Details[/bold cyan]")
    insert_data(connection, "insert_party", answers)
    print_table("show_inserted_party", "Inserted Party Details", answers)
    console.log(answers)

def add_candidate():
    console.print(Panel("[bold green]Add a New Candidate[/bold green]"))
    print_table("select_all_constituencies", "Constituencies")
    print_table("show_all_parties", "Parties")
    questions = [
        inquirer.Text('voter_id', message='Voter ID'),
        inquirer.Text('party_id', message='Enter Party id from the above table'),
        inquirer.Text('constituency_id', message='Enter Constituency id from the above table'),
    ]
    answers = inquirer.prompt(questions)
    console.print("\n[bold cyan]Candidate Details[/bold cyan]")
    insert_data(connection, "insert_candidate", answers)
    print_table("show_inserted_candidate", "Inserted Candidate Details", {"voter_id": answers["voter_id"]})
    contests_in_record_exists = select_data(connection, "check_if_contests_in_record_exists", {
        "party_id": answers["party_id"],
        "constituency_id": answers["constituency_id"]
    })
    if not contests_in_record_exists:
        insert_data(connection, "insert_contests_in", answers)
        console.print("\n[bold cyan]ContestsIn Record created[/bold cyan]")
        print_table("show_inserted_contests_in", "Inserted ContestsIn Details", {"party_id": answers["party_id"], "constituency_id": answers["constituency_id"]})
    else:
        console.print("\n[bold green]ContestsIn record already exists![/bold green]")
    console.log(answers)

def add_constituency():
    console.print(Panel("[bold green]Add a New Constituency[/bold green]"))
    questions = [
        inquirer.Text('name', message='Constituency name'),
        inquirer.Text('district', message='District'),
    ]
    answers = inquirer.prompt(questions)
    console.print("\n[bold cyan]Constituency Info:[/bold cyan]")
    insert_data(connection, "insert_constituency", answers)
    print_table("show_inserted_constituency", "Inserted Constituency Details", answers)
    console.log(answers)

def cast_vote(voter_id):
    has_voted = select_data(connection, "check_if_voter_has_voted", {"voter_id": voter_id})[0]["has_voted"]
    if has_voted:
        console.print("[red]You have already voted![/red]")
        return
    console.print(Panel("[bold green]Cast Your Vote[/bold green]\n"
                       "- Here are the list of candidates contesting in your constituency."))
    constituency_data = select_data(connection, "find_constituency_id_from_voter_id", {"voter_id": voter_id})[0]
    data = select_data(connection, "select_candidate_by_constituency_id", constituency_data)
    candidate_table = build_table_from_query_result(data, "select_candidate_by_constituency_id", "Candidates contesting in your constituency")
    console.print(candidate_table)
    questions = [
        inquirer.Text('candidate_id', message='Enter the candidate ID you want to vote for'),
    ]
    answers = inquirer.prompt(questions)
    insert_data(connection, "insert_vote_and_mark_voted", {
        "voter_id": voter_id,
        "candidate_id": answers['candidate_id'],
        "constituency_id": constituency_data["constituency_id"]
    })
    console.print("\n[bold cyan]Your vote has been casted successfully[/bold cyan]")

def show_results(voter_id, single_result):
    constituency_data = select_data(connection, "find_constituency_id_from_voter_id", {"voter_id": voter_id})[0]
    table = None
    if single_result:
        console.print("[cyan]Showing results for your constituency...[/cyan]")
        data = select_data(connection, "select_results_by_constituency_id", constituency_data)
        table = build_table_from_query_result(data, "select_results_by_constituency_id", "Results in your constituency")
    else:
        console.print("[cyan]Showing all results...[/cyan]")
        data = select_all_data(connection, "select_all_results")
        table = build_table_from_query_result(data, "select_all_results", "All Results")
    console.print(table)

def show_candidate_info(voter_id, single_result):
    constituency_data = select_data(connection, "find_constituency_id_from_voter_id", {"voter_id": voter_id})[0]
    table = None
    if single_result:
        console.print("[cyan]Showing candidates for your constituency...[/cyan]")
        data = select_data(connection, "select_candidate_by_constituency_id", constituency_data)
        table = build_table_from_query_result(data, "select_candidate_by_constituency_id", "Candidates contesting in your constituency")
    else:
        console.print("[cyan]Showing all candidates...[/cyan]")
        data = select_all_data(connection, "select_all_candidates")
        table = build_table_from_query_result(data, "select_all_candidates", "Candidates")
    console.print(table)

def show_party_info():
    console.print(Panel(
        "[bold cyan]Party Presence[/bold cyan]\n"
        "- See all parties and their respective constituencies they are contesting in."
    ))
    data = select_all_data(connection, "select_all_parties")
    table = build_table_from_query_result(data, "select_all_parties", "Parties")
    console.print(table)

def show_admin_info():
    console.print(Panel(
        "[bold cyan]Admin Details[/bold cyan]\n"
        "- See admin details."
    ))
    data = select_all_data(connection, "select_all_admins")
    table = build_table_from_query_result(data, "select_all_admins", "Admins")
    console.print(table)

def user_flow():
    console.print(Panel("[bold yellow]User Login[/bold yellow]"))
    voter_id = inquirer.text(message="Enter Voter ID")
    console.print(f"[green]Welcome, Voter {voter_id}![/green]")
    while True:
        action = show_user_menu()
        if action == 'Cast Vote':
            cast_vote(voter_id)
        elif action == 'See Results':
            sub_questions = [
                inquirer.List('result_option',
                              message="See Results for",
                              choices=[
                                  "Your Constituency",
                                  "All Candidates"
                              ])
            ]
            sub_answer = inquirer.prompt(sub_questions)
            if sub_answer['result_option'] == "Your Constituency":
                show_results(voter_id, True)
            elif sub_answer['result_option'] == "All Candidates":
                show_results(voter_id, False)
        elif action == 'Candidate Information':
            sub_questions = [
                inquirer.List('candidate_option',
                              message="Candidate Information for",
                              choices=[
                                  "Your Constituency",
                                  "All Candidates"
                              ])
            ]
            sub_answer = inquirer.prompt(sub_questions)
            if sub_answer['candidate_option'] == "Your Constituency":
                show_candidate_info(voter_id, True)
            elif sub_answer['candidate_option'] == "All Candidates":
                show_candidate_info(voter_id, False)
        elif action == 'Party Presence':
            show_party_info()
        elif action == 'Enquire Admin Details':
            show_admin_info()
        elif action == 'Logout to Main Menu':
            console.print("[green]Logged out![/green]")
            break
        sleep(1)
        console.print("\n[bold blue]Returning to user menu...[/bold blue]\n")

def admin_flow():
    console.print(Panel("[bold yellow]Admin Login[/bold yellow]"))
    admin_id = inquirer.text(message="Enter Admin ID")
    admin_pwd = inquirer.password(message="Enter Admin Password")
    is_authenticated = authenticate_admin(admin_id, admin_pwd)
    if is_authenticated:
        while True:
            action = show_admin_menu()
            if action == 'Add a new Voter to the DB':
                add_voter()
            elif action == 'Add a new Party to the DB':
                add_party()
            elif action == 'Add a new Candidate to the DB':
                add_candidate()
            elif action == 'Add a new Constituency to the DB':
                add_constituency()
            elif action == 'Add a new Admin to the DB':
                add_admin()
            elif action == 'Exit to Main Menu':
                console.print("\n[bold green]Thanks for using the Electronic Voter Management System![/bold green]")
                break
            sleep(1)
            console.print("\n[bold blue]Returning to admin menu...[/bold blue]\n")

def main():
    console.rule("[bold yellow]Electronic Voting System[/bold yellow]")
    while True:
        role = login_menu()
        if role == 'Admin':
            console.print(Panel("[bold green]Logged in as Admin[/bold green]"))
            admin_flow()
        elif role == 'Voter':
            user_flow()
        elif role == 'Exit':
            console.print("[green]Thanks for using the Electronic Voter Management System![/green]")
            break
        sleep(1)

if __name__ == "__main__":
    main()
