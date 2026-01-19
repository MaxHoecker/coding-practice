-- Database initialization script
-- Run this to create all tables with their indexes

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

DROP TABLE question_tags;
DROP TABLE user_attempts;
DROP TABLE questions;
DROP TABLE topics;

.read schemas/topics.sql

.read schemas/questions.sql

.read schemas/question_tags.sql

.read schemas/users.sql
.read schemas/questions.sql
.read schemas/user_attempts.sql

.read deployScripts/load_data.sql