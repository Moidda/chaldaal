CREATE OR REPLACE PROCEDURE CONFIRM_ORDER_INFO
(
		ONO 		IN 		INT,
		NAME 		IN 		VARCHAR,
		SNO 		IN 		VARCHAR,
		HNO 		IN 		VARCHAR,
		ANO 		IN 		VARCHAR,
		CRED 		IN 		INT,
		DISC 		IN 		INT
)
IS


BEGIN

		INSERT INTO ORDER_INFO
		(ORDAR_NO, CUSTOMER_NAME, STREET_NO, HOUSE_NO, APT_NO, CREDITS_REDEEMED, CREDITS_DISCOUNT)
		VALUES
		(ONO, NAME, SNO, HNO, ANO, CRED, DISC);

END;
/