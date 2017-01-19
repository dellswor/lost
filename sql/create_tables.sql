CREATE TABLE roles (
	role_pk		serial primary key,
	rolename	varchar(16)
);

CREATE TABLE users (
	user_pk		serial primary key,
	username	varchar(16),
	role_fk		integer REFERENCES roles(role_pk) not null
);
