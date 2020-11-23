CREATE OR REPLACE PROCEDURE CREATE_CUSTOMER
(
	NAME	IN 	VARCHAR,
	SNO 	IN 	VARCHAR,
	HNO 	IN 	VARCHAR,
	ANO 	IN 	VARCHAR,
	MAIL 	IN 	VARCHAR,
	P1 		IN 	VARCHAR,
	P2 		IN 	VARCHAR
)
IS 
	MAX_ID 	INT;
BEGIN
	
	SELECT MAX(CUSTOMER_ID) INTO MAX_ID FROM CUSTOMER;
	
	IF IS_VALID_SIGN_UP(NAME, SNO, HNO, ANO, MAIL, P1, P2) = 'VALID' THEN
		INSERT INTO CUSTOMER
		("CUSTOMER_ID", "CUSTOMER_NAME", "STREET_NO", "HOUSE_NO", "APT_NO", "EMAIL", "CUSTOMER_CREDIT", "PASSWORD")
		VALUES
		(MAX_ID + 1, NAME, SNO, HNO, ANO, MAIL, 0, P1);
		COMMIT;
	END IF;
	
END;
/