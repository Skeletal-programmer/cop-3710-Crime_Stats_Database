INSERT INTO Agency (Agency_ID, Agency_Name, Agency_Type)
SELECT 
    LEVEL + 10,
    'Agency_' || LEVEL,
    CASE 
        WHEN MOD(LEVEL,3)=0 THEN 'Forensic'
        WHEN MOD(LEVEL,3)=1 THEN 'Investigative'
        ELSE 'State'
    END
FROM dual
CONNECT BY LEVEL <= 100;

INSERT INTO Geographic (GEO_ID, City, State, Agency_ID)
SELECT 
    LPAD(LEVEL+10, 2, '0'),
    'City_' || LEVEL,
    CASE 
        WHEN MOD(LEVEL,3)=0 THEN 'FL'
        WHEN MOD(LEVEL,3)=1 THEN 'NY'
        ELSE 'CA'
    END,
    MOD(LEVEL,3) + 1
FROM dual
CONNECT BY LEVEL <= 100;

INSERT INTO Demographic 
(Victim_ID, Age, Gender, Ethnicity, Offender_ID, Crim_Rec, Agency_ID)
SELECT
    'V' || (LEVEL+10),
    TRUNC(DBMS_RANDOM.VALUE(18,80)),
    CASE WHEN MOD(LEVEL,2)=0 THEN 'M' ELSE 'F' END,
    'Ethnicity_' || LEVEL,
    LEVEL,
    CASE 
        WHEN MOD(LEVEL,3)=0 THEN 'AA'
        WHEN MOD(LEVEL,3)=1 THEN 'B&E'
        ELSE 'TE'
    END,
    MOD(LEVEL,3) + 1
FROM dual
CONNECT BY LEVEL <= 100;

INSERT INTO Victimology (Victim_ID, Offender_ID, Crim_Rec)
SELECT
    'V' || (LEVEL+10),
    LEVEL,
    CASE 
        WHEN MOD(LEVEL,3)=0 THEN 'AA'
        WHEN MOD(LEVEL,3)=1 THEN 'B&E'
        ELSE 'TE'
    END
FROM dual
CONNECT BY LEVEL <= 100;

INSERT INTO Modus_Operandi
(Crim_Rec_ID, Crim_Rec, Weapon, Connections, Tactics, GEO_ID, Victim_ID, Offender_ID)
SELECT
    'R' || (LEVEL+10),
    CASE 
        WHEN MOD(LEVEL,3)=0 THEN 'AA'
        WHEN MOD(LEVEL,3)=1 THEN 'B&E'
        ELSE 'TE'
    END,
    CASE 
        WHEN MOD(LEVEL,3)=0 THEN 'Gun'
        WHEN MOD(LEVEL,3)=1 THEN 'Knife'
        ELSE 'Poison'
    END,
    'Connection_' || LEVEL,
    'Tactic_' || LEVEL,
    LPAD(MOD(LEVEL,3)+1, 2, '0'),
    'V' || (LEVEL+10),
    LEVEL
FROM dual
CONNECT BY LEVEL <= 100;

SELECT DBMS_RANDOM.STRING('U',10) FROM dual;
SELECT DBMS_RANDOM.VALUE(1,100) FROM dual;
