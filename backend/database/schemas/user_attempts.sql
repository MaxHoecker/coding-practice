-- User Attempts table schema
-- Tracks user attempts on coding questions with status and timestamps

CREATE TABLE IF NOT EXISTS user_attempts (
    id TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question_id INTEGER REFERENCES questions(id),
    status TEXT NOT NULL,  -- e.g., 'started', 'completed', 'attempted'
    timestamp TEXT NOT NULL
);
