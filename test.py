from db import connect_to_db, insert_data, select_data, select_all_data
from queries import QUERY_MAP
from rich.console import Console
from rich.table import Table
import bcrypt
from helper import database_helper

console = Console()
connection = connect_to_db()

results = []

def Test(title, description):
    def decorator(func):
        def wrapper():
            try:
                func()
                results.append((title, description, "[green]PASS[/green]"))
            except Exception as e:
                results.append((title, description, f"[red]FAIL[/red]: {e}"))
        return wrapper
    return decorator

def clear_test_data():
    cursor = connection.cursor()
    for table in ["Vote", "Candidate", "Admin", "Voter", "ContestsIn", "Party", "Constituency"]:
        cursor.execute(f"DELETE FROM {table}")
    connection.commit()

@Test("Insert Constituency", "Insert a new constituency into the database")
def test_insert_constituency():
    insert_data(connection, "insert_constituency", {"name": "TestZone", "district": "TestDistrict"})
    res = select_data(connection, "show_inserted_constituency", {"name": "TestZone", "district": "TestDistrict"})
    assert len(res) == 1

@Test("Insert Party", "Insert a new party into the database")
def test_insert_party():
    insert_data(connection, "insert_party", {"name": "Test Party", "symbol": "TP", "leader": "Leader One"})
    res = select_data(connection, "show_inserted_party", {"name": "Test Party", "symbol": "TP", "leader": "Leader One"})
    assert len(res) == 1

@Test("Insert Voter", "Insert a new voter into the database")
def test_insert_voter():
    insert_data(connection, "insert_voter", {
        "aadhar": "000011112222",
        "name": "Jane Voter",
        "dob": "1990-10-10",
        "gender": "F",
        "address": "Test Address",
        "constituency_id": 2
    })
    res = select_data(connection, "show_inserted_voter", {"aadhar": "000011112222"})
    assert len(res) == 1

@Test("Insert Candidate", "Insert a new candidate into the database")
def test_insert_candidate():
    insert_data(connection, "insert_candidate", {
        "voter_id": 2,
        "party_id": 2,
        "constituency_id": 2
    })
    res = select_data(connection, "show_inserted_candidate", {"voter_id": 2})
    assert len(res) == 1

@Test("Insert Contests In", "Insert a new contests in record into the database")
def test_insert_contests_in():
    insert_data(connection, "insert_contests_in", {
        "party_id": 2,
        "constituency_id": 2
    })
    res = select_data(connection, "show_inserted_contests_in", {"party_id": 2, "constituency_id": 2})
    assert len(res) == 1

@Test("Insert Admin", "Insert a new admin into the database")
def test_insert_admin():
    hashed_pwd = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    insert_data(connection, "insert_admin", {
        "email": "admin@test.com",
        "pwd": hashed_pwd,
        "voter_id": 2
    })
    res = select_data(connection, "show_inserted_admin", {"email": "admin@test.com"})
    assert len(res) == 1

@Test("Cast Vote using Stored Procedure", "Cast a vote for a candidate")
def test_cast_vote():
    insert_data(connection, "insert_vote_and_mark_voted", {
        "voter_id": 2,
        "candidate_id": 2,
        "constituency_id": 2
    })
    res = select_data(connection, "check_if_voter_has_voted", {"voter_id": 2})
    assert res[0]["has_voted"] == 1

@Test("Fetch Election Results", "Fetch results for a specific constituency")
def test_fetch_results():
    res = select_data(connection, "select_results_by_constituency_id", {"constituency_id": 2})
    assert any(r["vote_count"] > 0 for r in res)

@Test("Check Constituency Count", "Verify constituencies in the database")
def test_constituency_presence():
    res = select_all_data(connection, "select_all_constituencies")
    assert len(res) == 2

@Test("Check Candidate Count", "Verify candidates in the database")
def test_candidate_count():
    res = select_all_data(connection, "select_all_candidates")
    assert len(res) == 2

@Test("Check Party Presence", "Verify parties in the database")
def test_party_presence():
    res = select_all_data(connection, "select_all_parties")
    assert len(res) == 2

@Test("Check Admin Details", "Verify admin details in the database")
def test_admin_presence():
    res = select_all_data(connection, "select_all_admins")
    assert len(res) == 2

if __name__ == "__main__":
    database_helper()
    test_insert_constituency()
    test_insert_party()
    test_insert_voter()
    test_insert_candidate()
    test_insert_contests_in()
    test_insert_admin()
    test_cast_vote()
    test_fetch_results()
    test_constituency_presence()
    test_candidate_count()
    test_party_presence()
    test_admin_presence()

    table = Table(title="Functionality Test Results")
    table.add_column("Test Case", style="cyan")
    table.add_column("Test Description", style="cyan")
    table.add_column("Test Result", style="bold")

    for title, description, result in results:
        table.add_row(title, description, result)

    console.print(table)
    clear_test_data()
    connection.close()