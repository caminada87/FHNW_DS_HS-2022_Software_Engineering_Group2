DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS permission;

CREATE TABLE user(
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

INSERT INTO permission (id, permission_name, permission_description) VALUES (0, 'User', 'login, predict, watch his predictions');
INSERT INTO permission (id, permission_name, permission_description) VALUES (1, 'SuperUser', 'login, predict, watch all predictions');
INSERT INTO permission (id, permission_name, permission_description) VALUES (2, 'Admin', 'login, CRUD predictions, CRUD users');

CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ip TEXT NOT NULL,
    query_data TEXT NOT NULL,
    predicted_price REAL NOT NULL
);