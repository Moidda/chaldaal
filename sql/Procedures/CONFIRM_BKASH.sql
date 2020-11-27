CREATE OR REPLACE PROCEDURE CONFIRM_BKASH
(
	ONO 	IN 	INT,
	CID 	IN 	INT,
	TID 	IN 	VARCHAR,
	PNO 	IN 	NUMBER
)
IS
BEGIN
	
	INSERT INTO BKASH
	(ORDAR_NO, CUSTOMER_ID, TRANS_ID, PHONE_NO)
	VALUES
	(ONO, CID, TID, PNO);

	COMMIT;

END;
/