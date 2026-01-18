-- Users table schema
-- Stores user accounts and their creation timestamps

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL
);
