CREATE OR REPLACE FUNCTION GET_CREDIT_CARD
(
	MY_ID 	IN 	INT,
	ATT		IN	VARCHAR
) 
RETURN VARCHAR IS

	RET 	VARCHAR(100);

BEGIN

	
	IF 		ATT = 'USERNAME' 	THEN
	
		SELECT USERNAME INTO RET FROM CUSTOMER_PAYMENT_INFO WHERE CUSTOMER_ID = MY_ID;
	
	ELSIF 	ATT = 'BANK' 		THEN
	
		SELECT BANK INTO RET FROM CUSTOMER_PAYMENT_INFO WHERE CUSTOMER_ID = MY_ID;
	
	ELSIF 	ATT = 'CARD_TYPE'	THEN
		
		SELECT CARD_TYPE INTO RET FROM CUSTOMER_PAYMENT_INFO WHERE CUSTOMER_ID = MY_ID;
	
	ELSIF	ATT = 'CARD_NO'		THEN
		
		SELECT CARD_NO INTO RET FROM CUSTOMER_PAYMENT_INFO WHERE CUSTOMER_ID = MY_ID;
	
	END IF;
	
	
	RETURN RET;

EXCEPTION

	WHEN NO_DATA_FOUND THEN
		RETURN NULL;
	WHEN OTHERS THEN
		RETURN NULL;

END;
/



