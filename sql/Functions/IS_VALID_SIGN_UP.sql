CREATE OR REPLACE FUNCTION IS_VALID_SIGN_UP	
(
	NAME 				IN 	VARCHAR, 
	SNO 				IN 	VARCHAR, 
	HNO 				IN 	VARCHAR, 
	ANO 				IN	VARCHAR, 
	MAIL 				IN 	VARCHAR,
	PASSWORD1 	IN 	VARCHAR,
	PASSWORD2 	IN 	VARCHAR
)
RETURN VARCHAR IS
	RET VARCHAR(100);
BEGIN
	
	IF NAME IS NULL THEN
		RET := 'Please provide your full name';
	ELSIF SNO IS NULL THEN
		RET := 'Please provide a street no';
	ELSIF HNO IS NULL THEN
		RET := 'Please provide a house no';
	ELSIF ANO IS NULL THEN
		RET := 'Please provide an apt no. If you can not provide an apt no, type in default';
	ELSIF MAIL IS NULL THEN
		RET := 'Please provide an email';
	ELSIF PASSWORD1 IS NULL THEN
		RET := 'Password cannot be empty';
	ELSIF PASSWORD1 <> PASSWORD2 THEN
		RET := 'Could not confirm password';
	ELSE
		RET := 'VALID';
	END IF;
		
	FOR R IN (SELECT EMAIL FROM CUSTOMER)
	LOOP
		IF R.EMAIL = MAIL THEN
			RET := 'Email already in use';
		END IF;
	END LOOP;
	
	RETURN RET;
END;
/