CREATE TABLE IF NOT EXISTS ekko (
    ebeln  VARCHAR(10) PRIMARY KEY,                  -- purchase order number
    lifnr  VARCHAR(10) NOT NULL REFERENCES lfa1(lifnr),
    bsart  CHAR(4)     NOT NULL,                     -- order type
    bedat  DATE        NOT NULL,                     -- order date
    waers  CHAR(3)     NOT NULL,                     -- currency
    ernam  VARCHAR(12)                               -- created by
);

CREATE TABLE IF NOT EXISTS ekpo (
    ebeln  VARCHAR(10) NOT NULL REFERENCES ekko(ebeln),
    ebelp  CHAR(5)     NOT NULL,                     -- item number
    matnr  VARCHAR(18) NOT NULL REFERENCES mara(matnr),
    menge  NUMERIC(13,3) NOT NULL,                   -- quantity
    meins  CHAR(3)     NOT NULL,                     -- unit of measure
    netpr  NUMERIC(11,2) NOT NULL,                   -- net price per unit
    PRIMARY KEY (ebeln, ebelp)
);

CREATE TABLE IF NOT EXISTS vbak (
    vbeln  VARCHAR(10) PRIMARY KEY,                  -- sales order number
    auart  CHAR(4)     NOT NULL,                     -- order type
    erdat  DATE        NOT NULL,                     -- creation date
    kunnr  VARCHAR(10) NOT NULL,                     -- customer number
    waerk  CHAR(3)     NOT NULL                      -- currency
);

CREATE TABLE IF NOT EXISTS vbap (
    vbeln  VARCHAR(10) NOT NULL REFERENCES vbak(vbeln),
    posnr  CHAR(6)     NOT NULL,                     -- item number
    matnr  VARCHAR(18) NOT NULL REFERENCES mara(matnr),
    kwmeng NUMERIC(15,3) NOT NULL,                   -- ordered quantity
    vrkme  CHAR(3)     NOT NULL,                     -- sales unit
    netwr  NUMERIC(15,2) NOT NULL,                   -- net value
    PRIMARY KEY (vbeln, posnr)
);
