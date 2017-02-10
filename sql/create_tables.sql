
CREATE TABLE users (
    user_pk	serial primary key, -- symmatically meaningless pk out of habit
    username    varchar(16) unique,        -- 16 chars from spec
    password    varchar(16),        -- Think this will be long enough for hash
    create_dt   timestamp           -- Will be used to age out accounts
);

