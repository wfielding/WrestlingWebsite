CREATE TABLE wrestlers(
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  weight_class INTEGER NOT NULL,
  year INTEGER NOT NULL,
  password VARCHAR(256) NOT NULL,
  PRIMARY KEY(email)
);
CREATE TABLE admins(
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  password VARCHAR(256) NOT NULL,
  PRIMARY KEY(email)
);

CREATE TABLE images(
    filename VARCHAR(64) NOT NULL,
    PRIMARY KEY(filename)
);