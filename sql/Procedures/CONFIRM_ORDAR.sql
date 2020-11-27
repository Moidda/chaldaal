DROP PROCEDURE CONFIRM_CHECKOUT;

CREATE OR REPLACE PROCEDURE CONFIRM_ORDAR
(
	ONO 	IN 	INT,
	CID 	IN 	INT
)
IS
BEGIN
	
	INSERT INTO ORDAR
	(ORDAR_NO, ORDAR_TIME, CUSTOMER_ID)
	VALUES
	(ONO, LOCALTIMESTAMP(0), CID);

	COMMIT;

END;
/


BEGIN
	CONFIRM_ORDAR(16, 1);
END;
/
