CREATE OR REPLACE FUNCTION GET_PRODUCT_PRICE ( PID IN INT )
RETURN INT IS
	PPU INT;
	PD  INT;
	RET INT;
	CNT INT;
BEGIN

	SELECT PRICE_PER_UNIT			INTO PPU 			FROM PRODUCT 				WHERE PRODUCT_ID = PID;
	SELECT COUNT(*)						INTO CNT 			FROM FLASH_SALE 		WHERE PRODUCT_ID = PID;
	
	IF CNT > 0 THEN
			SELECT PERCENT_DISCOUNT			INTO PD 		FROM FLASH_SALE 		WHERE PRODUCT_ID = PID;
			RET := PPU - FLOOR((PPU*PD) / 100);
	
	ELSE 
			RET := PPU;
	
	END IF;
	
	RETURN RET;

EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN 0;
END;
/



-- SELECT GET_PRODUCT_PRICE(4) FROM CUSTOMER;



