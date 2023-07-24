CREATE TABLE books (
  id SERIAL,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  publisher VARCHAR(255) NOT NULL,
  isbn VARCHAR(20) NOT NULL UNIQUE,
  primary key(id)
);


CREATE TABLE users(
  id SERIAL,
  user_name VARCHAR(50) NOT NULL,
  hashed_password VARCHAR(64) NOT NULL,
  salt VARCHAR(32) NOT NULL,
  mail VARCHAR(255) NOT NULL UNIQUE,
  primary key(id)
);

CREATE TABLE review (
  id SERIAL,
  book_id INT NOT NULL,
  title VARCHAR(50),
  comment TEXT NOT NULL,
  FOREIGN KEY (book_id) REFERENCES book(id)
);


CREATE TABLE lending (
	id SERIAL,
	book_id INT NOT NULL,
	user_id INT NOT NULL,
	lending_date TIMESTAMP NOT NULL,
	return_date TIMESTAMP,
	return_status varchar(1),
	FOREIGN KEY (book_id) REFERENCES book(id),
	FOREIGN KEY (user_id) REFERENCES users(id)
);






	CREATE TABLE lending (
	id SERIAL,
	book_id INT NOT NULL,
	user_id INT NOT NULL,
	lending_date TIMESTAMP NOT NULL,
	return_date TIMESTAMP,
	return_status VARCHAR(1) DEFAULT '未',
	FOREIGN KEY (book_id) REFERENCES book(id),
	FOREIGN KEY (user_id) REFERENCES users(id)
);
