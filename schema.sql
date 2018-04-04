CREATE TABLE IF NOT EXISTS users (
    id            SERIAL    PRIMARY KEY
                             UNIQUE
                             NOT NULL,
    name          CHAR (100) NOT NULL,
    username      CHAR (30)  NOT NULL
                             UNIQUE,
    email         CHAR (100) NOT NULL
                             UNIQUE,
    password      CHAR (100) NOT NULL,
    register_date TIMESTAMP   DEFAULT 'now',
    picture       VARCHAR    NOT NULL
                             DEFAULT ('/static/images/profile.png')
);
CREATE TABLE IF NOT EXISTS comments (
    user_id   INTEGER  REFERENCES users (id) ON DELETE CASCADE
                       NOT NULL,
    review_id INTEGER  REFERENCES reviews (id) ON DELETE CASCADE
                       NOT NULL,
    text      VARCHAR  NOT NULL
                       CHECK (LENGTH(text) > 0),
    date      TIMESTAMP NOT NULL
                       DEFAULT 'now'
);
CREATE TABLE IF NOT EXISTS follows (
    follower_id  INTEGER REFERENCES users (id) ON DELETE CASCADE
                         NOT NULL,
    following_id INTEGER REFERENCES users (id) ON DELETE CASCADE
                         NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
    id         SERIAL 	PRIMARY KEY 
                        UNIQUE
                        NOT NULL,
    user_id    INTEGER  REFERENCES users (id) ON DELETE CASCADE
                        NOT NULL,
    text       VARCHAR,
    subject_id INTEGER  REFERENCES subjects (id) ON DELETE CASCADE
                        NOT NULL,
    score      INTEGER  NOT NULL
                        CHECK (score >= 0 AND
                               score <= 5),
    date       TIMESTAMP DEFAULT 'now'
                        NOT NULL
);
CREATE TABLE IF NOT EXISTS subjects (
    id          SERIAL  PRIMARY KEY 
                        NOT NULL,
    type        VARCHAR NOT NULL
                        CHECK (type = 'album' OR
                               type = 'song'),
    name        NAME    NOT NULL,
    image       VARCHAR NOT NULL
                        DEFAULT ('/static/images/subject.png'),
    artist_name VARCHAR NOT NULL
);
CREATE TABLE IF NOT EXISTS votes (
    user_id   INTEGER REFERENCES users (id) ON DELETE CASCADE
                      NOT NULL,
    review_id INTEGER REFERENCES reviews (id) ON DELETE CASCADE,
    upvote    BOOLEAN NOT NULL
);
