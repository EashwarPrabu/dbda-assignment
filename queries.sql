-- CREATE TABLE QUERIES --
-- 1. CONSTITUENCY Table --
CREATE TABLE Constituency (
    constituency_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL
);

-- 2. PARTY Table --
CREATE TABLE Party (
    party_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(100),
    party_leader VARCHAR(100) NOT NULL
);

-- 3. VOTER Table --
CREATE TABLE Voter (
    voter_id INT PRIMARY KEY AUTO_INCREMENT,
    aadhar VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('M', 'F', 'O') NOT NULL,
    address VARCHAR(255) NOT NULL,
    has_voted BOOLEAN DEFAULT FALSE,
    constituency_id INT
);

-- 4. ADMIN Table --
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    pwd VARCHAR(255) NOT NULL,
    voter_id INT UNIQUE, 
    FOREIGN KEY (voter_id) REFERENCES Voter(voter_id)
);

-- 5. CANDIDATE Table --
CREATE TABLE Candidate (
    candidate_id INT PRIMARY KEY AUTO_INCREMENT,
    voter_id INT UNIQUE, 
    party_id INT, 
    constituency_id INT,
    FOREIGN KEY (voter_id) REFERENCES Voter(voter_id),
    FOREIGN KEY (party_id) REFERENCES Party(party_id),
    FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id)
);

-- 6. VOTE Table --
CREATE TABLE Vote (
    voter_id INT PRIMARY KEY,
    candidate_id INT NOT NULL,
    constituency_id INT NOT NULL,
    FOREIGN KEY (voter_id) REFERENCES Voter(voter_id),
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id),
    FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id)
);

-- 7. CONTESTS Table --
CREATE TABLE Contests (
    party_id INT,
    constituency_id INT,
    PRIMARY KEY (party_id, constituency_id),
    FOREIGN KEY (party_id) REFERENCES Party(party_id),
    FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id)
);

-- ALTERING CONSTRAINTS FOR VOTER TABLE --
ALTER TABLE Voter ADD CONSTRAINT fk_voter_constituency FOREIGN KEY (constituency_id) REFERENCES Constituency(constituency_id);

-- INSERT QUERIES --
-- 1. CONSTITUENCY --
INSERT INTO Constituency (name, district) VALUES ('North District', 'Springfield');

-- 2. PARTY --
INSERT INTO Party (name, symbol, party_leader) VALUES ('Progressive Party', 'PP', 'Adam Smith');

-- 3. VOTER --
INSERT INTO Voter (aadhar, name, dob, gender, address, constituency_id)
VALUES ('1234-5678-9012', 'John Doe', '1990-05-15', 'M', '123 Elm Street', 1);

-- 4. ADMIN --
INSERT INTO Admin (name, email, pwd, voter_id) VALUES ('Admin One', 'admin1@example.com', 'password123', 1);

-- 5. CANDIDATE --
INSERT INTO Candidate (voter_id, party_id, constituency_id) VALUES (1, 1, 1);

-- 6. VOTE --
INSERT INTO Vote (voter_id, candidate_id, constituency_id) VALUES (1, 1, 1);

-- 7. CONTESTS --
INSERT INTO Contests (party_id, constituency_id) VALUES (1, 1);

-- STORED PROCEDURE (Insert Vote record and update has_voted property in Voter table) --
DELIMITER $$
CREATE PROCEDURE insert_vote_and_mark_voted(
    IN p_voter_id INT,
    IN p_candidate_id INT,
    IN p_constituency_id INT
)
BEGIN
    # --- Insert Vote record ---
    INSERT INTO Vote (voter_id, candidate_id, constituency_id) VALUES (p_voter_id, p_candidate_id, p_constituency_id);

    # --- Update has_voted field in Voter table ---
    UPDATE Voter
    SET has_voted = TRUE
    WHERE voter_id = p_voter_id;
END$$
DELIMITER ;