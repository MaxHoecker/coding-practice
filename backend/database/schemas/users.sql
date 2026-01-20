-- Users table schema
-- Stores user accounts and their creation timestamps

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    new_question_weight NOT NULL DEFAULT 50,
    attempted_weight INTEGER NOT NULL DEFAULT 30,
    completed_weight INTEGER NOT NULL DEFAULT 20,
    easy_difficulty BOOLEAN DEFAULT TRUE,
    medium_difficulty BOOLEAN DEFAULT TRUE,
    hard_difficulty BOOLEAN DEFAULT FALSE,
    attempted_timing_days INTEGER NOT NULL DEFAULT 3,
    completed_timing_days INTEGER NOT NULL DEFAULT 7,
    view_paid_only BOOLEAN DEFAULT FALSE
);
