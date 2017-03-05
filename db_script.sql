CREATE TABLE comments
(  id                     INTEGER(3)             PRIMARY KEY
 , surname                TEXT(20)               NOT NULL
 , name                   TEXT(20)               NOT NULL
 , middlename             TEXT(20)               NULL
 , region                 INTEGER(3)             NULL
 , city                   INTEGER(3)             NULL
 , phone                  TEXT(11)               NULL
 , email                  TEXT(20)               NULL
 , comment                TEXT(400)              NOT NULL
 , FOREIGN KEY(region)    REFERENCES regions(id)
 , FOREIGN KEY(city)      REFERENCES cities(id)
);

CREATE TABLE regions
(  id                     INTEGER(3)             PRIMARY KEY
 , region                 TEXT(30)               NOT NULL
);

CREATE TABLE cities
(  id                     INTEGER(3)             PRIMARY KEY    
 , city                   TEXT(30)               NOT NULL
 , region_id              INTEGER(3)             NOT NULL
 , FOREIGN KEY(region_id) REFERENCES regions(id)
);

INSERT INTO regions VALUES (1, 'Краснодарский край');
INSERT INTO regions VALUES (2, 'Ростовская область');
INSERT INTO regions VALUES (3, 'Ставропольский край');

INSERT INTO cities VALUES (1, 'Краснодар', 1);
INSERT INTO cities VALUES (2, 'Кропоткин', 1);
INSERT INTO cities VALUES (3, 'Славянск', 1);
INSERT INTO cities VALUES (4, 'Ростов', 2);
INSERT INTO cities VALUES (5, 'Шахты', 2);
INSERT INTO cities VALUES (6, 'Батайск', 2);
INSERT INTO cities VALUES (7, 'Ставрополь', 3);
INSERT INTO cities VALUES (8, 'Пятигорск', 3);
INSERT INTO cities VALUES (9, 'Кисловодск', 3);