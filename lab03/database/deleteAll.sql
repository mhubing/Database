delimiter //
DROP PROCEDURE IF EXISTS delete_all;
CREATE PROCEDURE delete_all(OUT state int)
BEGIN
    DECLARE s INT DEFAULT 0;
    START TRANSACTION;
    SET FOREIGN_KEY_CHECKS = 0;

    Drop Table IF EXISTS Subbranch;
    Drop Table IF EXISTS Client;
    Drop Table IF EXISTS Contact;
    Drop Table IF EXISTS Staff;
    Drop Table IF EXISTS Account;
    Drop Table IF EXISTS SavingsAccount;
    Drop Table IF EXISTS CheckingAccount;
    Drop Table IF EXISTS AccessAccount;
    Drop Table IF EXISTS Department;
    Drop Table IF EXISTS Loan;
    Drop Table IF EXISTS PayLoan;
    Drop Table IF EXISTS ClientLoan;

    SET FOREIGN_key_checks = 1;
    IF s=0 THEN
        SET state=0;
        COMMIT;
    ELSE
        SET state=1;
        ROLLBACK;
    END IF;
END //
delimiter ;