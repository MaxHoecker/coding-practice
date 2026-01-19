

CREATE TABLE IF NOT EXISTS question_tags(
    id INTEGER PRIMARY KEY,
    questionId INTEGER REFERENCES questions(id),
    topicId INTEGER REFERENCES topics(id)
);