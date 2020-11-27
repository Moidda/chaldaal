CREATE OR REPLACE PROCEDURE UPDATE_CUSTOMER_INFO
(
		CID 		IN 	INT,
		CNAME 	IN	VARCHAR,
		MAIL 		IN 	VARCHAR,
		SNO 		IN 	VARCHAR,
		HNO 		IN 	VARCHAR,
		ANO 		IN 	VARCHAR
)
IS


BEGIN

	UPDATE	CUSTOMER
	SET 	
					CUSTOMER_NAME = CNAME,
					EMAIL = MAIL,
					STREET_NO = SNO,
					HOUSE_NO = HNO,
					APT_NO = ANO
	WHERE
					CUSTOMER_ID = CID;
					
	COMMIT;

END;
/