QUERY_MAP = {
    "create_constituency": (
        "CREATE TABLE IF NOT EXISTS Constituency (constituency_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100) NOT NULL, district VARCHAR(100) NOT NULL)"
    ),
    "create_party": (
        "CREATE TABLE IF NOT EXISTS Party (party_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100) NOT NULL, symbol VARCHAR(100), leader VARCHAR(100) NOT NULL)"
    ),
    "create_voter": (
        "CREATE TABLE IF NOT EXISTS Voter (voter_id INT PRIMARY KEY AUTO_INCREMENT, aadhar VARCHAR(20) UNIQUE NOT NULL, name VARCHAR(100) NOT NULL, dob DATE NOT NULL, gender ENUM('M', 'F', 'O') NOT NULL, address VARCHAR(255) NOT NULL, has_voted BOOLEAN DEFAULT FALSE, constituency_id INT)"
    ),
    "create_admin": (
        "CREATE TABLE IF NOT EXISTS Admin (admin_id INT PRIMARY KEY AUTO_INCREMENT, email VARCHAR(100) UNIQUE NOT NULL, pwd VARCHAR(255) NOT NULL, voter_id INT UNIQUE, FOREIGN KEY (voter_id) REFERENCES Voter(voter_id))"
    ),
    "create_candidate": (
        "CREATE TABLE IF NOT EXISTS Candidate (candidate_id INT PRIMARY KEY AUTO_INCREMENT, voter_id INT UNIQUE, party_id INT, constituency_id INT, FOREIGN KEY (voter_id) REFERENCES Voter(voter_id), FOREIGN KEY (party_id) REFERENCES Party(party_id), FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id))"
    ),
    "create_vote": (
        "CREATE TABLE IF NOT EXISTS Vote (voter_id INT PRIMARY KEY, candidate_id INT NOT NULL, constituency_id INT NOT NULL, FOREIGN KEY (voter_id) REFERENCES Voter(voter_id), FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id), FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id))"
    ),
    "create_contests_in": (
        "CREATE TABLE IF NOT EXISTS ContestsIn (party_id INT, constituency_id INT, PRIMARY KEY (party_id, constituency_id), FOREIGN KEY (party_id) REFERENCES Party(party_id), FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id))"
    ),
    "check_if_voter_fk_constraint_exists": (
        "SELECT CONSTRAINT_NAME FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Voter' AND CONSTRAINT_TYPE = 'FOREIGN KEY' AND CONSTRAINT_NAME = 'fk_voter_constituency'"
    ),
    "add_voter_fk_constraint": (
        "ALTER TABLE Voter ADD CONSTRAINT fk_voter_constituency FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id)"
    ),
    # Insert queries
    "insert_constituency": (
        "INSERT INTO Constituency (name, district) "
        "VALUES (%s, %s)"
    ),
    "insert_party": (
        "INSERT INTO Party (name, symbol, leader) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_voter": (
        "INSERT INTO Voter (aadhar, name, dob, gender, address, constituency_id) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    ),
    "insert_admin": (
        "INSERT INTO Admin (email, pwd, voter_id) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_candidate": (
        "INSERT INTO Candidate (voter_id, party_id, constituency_id) "
        "VALUES (%s, %s, %s)"
    ),
    "insert_contests_in": (
        "INSERT INTO ContestsIn (party_id, constituency_id) "
        "VALUES (%s, %s)"
    ),

    # Stored procedure to insert vote and mark voter as voted
    "insert_vote_and_mark_voted": (
        "CALL insert_vote_and_mark_voted(%s, %s, %s)"
    ),

    "show_inserted_constituency": (
        "SELECT constituency_id, name, district FROM Constituency WHERE name = %s AND district = %s"
    ),
    "show_inserted_party": (
        "SELECT party_id, name, symbol, leader FROM Party WHERE name = %s AND symbol = %s AND leader = %s"
    ),
    "show_inserted_voter": (
        "SELECT voter_id, aadhar, name, dob, gender, address, has_voted, constituency_id FROM Voter WHERE aadhar = %s"
    ),
    "show_inserted_admin": (
        "SELECT admin_id, email, voter_id FROM Admin WHERE email = %s"
    ),
    "show_inserted_candidate": (
        "SELECT candidate_id, voter_id, party_id, constituency_id FROM Candidate WHERE voter_id = %s"
    ),
    "show_inserted_contests_in": (
        "SELECT party_id, constituency_id FROM ContestsIn WHERE party_id = %s AND constituency_id = %s"
    ),
    
    # Helper queries
    "select_all_constituencies": (
        "SELECT * FROM Constituency;"
    ),
    "show_all_parties": (
        "SELECT * FROM Party;"
    ),
    "find_constituency_id_from_voter_id": (
        "SELECT constituency_id FROM Voter WHERE voter_id = %s"
    ),
    "check_if_voter_has_voted": (
        "SELECT has_voted FROM Voter WHERE voter_id = %s"
    ),
    "check_if_contests_in_record_exists": (
        "SELECT 1 AS is_exists FROM ContestsIn WHERE party_id = %s AND constituency_id = %s"
    ),
    "find_admin_by_id": (
        "SELECT admin_id, pwd FROM Admin WHERE admin_id = %s"
    ),
    
    # Candidate details for single constituency using constituency_id
    "select_candidate_by_constituency_id": (
        "SELECT c.candidate_id, v.name AS candidate_name, p.name AS party_name, cons.name AS constituency_name "
        "FROM Candidate c, Voter v, Party p, Constituency cons "
        "WHERE v.voter_id = c.voter_id AND c.party_id = p.party_id AND c.constituency_id = cons.constituency_id AND c.constituency_id = %s"
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
        "FROM Party p, Constituency cons, ContestsIn c "
        "WHERE p.party_id = c.party_id AND cons.constituency_id = c.constituency_id"
    ),
    # Admin details
    "select_all_admins": (
        "SELECT v.name, a.email FROM Admin a, Voter v WHERE a.voter_id = v.voter_id"
    ),
    # Results for a single constituency using constituency_id
    "select_results_by_constituency_id": (
        "SELECT c.candidate_id, vtr.name AS candidate_name, p.name AS party_name, COUNT(v.voter_id) AS vote_count "
        "FROM vote v, candidate c, voter vtr, party p "
        "WHERE v.candidate_id = c.candidate_id AND c.voter_id = vtr.voter_id AND c.party_id = p.party_id AND v.constituency_id = %s "
        "GROUP BY c.candidate_id, vtr.name, p.name "
        "ORDER BY vote_count DESC"
    ),
    # Results for all constituencies
    "select_all_results": (        
        "SELECT c.candidate_id, vtr.name AS candidate_name, p.name AS party_name, COUNT(v.voter_id) AS vote_count "
        "FROM vote v, candidate c, voter vtr, party p "
        "WHERE v.candidate_id = c.candidate_id AND c.voter_id = vtr.voter_id AND c.party_id = p.party_id "
        "GROUP BY c.candidate_id, vtr.name, p.name "
        "ORDER BY vote_count DESC"
    )
}

QUERY_PARAM_ORDER = {
    "insert_constituency": ["name", "district"],
    "insert_party": ["name", "symbol", "leader"],
    "insert_voter": ["aadhar", "name", "dob", "gender", "address", "constituency_id"],
    "insert_admin": ["email", "pwd", "voter_id"],
    "insert_candidate": ["voter_id", "party_id", "constituency_id"],
    "insert_vote": ["voter_id", "candidate_id", "constituency_id"],
    "insert_contests_in": ["party_id", "constituency_id"],

    "show_inserted_constituency": ["name", "district"],
    "show_inserted_party": ["name", "symbol", "leader"],
    "show_inserted_voter": ["aadhar"],
    "show_inserted_admin": ["email"],
    "show_inserted_candidate": ["voter_id"],
    "show_inserted_contests_in": ["party_id", "constituency_id"],

    "find_constituency_id_from_voter_id": ["voter_id"],
    "check_if_voter_has_voted": ["voter_id"],
    "check_if_contests_in_record_exists": ["party_id", "constituency_id"],
    "find_admin_by_id": ["admin_id"],
    
    "select_candidate_by_constituency_id": ["constituency_id"],
    "select_results_by_constituency_id": ["constituency_id"],

    "insert_vote_and_mark_voted": ["voter_id", "candidate_id", "constituency_id"],
}


QUERY_HEADERS = {
    "select_all_constituencies": ["constituency_id", "name", "district"],
    "show_all_parties": ["party_id", "name", "symbol", "leader"],
    "select_candidate_by_constituency_id": ["candidate_id", "candidate_name", "party_name", "constituency_name"],
    "select_all_candidates": ["candidate_id", "candidate_name", "party_name", "constituency_name"],
    "select_all_parties": ["party_id", "party_name", "constituency_name"],
    "select_all_admins": ["name", "email"],
    "select_results_by_constituency_id": ["candidate_id", "candidate_name", "party_name", "vote_count"],
    "select_all_results": ["candidate_id", "candidate_name", "party_name", "vote_count"],
    "show_inserted_constituency": ["constituency_id", "name", "district"],
    "show_inserted_party": ["party_id", "name", "symbol", "leader"],
    "show_inserted_voter": ["voter_id", "aadhar", "name", "dob", "gender", "address", "has_voted", "constituency_id"],
    "show_inserted_admin": ["admin_id", "email", "voter_id"],
    "show_inserted_candidate": ["candidate_id", "voter_id", "party_id", "constituency_id"],
    "show_inserted_contests_in": ["party_id", "constituency_id"],

}
