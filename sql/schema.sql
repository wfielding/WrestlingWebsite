CREATE TABLE wrestlers(
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  weight_class INTEGER NOT NULL,
  gender VARCHAR(1) NOT NULL,
  pic VARCHAR(64) DEFAULT "pfp.jpg" NOT NULL,
  year VARCHAR(20) NOT NULL,
  password VARCHAR(256) NOT NULL,
  PRIMARY KEY(email)
);
CREATE TABLE admins(
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  position VARCHAR(20) NOT NULL,
  pic VARCHAR(64) DEFAULT "pfp.jpg" NOT NULL,
  password VARCHAR(256) NOT NULL,
  PRIMARY KEY(email)
);

CREATE TABLE images(
    filename VARCHAR(64) NOT NULL,
    PRIMARY KEY(filename)
);