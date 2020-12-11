CREATE TABLE CUSTOMER
(
    CUSTOMER_ID     INT         	NOT NULL,
    CUSTOMER_NAME   VARCHAR(20) 	NOT NULL,
    STREET_NO       VARCHAR(20) 	NOT NULL, 
    HOUSE_NO        VARCHAR(20) 	NOT NULL,
    APT_NO          VARCHAR(20) 	NOT NULL,
    EMAIL           VARCHAR(20),
    CUSTOMER_CREDIT INT,
    PASSWORD        VARCHAR(20) 	NOT NULL,

    CONSTRAINT CUSTOMER_PK PRIMARY KEY (CUSTOMER_ID)
);

DROP TABLE CUSTOMER_PHONE;
CREATE TABLE CUSTOMER_PHONE
(
    CUSTOMER_ID     INT						NOT NULL,
    PHONE_NUMBER    VARCHAR(20)		NULL,
	
	CONSTRAINT CUSTOMER_PHONE_PK PRIMARY KEY (CUSTOMER_ID),
	CONSTRAINT CUSTOMER_PHONE_FK FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID) ON DELETE CASCADE
);

DROP TABLE ORDAR;
CREATE TABLE ORDAR
(
    ORDAR_NO    INT          NOT NULL,
    ORDAR_DATE  DATE         NOT NULL,
    ORDAR_TIME  TIMESTAMP    NOT NULL,
		CUSTOMER_ID	INT					 NOT NULL, 					

    CONSTRAINT ORDAR_PK PRIMARY KEY(ORDAR_NO),
		CONSTRAINT ORDAR_FK FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID) ON DELETE CASCADE
);
ALTER TABLE ORDAR
DROP COLUMN ORDAR_DATE;


-- CREATE TABLE MAKES
-- (
--     ORDAR_NO    INT     NOT NULL,
--     CUSTOMER_ID INT     NOT NULL,
-- 
--     CONSTRAINT MAKES_PK PRIMARY KEY (ORDAR_NO)
-- );
DROP TABLE MAKES;


-- PRODUCT WAS RE CREATED. CHECK PRODUCT_TABLE_RECREATE.SQL 
CREATE TABLE PRODUCT
(
    PRODUCT_ID  		INT     		NOT NULL,
    PRODUCT_NAME 		VARCHAR(20)    	NOT NULL,
    UNIT        		VARCHAR(5)  	NOT NULL,
    UNITS_IN_STOCK  	NUMBER(10, 2),
    PRICE_PER_UNIT  	NUMBER(20, 2), 
    CATEGORY    		VARCHAR(20),
    RATING_BY_CUSTOMER  NUMBER(2, 2),

    CONSTRAINT PRODUCT_PK PRIMARY KEY (PRODUCT_ID)
);


DROP TABLE CONTAINS;
CREATE TABLE PRODUCTS_IN_ORDER
(
    ORDAR_NO    INT             NOT NULL,
    PRODUCT_ID  INT             NOT NULL,
    QUANTITY    NUMBER(10, 2)   NOT NULL,

    CONSTRAINT PO_FK1 FOREIGN KEY(ORDAR_NO) 		REFERENCES ORDAR(ORDAR_NO) 				ON DELETE CASCADE,
		CONSTRAINT PO_FK2 FOREIGN KEY(PRODUCT_ID) 	REFERENCES PRODUCT(PRODUCT_ID) 		ON DELETE CASCADE
);


CREATE TABLE OFFER
(
    PRODUCT_ID          INT     NOT NULL,
    START_DATE          DATE,
    END_DATE            DATE,
    QUANTITY            NUMBER(10, 2),
    PERCENT_DISCOUNT    NUMBER(2),

    CONSTRAINT OFFER_PK PRIMARY KEY (PRODUCT_ID),
    CONSTRAINT OFFER_FK FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID)
);

DROP TABLE OFFER;

DROP TABLE FLASH_SALE;

CREATE TABLE FLASH_SALE
(
		SALE_ID             INT     NOT NULL,
    PRODUCT_ID          INT     NOT NULL,
		PERCENT_DISCOUNT    INT     NOT NULL,
		START_DATE          DATE,
		END_DATE            DATE,
		AVAILABILITY        CHAR(1) NOT NULL,
		
    CONSTRAINT FLASH_SALE_PK PRIMARY KEY (SALE_ID),
    CONSTRAINT FLASH_SALE_FK FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID)
);




CREATE TABLE FREE
(
    MAIN_PRODUCT_ID         INT     NOT NULL,
    FREE_PRODUCT_ID         INT     NOT NULL,
    START_DATE              DATE,
    END_DATE                DATE,
    MAIN_PRODUCT_QUANTITY   NUMBER(10, 2),
    FREE_PRODUCT_QUANTITY   NUMBER(10, 2)
);
DROP TABLE FREE;


CREATE TABLE RATES
(
    CUSTOMER_ID     INT     NOT NULL,
    PRODUCT_ID      INT     NOT NULL,
    RATING_NO       NUMBER(2, 2), 

    CONSTRAINT RATES_PK PRIMARY KEY (CUSTOMER_ID, PRODUCT_ID)
);


DROP TABLE PAYMENT;
CREATE TABLE PAYMENT
(
    ORDAR_NO      	INT             NOT NULL,
		CUSTOMER_ID 		INT							NOT NULL,
    PAYMENT_DATE    DATE            NOT NULL,
    TOTAL_COST      NUMBER(10, 2)   NOT NULL,
    DUE             NUMBER(10, 2)   NOT NULL,

    CONSTRAINT PAYMENT_FK1 FOREIGN KEY(ORDAR_NO) 		REFERENCES ORDAR(ORDAR_NO) 				ON DELETE CASCADE,
		CONSTRAINT PAYMENT_FK2 FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID) 	ON DELETE CASCADE
);


DROP TABLE BKASH;
CREATE TABLE BKASH
(
    ORDAR_NO      	INT             NULL,
		CUSTOMER_ID 		INT 						NOT NULL,
    TRANS_ID        VARCHAR(20)     NULL,
    PHONE_NO        NUMBER(11)      NOT NULL,

    CONSTRAINT BKASH_FK1 FOREIGN KEY(ORDAR_NO) 		REFERENCES ORDAR(ORDAR_NO) 				ON DELETE CASCADE,
		CONSTRAINT BKASH_FK2 FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID) 	ON DELETE CASCADE
);
ALTER TABLE BKASH
MODIFY (PHONE_NO VARCHAR(100));


DROP TABLE CREDIT_CARD;
CREATE TABLE CREDIT_CARD
(
    ORDAR_NO      	INT             	NULL,
    CUSTOMER_ID 	INT	 				NOT NULL,
	USERNAME        VARCHAR(100)     	NOT NULL,
    BANK            VARCHAR(100)     	NOT NULL,
    CARD_TYPE       VARCHAR(100)     	NOT NULL,
    CARD_NO         VARCHAR(100)     	NOT NULL,

    CONSTRAINT CARD_FK1 FOREIGN KEY(ORDAR_NO) 		REFERENCES ORDAR(ORDAR_NO) 				ON DELETE CASCADE,
	CONSTRAINT CARD_FK2 FOREIGN KEY(CUSTOMER_ID) 	REFERENCES CUSTOMER(CUSTOMER_ID) 		ON DELETE CASCADE
);


CREATE TABLE CASH_ON_DELIVERY
(
    PAYMENT_ID      INT             NOT NULL,
    PAID            NUMBER(10, 2)   NOT NULL,
    CHANGE          NUMBER(10, 2)   NOT NULL,

    CONSTRAINT CASH_ON_DELIVERY_PK PRIMARY KEY (PAYMENT_ID)
);

-- CREATE TABLE NEEDS
-- (
--     ORDAR_NO        INT     NOT NULL,    
--     PAYMENT_ID      INT     NOT NULL,
--     CUSTOMER_POINTS INT,
-- 
--     CONSTRAINT NEEDS_PK PRIMARY KEY (ORDAR_NO)
-- );
DROP TABLE NEEDS;

CREATE TABLE AGENT
(
    AGENT_ID        INT             NOT NULL,
    AGENT_NAME      VARCHAR(20)     NOT NULL,
    AGENT_PHONE_NO  NUMBER(11)      NOT NULL,
    DELIVERY_CHARGE NUMBER(3, 2)    NOT NULL,

    CONSTRAINT AGENT_PK PRIMARY KEY (AGENT_ID)
);

CREATE TABLE RECEIVES
(
    ORDAR_NO        INT     NOT NULL,
    AGENT_ID        INT     NOT NULL,

    CONSTRAINT RECEIVES_PK PRIMARY KEY (ORDAR_NO)
);


CREATE TABLE CUSTOMER_PAYMENT_INFO
(
	CUSTOMER_ID		INT	 				NOT NULL,
	USERNAME		VARCHAR(100)     	NULL,
	BANK            VARCHAR(100)     	NULL,
	CARD_TYPE       VARCHAR(100)     	NULL,
	CARD_NO         VARCHAR(100)     	NULL,
	BKASH_PHONE_NO	NUMBER(11)	 		NULL,

	CONSTRAINT 		CUSTOMER_PAYMENT_FK		FOREIGN KEY(CUSTOMER_ID)	REFERENCES	CUSTOMER(CUSTOMER_ID)	ON DELETE CASCADE,
	CONSTRAINT 		CUSTOMER_PAYMENT_UNQ	UNIQUE(CUSTOMER_ID)
);
DELETE FROM CUSTOMER_PAYMENT_INFO WHERE CUSTOMER_ID = 2;
ALTER TABLE CUSTOMER_PAYMENT_INFO
MODIFY (BKASH_PHONE_NO VARCHAR(100));


CREATE TABLE PRODUCT_RATING
(
	PRODUCT_ID 			INT 	NOT NULL,
	TOTAL_RATING		INT 	NULL,
	TOTAL_CUSTOMER 	INT 	NULL,
	
	CONSTRAINT 		PRODUCT_RATING_FK 		FOREIGN KEY(PRODUCT_ID) 		REFERENCES 		PRODUCT(PRODUCT_ID) 	ON DELETE CASCADE,
	CONSTRAINT 		PRODUCT_RATING_UNQ 		UNIQUE(PRODUCT_ID)
);


DROP TABLE ORDER_INFO;
CREATE TABLE ORDER_INFO
(
	ORDAR_NO    			INT						NOT NULL,
	CUSTOMER_NAME 		VARCHAR(50) 	NOT NULL,
	
	STREET_NO 				VARCHAR(50) 	NOT NULL,
	HOUSE_NO 					VARCHAR(50) 	NOT NULL,
	APT_NO 						VARCHAR(50) 	NOT NULL,
	CREDITS_REDEEMED 	INT 					NULL,
	CREDITS_DISCOUNT 	INT 					NULL,
	
	CONSTRAINT 		ORDAR_INFO_FK 		FOREIGN KEY(ORDAR_NO) 		REFERENCES 		ORDAR(ORDAR_NO) 	ON DELETE CASCADE,
	CONSTRAINT 		ORDAR_INFO_UNQ 		UNIQUE(ORDAR_NO)
);

CREATE TABLE BUNDLE_OFFER
(
	BUNDLE_ID    INT 					NOT NULL,
	BUNDLE_NAME  VARCHAR(50)	NOT NULL,
	COST         INT          NOT NULL,
	
	CONSTRAINT BUNDLE_OFFER_PK PRIMARY KEY(BUNDLE_ID)
);

DROP TABLE PRODUCTS_IN_BUNDLE_OFFER;
CREATE TABLE PRODUCTS_IN_BUNDLE_OFFER
(
	BUNDLE_ID 		INT 		NOT NULL,
	PRODUCT_ID		INT     NOT NULL,
	QUANTITY      INT     NOT NULL,
	
	CONSTRAINT PRODUCTS_IN_BUNDLE_OFFER_FK1 FOREIGN KEY(BUNDLE_ID) 		REFERENCES BUNDLE_OFFER(BUNDLE_ID) ON DELETE CASCADE,
	CONSTRAINT PRODUCTS_IN_BUNDLE_OFFER_FK2 FOREIGN KEY(PRODUCT_ID) 	REFERENCES PRODUCT(PRODUCT_ID) 		 ON DELETE CASCADE
);



