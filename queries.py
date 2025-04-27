QUERY_MAP = {
    "insert_constituency": (
        "INSERT INTO Constituency (constituency_id, name, district) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_party": (
        "INSERT INTO Party (party_id, name, symbol) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_voter": (
        "INSERT INTO Voter (voter_id, aadhar, name, dob, gender, address, has_voted, constituency_id, candidate_id) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ),
    "insert_admin": (
        "INSERT INTO Admin (admin_id, name, email, pwd, voter_id) "
        "VALUES (%s, %s, %s, %s, %s)"
    ),
    "insert_candidate": (
        "INSERT INTO Candidate (candidate_id, name, voter_id, party_id) "
        "VALUES (%s, %s, %s, %s)"
    ),
    "insert_vote": (
        "INSERT INTO Vote (voter_id, candidate_id, constituency_id) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_contests": (
        "INSERT INTO Contests (party_id, constituency_id) "
        "VALUES (%s, %s)"
    ),
}

QUERY_PARAM_ORDER = {
    "insert_constituency": ["constituency_id", "name", "district"],
    "insert_party": ["party_id", "name", "symbol"],
    "insert_voter": [
        "voter_id", "aadhar", "name", "dob", "gender", "address",
        "has_voted", "constituency_id", "candidate_id"
    ],
    "insert_admin": ["admin_id", "name", "email", "pwd", "voter_id"],
    "insert_candidate": ["candidate_id", "name", "voter_id", "party_id"],
    "insert_vote": ["voter_id", "candidate_id", "constituency_id"],
    "insert_contests": ["party_id", "constituency_id"],
}


QUERY_HEADERS = {
    "get_candidate_by_constituency": ["Candidate ID", "Name", "Age", "Party ID", "Constituency ID"],
}
