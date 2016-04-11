/*
CREATE TABLE groupdeal_test.user_account
(
	user_id int NOT NULL PRIMARY KEY,
	username varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
);
*/
CREATE TABLE user_account
(
	user_id 	int				NOT NULL 	PRIMARY KEY		AUTOINCREMENT,
	username 	varchar(255) 	NOT NULL,
	password 	varchar(255) 	NOT NULL,
	address		varchar(255)
);

CREATE TABLE vendor
(
	vendor_id 	int 			NOT NULL 	PRIMARY KEY,
	name 		varchar(255) 	NOT NULL
);

CREATE TABLE product
(
	product_id 	int 			NOT NULL 	PRIMARY KEY,
	price 		int				NOT NULL,
	image 		blob,
	description varchar(1023s),
	vendor_id	int				NOT NULL,
	FOREIGN KEY(vendor_id) 		REFERENCES 	vendor(vendor_id)
);

CREATE TABLE vendor_account
(
	username 	varchar(255) 	NOT NULL,
	FOREIGN KEY(username) 		REFERENCES 	user_account(username)
);

CREATE TABLE consumer_account
(
	username 	varchar(255) 	NOT NULL,
	consumer_id int				NOT NULL,
	FOREIGN KEY(username) 		REFERENCES 	user_account(username),
	FOREIGN KEY(consumer_id)	REFERENCES  user_account(user_id)
);

CREATE TABLE contributions
(
	product_id  int        		NOT NULL,
	consumer_id int             NOT NULL,
	amount      numeric(8,2),
	FOREIGN KEY(product_id)		REFERENCES product,
	FOREIGN KEY(consumer_id)	REFERENCES consumer_account
);