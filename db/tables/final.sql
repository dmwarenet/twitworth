CREATE TABLE final (
        id              serial PRIMARY KEY,
	username	VARCHAR(200) UNIQUE,
	level1		integer NOT NULL,
	level2		integer NOT NULL,
	cost		VARCHAR(200) UNIQUE,
        created_at      timestamp DEFAULT current_timestamp
);
