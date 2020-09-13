CREATE SCHEMA MONITORING;

CREATE TABLE MONITORING.ROLE
(
    ID INTEGER GENERATED BY DEFAULT AS IDENTITY,
    NAME VARCHAR,
    DESCRIPTION VARCHAR,
    PRIMARY KEY (ID),
    UNIQUE(NAME)
);

INSERT INTO MONITORING.ROLE(NAME, DESCRIPTION) VALUES ('superuser', 'superuser role');

CREATE TABLE MONITORING.USER
(
    ID INTEGER GENERATED BY DEFAULT AS IDENTITY,
    EMAIL VARCHAR NOT NULL,
    PASSWORD VARCHAR,
    ACTIVE BOOLEAN DEFAULT TRUE,
    CONFIRMED_AT TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (ID),
    UNIQUE (EMAIL),
    CONSTRAINT CONST_EMAIL CHECK (EMAIL ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
);

CREATE TABLE MONITORING.ROLES_USERS
(
    USER_ID INTEGER,
    ROLE_ID INTEGER,
    FOREIGN KEY(USER_ID) REFERENCES MONITORING.USER(ID),
    FOREIGN KEY(ROLE_ID) REFERENCES MONITORING.ROLE(ID)
);

INSERT INTO MONITORING.USER(EMAIL, PASSWORD, ACTIVE, CONFIRMED_AT) VALUES
    ('admin@monitoring.com', 'admin', TRUE, current_timestamp);

CREATE TABLE MONITORING.STUDENT
(
    ID INTEGER GENERATED BY DEFAULT AS IDENTITY,
    FIRST_NAME VARCHAR,
    LAST_NAME VARCHAR,
    EMAIL VARCHAR NOT NULL,
    IP VARCHAR,
    ACTIVE BOOLEAN DEFAULT TRUE,
    PRIMARY KEY(ID),
    UNIQUE(EMAIL),
    CONSTRAINT CONST_EMAIL CHECK (EMAIL ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
);

CREATE TABLE MONITORING.ALERT
(
    ID INTEGER GENERATED BY DEFAULT AS IDENTITY,
    TYPE_ALERT VARCHAR,
    PRIMARY KEY(ID),
    UNIQUE(TYPE_ALERT)
);

INSERT INTO MONITORING.ALERT(TYPE_ALERT) VALUES ('');
INSERT INTO MONITORING.ALERT(TYPE_ALERT) VALUES ('PHONE');
INSERT INTO MONITORING.ALERT(TYPE_ALERT) VALUES ('NO PERSON');
INSERT INTO MONITORING.ALERT(TYPE_ALERT) VALUES ('SEVERAL PEOPLE');
INSERT INTO MONITORING.ALERT(TYPE_ALERT) VALUES ('UNKNOWN PERSON');

CREATE TABLE MONITORING.EVENT
(
    ID INTEGER GENERATED BY DEFAULT AS IDENTITY,
    STUDENT_ID INTEGER NOT NULL CHECK(STUDENT_ID IS NOT NULL),
    IMG_PATH VARCHAR NOT NULL CHECK(IMG_PATH <> ''),
    IMG_DATETIME TIMESTAMP DEFAULT current_timestamp,
    IMG_METADATA JSONB,
    ALERT_ID INTEGER DEFAULT NULL,
    FOREIGN KEY (STUDENT_ID) REFERENCES MONITORING.STUDENT(ID)
);

CREATE USER MONITORING_ADMIN WITH PASSWORD 'password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA MONITORING TO MONITORING_ADMIN;
GRANT USAGE ON SCHEMA MONITORING TO MONITORING_ADMIN;

--DROP SCHEMA IF EXISTS MONITORING CASCADE;
--DROP ROLE MONITORING_ADMIN;