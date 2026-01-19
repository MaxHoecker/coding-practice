.mode csv

DELETE FROM questions;
.import --skip 1 deployScripts/questions.csv questions

DELETE FROM topics;
.import --skip 1 deployScripts/topics.csv topics

DELETE FROM question_tags;
.import --skip 1 deployScripts/question_tags.csv question_tags