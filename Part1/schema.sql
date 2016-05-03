CREATE TABLE user_account
(
	user_id 	INTEGER			NOT NULL 	PRIMARY KEY		AUTOINCREMENT,
	username 	varchar(255) 	NOT NULL,
	password 	varchar(255) 	NOT NULL,
	address		varchar(255)
);

CREATE TABLE vendor
(
	vendor_name varchar(255) 	NOT NULL 	PRIMARY KEY
);

CREATE TABLE campaign
(
	campaign_id 	INTEGER			NOT NULL 	PRIMARY KEY 	AUTOINCREMENT,
	campaign_name 	varchar(255) 	NOT NULL,
	price 			numeric(8,2)	NOT NULL,
	image 			varchar(255),
	descr 			varchar(1023),
	descr_simple	varchar(1023),
	num_pledges		INTEGER,
	vendor_name		varchar(255)	NOT NULL,
	FOREIGN KEY(vendor_name) 		REFERENCES 	vendor(vendor_name)
);

CREATE TABLE price_points
(
	campaign_id 	INTEGER			NOT NULL,
	pledge_num		INTEGER			NOT NULL,
	new_price		numeric(8,2)	NOT NULL,
	FOREIGN KEY(campaign_id)		REFERENCES 	campaign(campaign_id)
);

CREATE TABLE vendor_account
(
	username 	varchar(255) 	NOT NULL,
	FOREIGN KEY(username) 		REFERENCES 	user_account(username)
);

CREATE TABLE consumer_account
(
	username 	varchar(255) 	NOT NULL,
	consumer_id INTEGER			NOT NULL,
	FOREIGN KEY(username) 		REFERENCES 	user_account(username),
	FOREIGN KEY(consumer_id)	REFERENCES  user_account(user_id)
);

CREATE TABLE payment_info
(
	consumer_id	INTEGER			NOT NULL,
	card_num	BIGINT			NOT NULL,
	security	INTEGER,
	FOREIGN KEY(consumer_id)	REFERENCES	consumer_account(consumder_id)
);

CREATE TABLE contributions
(
	campaign_id  	INTEGER        	NOT NULL,
	consumer_id 	INTEGER         NOT NULL,
	amount      	numeric(8,2),
	FOREIGN KEY(campaign_id)		REFERENCES campaign(campaign_id),
	FOREIGN KEY(consumer_id)		REFERENCES consumer_account
);