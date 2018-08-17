CREATE TABLE messages (
    id            MEDIUMINT UNSIGNED NOT NULL AUTOINCREMENT,
    members_id    MEDIUMINT NOT NULL,
    comment        VARCHAR(20) NOT NULL,
    PRIMARY KEY(id)
);