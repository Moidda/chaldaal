CREATE OR REPLACE FUNCTION GET_CUSTOMER
(
		CID 	IN 		INT,
		T 		IN 		VARCHAR
)
RETURN VARCHAR 
IS

		RET 	VARCHAR(100);
		TEMP 	INT;

BEGIN

		IF T = 'CUSTOMER_NAME' THEN
		
				SELECT CUSTOMER_NAME INTO RET FROM CUSTOMER WHERE CUSTOMER_ID = CID;
		
		ELSIF T = 'EMAIL' THEN
		
				SELECT EMAIL INTO RET FROM CUSTOMER WHERE CUSTOMER_ID = CID;
		
		ELSIF T = 'STREET_NO' THEN
		
				SELECT STREET_NO INTO RET FROM CUSTOMER WHERE CUSTOMER_ID = CID;
		
		ELSIF T = 'HOUSE_NO' THEN
		
				SELECT HOUSE_NO INTO RET FROM CUSTOMER WHERE CUSTOMER_ID = CID;
		
		ELSIF T = 'APT_NO' THEN
		
				SELECT APT_NO INTO RET FROM CUSTOMER WHERE CUSTOMER_ID = CID;
				
		ELSIF T = 'CUSTOMER_CREDIT' THEN
		
				SELECT CUSTOMER_CREDIT INTO TEMP FROM CUSTOMER WHERE CUSTOMER_ID = CID;
				RET := CAST(TEMP AS VARCHAR);
		
		ELSIF T = 'PHONE_NO' THEN
		
				SELECT PHONE_NUMBER INTO RET FROM CUSTOMER_PHONE WHERE CUSTOMER_ID = CID;
		
		END IF;

		RETURN RET;

EXCEPTION

		WHEN NO_DATA_FOUND THEN
				RETURN NULL;
		WHEN OTHERS THEN
				RETURN NULL;

END;
/