--
-- Create model Account
--
CREATE TABLE `bank_account` (`id` varchar(20) NOT NULL PRIMARY KEY, `balanch` numeric(20, 2) NOT NULL, `open_date` datetime(6) NOT NULL);
--
-- Create model Client
--
CREATE TABLE `bank_client` (`id` varchar(18) NOT NULL PRIMARY KEY, `name` varchar(20) NOT NULL, `phone` varchar(11) NOT NULL, `address` varchar(100) NOT NULL, `staff_type` bool NOT NULL);
--
-- Create model Department
--
CREATE TABLE `bank_department` (`id` varchar(8) NOT NULL PRIMARY KEY, `name` varchar(20) NOT NULL, `type` varchar(30) NOT NULL);
--
-- Create model Loan
--
CREATE TABLE `bank_loan` (`id` varchar(20) NOT NULL PRIMARY KEY);
--
-- Create model Subbranch
--
CREATE TABLE `bank_subbranch` (`name` varchar(20) NOT NULL PRIMARY KEY, `city` varchar(64) NOT NULL, `asset` numeric(20, 2) NOT NULL);
--
-- Create model CheckingAccount
--
CREATE TABLE `bank_checkingaccount` (`account_id_id` varchar(20) NOT NULL PRIMARY KEY, `overdraft` numeric(20, 2) NOT NULL);
--
-- Create model SavingsAccount
--
CREATE TABLE `bank_savingsaccount` (`account_id_id` varchar(20) NOT NULL PRIMARY KEY, `currency_type` varchar(20) NOT NULL);
--
-- Create model Staff
--
CREATE TABLE `bank_staff` (`id` varchar(18) NOT NULL PRIMARY KEY, `name` varchar(20) NOT NULL, `phone` varchar(11) NOT NULL, `address` varchar(100) NOT NULL, `hire_date` date NOT NULL, `department_id_id` varchar(8) NOT NULL);
--
-- Create model PayLoan
--
CREATE TABLE `bank_payloan` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `pay_date` datetime(6) NOT NULL, `pay_amount` numeric(20, 2) NOT NULL, `loan_id_id` varchar(20) NOT NULL);
--
-- Add field subbranch_name to loan
--
ALTER TABLE `bank_loan` ADD COLUMN `subbranch_name_id` varchar(20) NOT NULL , ADD CONSTRAINT `bank_loan_subbranch_name_id_89793da1_fk_bank_subbranch_name` FOREIGN KEY (`subbranch_name_id`) REFERENCES `bank_subbranch`(`name`);
--
-- Add field leader_id to department
--
ALTER TABLE `bank_department` ADD COLUMN `leader_id_id` varchar(18) NOT NULL , ADD CONSTRAINT `bank_department_leader_id_id_63b911f0_fk_bank_staff_id` FOREIGN KEY (`leader_id_id`) REFERENCES `bank_staff`(`id`);
--
-- Add field subbranch_name to department
--
ALTER TABLE `bank_department` ADD COLUMN `subbranch_name_id` varchar(20) NOT NULL , ADD CONSTRAINT `bank_department_subbranch_name_id_7f3fe777_fk_bank_subb` FOREIGN KEY (`subbranch_name_id`) REFERENCES `bank_subbranch`(`name`);
--
-- Create model Contact
--
CREATE TABLE `bank_contact` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(20) NOT NULL, `phone` varchar(11) NOT NULL, `email` varchar(254) NOT NULL, `relation` varchar(20) NOT NULL, `client_id_id` varchar(18) NOT NULL);
--
-- Create model ClientLoan
--
CREATE TABLE `bank_clientloan` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `client_id_id` varchar(18) NOT NULL, `loan_id_id` varchar(20) NOT NULL);
--
-- Add field staff_id to client
--
ALTER TABLE `bank_client` ADD COLUMN `staff_id_id` varchar(18) NULL , ADD CONSTRAINT `bank_client_staff_id_id_82ea35d8_fk_bank_staff_id` FOREIGN KEY (`staff_id_id`) REFERENCES `bank_staff`(`id`);
--
-- Create model AccessAccount
--
CREATE TABLE `bank_accessaccount` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `least_recently_access` datetime(6) NOT NULL, `account_id_id` varchar(20) NOT NULL, `client_id_id` varchar(18) NOT NULL);
--
-- Create constraint PayLoan Primary Key on model payloan
--
ALTER TABLE `bank_payloan` ADD CONSTRAINT `PayLoan Primary Key` UNIQUE (`loan_id_id`, `pay_date`);
--
-- Create constraint Contact Primary key on model contact
--
ALTER TABLE `bank_contact` ADD CONSTRAINT `Contact Primary key` UNIQUE (`client_id_id`, `name`);
--
-- Create constraint ClientLoan Primary Key on model clientloan
--
ALTER TABLE `bank_clientloan` ADD CONSTRAINT `ClientLoan Primary Key` UNIQUE (`loan_id_id`, `client_id_id`);
--
-- Create constraint AccessAccount Primary key on model accessaccount
--
ALTER TABLE `bank_accessaccount` ADD CONSTRAINT `AccessAccount Primary key` UNIQUE (`account_id_id`, `client_id_id`);
ALTER TABLE `bank_checkingaccount` ADD CONSTRAINT `bank_checkingaccount_account_id_id_df0861f5_fk_bank_account_id` FOREIGN KEY (`account_id_id`) REFERENCES `bank_account` (`id`);
ALTER TABLE `bank_savingsaccount` ADD CONSTRAINT `bank_savingsaccount_account_id_id_48a27843_fk_bank_account_id` FOREIGN KEY (`account_id_id`) REFERENCES `bank_account` (`id`);
ALTER TABLE `bank_staff` ADD CONSTRAINT `bank_staff_department_id_id_47331d4d_fk_bank_department_id` FOREIGN KEY (`department_id_id`) REFERENCES `bank_department` (`id`);
ALTER TABLE `bank_payloan` ADD CONSTRAINT `bank_payloan_loan_id_id_90cf71ad_fk_bank_loan_id` FOREIGN KEY (`loan_id_id`) REFERENCES `bank_loan` (`id`);
ALTER TABLE `bank_contact` ADD CONSTRAINT `bank_contact_client_id_id_d108b3a9_fk_bank_client_id` FOREIGN KEY (`client_id_id`) REFERENCES `bank_client` (`id`);
ALTER TABLE `bank_clientloan` ADD CONSTRAINT `bank_clientloan_client_id_id_9d732a84_fk_bank_client_id` FOREIGN KEY (`client_id_id`) REFERENCES `bank_client` (`id`);
ALTER TABLE `bank_clientloan` ADD CONSTRAINT `bank_clientloan_loan_id_id_75e2ace1_fk_bank_loan_id` FOREIGN KEY (`loan_id_id`) REFERENCES `bank_loan` (`id`);
ALTER TABLE `bank_accessaccount` ADD CONSTRAINT `bank_accessaccount_account_id_id_ff9659a2_fk_bank_account_id` FOREIGN KEY (`account_id_id`) REFERENCES `bank_account` (`id`);
ALTER TABLE `bank_accessaccount` ADD CONSTRAINT `bank_accessaccount_client_id_id_81dca4dc_fk_bank_client_id` FOREIGN KEY (`client_id_id`) REFERENCES `bank_client` (`id`);