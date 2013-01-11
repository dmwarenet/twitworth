CREATE TABLE call (
        id              serial PRIMARY KEY,
	call_type	integer NOT NULL,
        created_at      timestamp DEFAULT current_timestamp
);
