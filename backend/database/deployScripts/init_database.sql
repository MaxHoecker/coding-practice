-- Database initialization script
-- Run this to create all tables with their indexes

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

DROP TABLE topics;
.read schemas/topics.sql

DROP TABLE questions;
.read schemas/questions.sql

DROP TABLE question_tags;
.read schemas/question_tags.sql

.read schemas/users.sql
.read schemas/questions.sql
.read schemas/user_attempts.sql

.read deployScripts/load_data.sql