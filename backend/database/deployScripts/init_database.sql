-- Database initialization script
-- Run this to create all tables with their indexes

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

.read schemas/topics.sql
.read schemas/questions.sql
.read schemas/users.sql
.read schemas/questions.sql
.read schemas/user_attempts.sql