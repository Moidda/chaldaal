CREATE OR REPLACE PROCEDURE CHECKING_FLASH_SALE(
		PID      IN   INT,
		PERDIS   IN   INT
)
IS 
		CNT  INT;
		SID  INT;
		
BEGIN
			SELECT COUNT(*) INTO CNT FROM FLASH_SALE WHERE PRODUCT_ID = PID;
			
			IF CNT = 0 THEN 
			SELECT NVL(MAX(SALE_ID),0) INTO SID FROM FLASH_SALE;
				INSERT INTO FLASH_SALE(SALE_ID,PRODUCT_ID,PERCENT_DISCOUNT,START_DATE,AVAILABILITY)
				VALUES
				(SID + 1,PID,PERDIS,SYSDATE,'Y');
			
			ELSIF CNT = 1 THEN
				UPDATE FLASH_SALE
				SET
					PERCENT_DISCOUNT = PERDIS,
					START_DATE = SYSDATE
				WHERE PRODUCT_ID = PID;	
			END IF;
		
		COMMIT;
END;
/