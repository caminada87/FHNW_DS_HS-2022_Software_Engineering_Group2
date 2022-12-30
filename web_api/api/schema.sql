DROP TABLE IF EXISTS api_key;
DROP TABLE IF EXISTS developer;
DROP TABLE IF EXISTS permission;

CREATE TABLE api_key(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consumer_name TEXT UNIQUE NOT NULL,
    api_key TEXT UNIQUE NOT NULL,
    developer_id INTEGER NOT NULL,
    FOREIGN KEY (developer_id) 
      REFERENCES developer (id) 
         ON DELETE CASCADE 
         ON UPDATE CASCADE
);

CREATE TABLE developer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    permission_id INTEGER NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (permission_id) 
      REFERENCES permission (id) 
         ON DELETE NO ACTION 
         ON UPDATE CASCADE
);

CREATE TABLE permission(
    id INTEGER PRIMARY KEY,
    permission_name TEXT UNIQUE NOT NULL,
    permission_description TEXT NOT NULL
);

INSERT INTO permission (id, permission_name, permission_description) VALUES (-1, 'Unregistered', 'registration process');
INSERT INTO permission (id, permission_name, permission_description) VALUES (0, 'Developer', 'login, create and read own API KEYs');
INSERT INTO permission (id, permission_name, permission_description) VALUES (1, 'Admin', 'login, CRD API KEYs, manage develpers');

INSERT INTO developer (email, permission_id, password) VALUES ('scam87@gmail.com', 1, 'pbkdf2:sha256:260000$lIjiXc8EAdvL3FLG$62b93b2b739e84f1355f5db813eba3363c90c58d4a029e86fd31dca2108a45b0');
INSERT INTO api_key (consumer_name, api_key, developer_id) VALUES ('frontend', '7c106cb1c4c040998b7a447e3a96d742', (SELECT id FROM developer WHERE email = 'scam87@gmail.com' LIMIT 1));