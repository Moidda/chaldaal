CREATE OR REPLACE PROCEDURE INSERT_PRODUCTS_IN_ORDAR
(
	ONO 	IN 	INT,
	PID 	IN 	INT,
	CNT 	IN 	INT
)
IS
BEGIN

	INSERT INTO PRODUCTS_IN_ORDER
	(ORDAR_NO, PRODUCT_ID, QUANTITY)
	VALUES
	(ONO, PID, CNT);

END;
/