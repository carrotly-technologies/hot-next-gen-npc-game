CREATE TABLE NPC
(
    id          INT PRIMARY KEY,
    name        VARCHAR(255),
    description TEXT
);

CREATE TABLE Correlations
(
    id          INT PRIMARY KEY,
    description TEXT,
    npcId       INT,
    opinion     TEXT,
    FOREIGN KEY (npcId) REFERENCES NPC (id)
);

CREATE TABLE Event
(
    id          INT PRIMARY KEY,
    npcId       INT,
    description TEXT,
    FOREIGN KEY (npcId) REFERENCES NPC (id)
);

CREATE TABLE Building
(
    id      INT PRIMARY KEY,
    name    VARCHAR(255),
    pattern VARCHAR(255)
);

-- CREATE TABLE SendEvent
-- (
--     playerId    VARCHAR(255),
--     npcId       INT,
--     description TEXT,
--     FOREIGN KEY (npcId) REFERENCES NPC (id)
-- );