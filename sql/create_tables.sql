/* Table to enumarate valid roles and add the base roles */
CREATE TABLE roles (
    role	varchar(32) primary key
);
--INSERT INTO roles (role) VALUES ('System'); -- System role
INSERT INTO roles (role) VALUES ('Logistics Officer');
INSERT INTO roles (role) VALUES ('Facilities Officer');

/* Table to hold the users */
CREATE TABLE users (
    user_pk	serial primary key, -- symmatically meaningless pk out of habit
    username    varchar(16) unique,        -- 16 chars from spec
    password    varchar(16),        -- Think this will be long enough for hash
    create_dt   timestamp,          -- Will be used to age out accounts
    role        varchar(32) REFERENCES roles(role) not null -- setup role
);
--INSERT INTO users (username,password,create_dt,role) VALUES ('system',NULL,now(),'System'); -- System user, can't login due to NULL password
--INSERT INTO users (username,password,create_dt,role) VALUES ('log','l',now(),'Logistics Officer'); -- testing
--INSERT INTO users (username,password,create_dt,role) VALUES ('fac','f',now(),'Facilities Officer'); -- testing

CREATE TABLE facilities (
    facility_pk	     serial primary key, -- habit
    common_name      varchar(32),        -- spec
    fcode            varchar(6),         -- spec
    create_dt        timestamp not null,
    create_user      integer REFERENCES users(user_pk) not null
);
--INSERT INTO facilities (common_name,fcode,create_dt,create_user) VALUES ('Headquarters','HQ',now(),1);
--INSERT INTO facilities (common_name,fcode,create_dt,create_user) VALUES ('Capital','DC',now(),1);

CREATE TABLE assets (
    asset_pk         serial primary key, -- habit
    asset_tag        varchar(16) unique, -- spec, May break if tagging is poorly done
    description      text,
    create_dt        timestamp not null,
    create_user      integer REFERENCES users(user_pk) not null
);
--INSERT INTO assets (asset_tag,description,create_dt,create_user) VALUES ('A0001','Asset 1',now(),1);

CREATE TABLE asset_at (
    asset_fk         integer REFERENCES assets(asset_pk),
    facility_fk      integer REFERENCES facilities(facility_pk),
    arrive_dt        timestamp not null,
    depart_dt        timestamp,
    disposed_dt      timestamp
);
--INSERT INTO asset_at (asset_fk,facility_fk,arrive_dt,depart_dt) VALUES (1,1,'20170109T14:00:00','20170117T09:00:00');
--INSERT INTO asset_at (asset_fk,facility_fk,arrive_dt) VALUES (1,2,'20170117T09:00:00');