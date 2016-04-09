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
	user_id 	int				NOT NULL 	PRIMARY KEY,
	username 	varchar(255) 	NOT NULL,
	password 	varchar(255) 	NOT NULL
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
	description varchar(255),
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
	FOREIGN KEY(username) 		REFERENCES 	user_account(username)
);