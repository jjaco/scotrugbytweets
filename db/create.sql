\c scotrugbytweet;
CREATE TABLE tweets (
 id VARCHAR PRIMARY KEY,
 timestamp TIMESTAMP NOT NULL,
 tweet VARCHAR NOT NULL,
 entities VARCHAR NOT NULL
);