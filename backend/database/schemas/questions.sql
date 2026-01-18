-- Questions table schema
-- Stores coding practice questions with their metadata

CREATE TABLE IF NOT EXISTS questions(
    id INTEGER PRIMARY KEY,
    topicId INTEGER REFERENCES topics(id),
    questionFrontendId INTEGER NOT NULL,
    paidOnly BOOLEAN NOT NULL,
    title TEXT NOT NULL,
    titleSlug TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    acRate REAL NOT NULL
);

-- Add index on difficulty for faster filtering
 CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);