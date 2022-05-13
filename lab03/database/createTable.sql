-- 支行表
Drop Table IF EXISTS Subbranch;

CREATE Table IF NOT EXISTS Subbranch(
    name varchar(64),
    city varchar(64),
    asset decimal(20, 2),
    Constraint PK_bname PRIMARY KEY(name)
);


-- 客户表
Drop Table IF EXISTS Client(
    id numeric(18,0),
    name varchar(256),
    phone numeric(11,0),
    address text,
    
)

