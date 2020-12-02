CREATE OR REPLACE TRIGGER CUSTOMER_POINT
BEFORE INSERT
ON PAYMENT
FOR EACH ROW
DECLARE

BEGIN
	UPDATE CUSTOMER C SET C.CUSTOMER_CREDIT = C.CUSTOMER_CREDIT + ROUND((:NEW.TOTAL_COST)/100, 0)
	WHERE C.CUSTOMER_ID = :NEW.CUSTOMER_ID;
END;
/
