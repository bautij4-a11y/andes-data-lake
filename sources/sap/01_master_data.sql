CREATE TABLE IF NOT EXISTS mara (
    matnr  VARCHAR(18) PRIMARY KEY,  -- material number
    maktx  VARCHAR(40) NOT NULL,     -- material description
    mtart  CHAR(4)     NOT NULL,     -- material type (ROH raw, FERT finished, HALB semi)
    matkl  VARCHAR(9),               -- material group
    meins  CHAR(3)     NOT NULL,     -- base unit of measure
    brgew  NUMERIC(13,3),            -- gross weight
    ersda  DATE        NOT NULL      -- creation date
);

CREATE TABLE IF NOT EXISTS lfa1 (
    lifnr  VARCHAR(10) PRIMARY KEY,  -- vendor number
    name1  VARCHAR(35) NOT NULL,     -- vendor name
    land1  CHAR(2)     NOT NULL,     -- country key
    ort01  VARCHAR(35),              -- city
    ktokk  CHAR(4),                  -- vendor account group
    erdat  DATE        NOT NULL      -- creation date
);
