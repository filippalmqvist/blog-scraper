CREATE TABLE source_codes(
   source_code VARCHAR (64) PRIMARY KEY,
   description VARCHAR (256) NOT NULL,
   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE posts(
   post_id serial PRIMARY KEY,
   ext_id VARCHAR (64) UNIQUE NOT NULL,
   title VARCHAR (64) NOT NULL,
   link VARCHAR (256) UNIQUE NOT NULL,
   source_code VARCHAR (64) REFERENCES source_codes(source_code) NOT NULL,
   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


