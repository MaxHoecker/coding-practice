
CREATE TABLE IF NOT EXISTS user_topics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    topic_id INTEGER REFERENCES topics(id)
);