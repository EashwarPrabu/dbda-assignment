QUERY_MAP = {
    # Insert queries
    "insert_constituency": (
        "INSERT INTO Constituency (name, district) "
        "VALUES (%s, %s)"
    ),
    "insert_party": (
        "INSERT INTO Party (name, symbol, party_leader) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_voter": (
        "INSERT INTO Voter (aadhar, name, dob, gender, address, constituency_id) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    ),
    "insert_admin": (
        "INSERT INTO Admin (name, email, pwd, voter_id) "
        "VALUES (%s, %s, %s, %s)"
    ),
    "insert_candidate": (
        "INSERT INTO Candidate (voter_id, party_id, constituency_id) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_vote": (
        "INSERT INTO Vote (voter_id, candidate_id, constituency_id) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_contests": (
        "INSERT INTO Contests (party_id, constituency_id) "
        "VALUES (%s, %s)"
    ),
    
    # Helper queries
    "select_all_constituencies": (
        "SELECT * FROM Constituency;"
    ),
    "select_all_parties": (
        "SELECT * FROM Party;"
    ),
    "find_constituency_id_from_voter_id": (
        "SELECT constituency_id FROM Voter WHERE voter_id = %s;"
    ),
    
    # Candidate details for single constituency using constituency_id
    "select_candidate_by_constituency_id": (
        "SELECT c.candidate_id, v.name AS candidate_name, p.name AS party_name, cons.name AS constituency_name "
        "FROM Candidate c, Voter v, Party p, Constituency cons "
        "WHERE v.voter_id = c.voter_id AND c.party_id = p.party_id AND c.constituency_id = cons.constituency_id AND c.constituency_id = %s;"
    ),
    # Candidate details for all constituencies
    "select_all_candidates": (
        "SELECT c.candidate_id, v.name AS candidate_name, p.name AS party_name, cons.name AS constituency_name "
        "FROM Candidate c, Voter v, Party p, Constituency cons "
        "WHERE v.voter_id = c.voter_id AND c.party_id = p.party_id AND c.constituency_id = cons.constituency_id"
    ),
    # Party details
    "select_all_parties": (
        "SELECT p.party_id, p.name AS party_name, cons.name AS constituency_name "
        "FROM Party p, Constituency cons, Contests c "
        "WHERE p.party_id = c.party_id AND cons.constituency_id = c.constituency_id;"
    ),
    # Admin details
    "select_all_admins": (
        "SELECT name, email FROM Admin;"
    ),
    # Results for a single constituency using constituency_id
    "select_results_by_constituency_id": (
        "SELECT c.candidate_id, vtr.name AS candidate_name, p.name AS party_name, COUNT(v.voter_id) AS vote_count "
        "FROM vote v, candidate c, voter vtr, party p "
        "WHERE v.candidate_id = c.candidate_id AND c.voter_id = vtr.voter_id AND c.party_id = p.party_id AND v.constituency_id = %s "
        "GROUP BY c.candidate_id, vtr.name, p.name "
        "ORDER BY vote_count DESC;"
    ),
    # Results for all constituencies
    "select_all_results": (        
        "SELECT c.candidate_id, vtr.name AS candidate_name, p.name AS party_name, COUNT(v.voter_id) AS vote_count "
        "FROM vote v, candidate c, voter vtr, party p "
        "WHERE v.candidate_id = c.candidate_id AND c.voter_id = vtr.voter_id AND c.party_id = p.party_id "
        "GROUP BY c.candidate_id, vtr.name, p.name "
        "ORDER BY vote_count DESC;")
}

QUERY_PARAM_ORDER = {
    "insert_constituency": ["name", "district"],
    "insert_party": ["name", "symbol", "party_leader"],
    "insert_voter": ["aadhar", "name", "dob", "gender", "address", "constituency_id"],
    "insert_admin": ["name", "email", "pwd", "voter_id"],
    "insert_candidate": ["voter_id", "party_id", "constituency_id"],
    "insert_vote": ["voter_id", "candidate_id", "constituency_id"],
    "insert_contests": ["party_id", "constituency_id"],
    "find_constituency_id_from_voter_id": ["voter_id"],
    "select_candidate_by_constituency_id": ["constituency_id"],
    "select_results_by_constituency_id": ["constituency_id"],
}


QUERY_HEADERS = {
    # "get_candidate_by_constituency": ["Candidate ID", "Name", "Age", "Party ID", "Constituency ID"],
    "select_all_constituencies": ["constituency_id", "name", "district"],
    "select_all_parties": ["party_id", "name", "symbol", "party_leader"],
    "select_candidate_by_constituency_id": ["candidate_id", "candidate_name", "party_name", "constituency_name"],
    "select_all_candidates": ["candidate_id", "candidate_name", "party_name", "constituency_name"],
    "select_all_parties": ["party_id", "party_name", "constituency_name"],
    "select_all_admins": ["name", "email"],
    "select_results_by_constituency_id": ["candidate_id", "candidate_name", "party_name", "vote_count"],
    "select_all_results": ["candidate_id", "candidate_name", "party_name", "vote_count"]
}
