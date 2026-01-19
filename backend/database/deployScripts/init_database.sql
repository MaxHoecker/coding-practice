-- Database initialization script
-- Run this to create all tables with their indexes

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS question_tags;
DROP TABLE IF EXISTS user_attempts;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS topics;

.read schemas/topics.sql

.read schemas/questions.sql

.read schemas/question_tags.sql

.read schemas/users.sql
.read schemas/questions.sql
.read schemas/user_attempts.sql

.read deployScripts/load_data.sql