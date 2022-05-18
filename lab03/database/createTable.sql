-- 创建基本表

-- 1.支行表 Subbranch
Drop Table IF EXISTS Subbranch;

Create Table IF NOT EXISTS Subbranch(
    name varchar(20),
    city varchar(64),
    asset decimal(20, 2),
    Constraint PK_branch Primary Key(name)
);


-- 2.部门表 Department
Drop Table IF EXISTS Department;

Create Table IF NOT EXISTS Department(
    id char(8),
    name varchar(20),
    type varchar(30),
    subbranch_name varchar(20),
    leader_id char(18),
    Constraint PK_department Primary Key(id),
    Constraint FK_department1 Foreign Key(subbranch_name) References Subbranch(name)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
    -- Constraint FK_department2 Foreign Key(leader_id) References staff(id)
);


-- 3.员工表 Staff
Drop Table IF EXISTS Staff;

Create Table IF NOT EXISTS Staff(
    id char(18),
    name varchar(20),
    phone char(11),
    address varchar(100),
    department_id char(8),
    hire_date date,
    Constraint PK_staff Primary Key(id),
    Constraint FK_staff1 Foreign Key(department_id) References Department(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 部门经理（外键）
Alter Table Department
    Add Constraint FK_department2 Foreign Key(leader_id) References staff(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;



-- 4.客户表 Client
Drop Table IF EXISTS Client;

Create Table IF NOT EXISTS Client(
    id char(18),
    name varchar(20),
    phone char(11),
    address varchar(100),
    staff_id char(8),
    staff_type bool,
    Constraint PK_client Primary Key(id),
    Constraint FK_client1 Foreign Key(staff_id) References Staff(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


 -- 5.联系人表 Contact
Drop Table IF EXISTS Contact;

Create Table IF NOT EXISTS Contact(
    client_id char(18),
    name varchar(20),
    phone char(11),
    email varchar(50),
    relation varchar(20),
    Constraint PK_contact Primary Key(client_id, name),
    Constraint FK_contact1 Foreign Key(client_id) References Client(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- 6.账户表 Account
Drop Table IF EXISTS Account;

Create Table IF NOT EXISTS Account(
    id char(20),
    balance decimal(20,2),
    open_date datetime,
    Constraint PK_account Primary Key(id)
);


-- 7.储蓄账户表 SavingsAccount
Drop Table IF EXISTS SavingsAccount;

Create Table IF NOT EXISTS SavingsAccount(
    account_id char(20),
    interest_rate decimal,
    currency_type varchar(20),
    Constraint PK_sa Primary Key(account_id),
    Constraint FK_sa1 Foreign Key(account_id) References Account(id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);


-- 8.支票账户表 CheckingAccount
Drop Table IF EXISTS CheckingAccount;

Create Table IF NOT EXISTS CheckingAccount(
    account_id char(20),
    overdraft decimal(20,2),
    Constraint PK_ca Primary Key(account_id),
    Constraint FK_ca1 Foreign Key(account_id) References Account(id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);


-- 9.访问账户表 AccessAccount
Drop Table IF EXISTS AccessAccount;

Create Table IF NOT EXISTS AccessAccount(
    account_id char(20),
    client_id char(18),
    least_recently_access datetime,
    Constraint PK_aa Primary Key(account_id, client_id),
    Constraint FK_aa1 Foreign Key(account_id) References Account(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    Constraint FK_aa2 Foreign Key(client_id) References Client(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- 10.贷款表 Loan
Drop Table IF EXISTS Loan;

Create Table IF NOT EXISTS Loan(
    id char(20),
    subbranch_name varchar(20),
    loan_amount decimal(20,2),
    Constraint PK_loan Primary Key(id),
    Constraint FK_loan1 Foreign Key(subbranch_name) References Subbranch(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- 11.支付贷款表 PayLoan
Drop Table IF EXISTS PayLoan;

Create Table IF NOT EXISTS PayLoan(
    loan_id char(20),
    pay_date datetime,
    pay_amount decimal(20,2),
    Constraint PK_pl Primary Key(loan_id, pay_date),
    Constraint FK_pl1 Foreign Key(loan_id) References Loan(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- 12.客户_贷款表 ClientLoan
Drop Table IF EXISTS ClientLoan;

Create Table IF NOT EXISTS ClientLoan(
    loan_id char(20),
    client_id char(18),
    Constraint PK_cl Primary Key(loan_id, client_id),
    Constraint FK_cl1 Foreign Key(loan_id) References Loan(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    Constraint FK_cl2 Foreign Key(client_id) References Client(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);