-- Questions table schema
-- Stores coding practice questions with their metadata

CREATE TABLE IF NOT EXISTS questions(
    difficulty TEXT NOT NULL,
    id INTEGER PRIMARY KEY,
    paidOnly BOOLEAN NOT NULL,
    questionFrontendId INTEGER NOT NULL,
    title TEXT NOT NULL,
    titleSlug TEXT NOT NULL,
    acRate DECIMAL NOT NULL
);

-- Add index on difficulty for faster filtering
 CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);