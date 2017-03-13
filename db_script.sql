CREATE TABLE comments
(  id                     INTEGER                PRIMARY KEY
 , surname                TEXT(20)               NOT NULL
 , name                   TEXT(20)               NOT NULL
 , middlename             TEXT(20)               NULL
 , region                 INTEGER(3)             NULL
 , city                   INTEGER(3)             NULL
 , phone                  TEXT(20)               NULL
 , email                  TEXT(20)               NULL
 , comment                TEXT(400)              NOT NULL
 , FOREIGN KEY(region)    REFERENCES regions(id)
 , FOREIGN KEY(city)      REFERENCES cities(id)
);

CREATE TABLE regions
(  id                     INTEGER                PRIMARY KEY
 , region                 TEXT(30)               NOT NULL
);

CREATE TABLE cities
(  id                     INTEGER                PRIMARY KEY    
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

-- Строки для заполнения таблицы

INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Петров',
     'Петр',
     'Геннадьевич',
     '3',
     '9',
     '(928)3609884',
     'wer@fds.ru',
     'Комментарий номер один!!11'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Семенов',
     'Семен',
     'Петрович',
     '3',
     '7',
     '(928)8889849',
     'semenwer@fds.ru',
     'Lorum ipsum dolor.'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Александров',
     'Александр',
     'Степанович',
     '3',
     '8',
     '(924)5609844',
     'se@mail.ru',
     'Lorum ipsum dolor. Lorum ipsum dolor.'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Алексеев',
     'Алексей',
     'Сережаевич',
     '3',
     '9',
     '(933)5211211',
     'alex12@gmail.com',
     'Lorum ipsum dolor. Lorum ipsum dolor.'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Тарасов',
     'Антон',
     'Федорович',
     '3',
     '8',
     '(926)5667789',
     'taras@list.ru',
     'Lorum ipsum dolor. Lorum ipsum dolor.'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Охмат',
     'Артем',
     'Александрович',
     '3',
     '7',
     '(929)4312232',
     'ohmat@list.ru',
     'Lorum ipsum dolor. Lorum ipsum dolor.'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Иванов',
     'Иван',
     'Петрович',
     '2',
     '4',
     '(918)5554433',
     'ivan@fdssdf.com',
     'Второй комментарий.'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Сидоров',
     'Николай',
     'Евгеньевич',
     '1',
     '3',
     '(925)4358496',
     'sid@yahoo.com',
     'Четвёртый комментарий.'
    );
INSERT INTO comments (surname, name, middlename, region,
                      city, phone, email, comment)
    VALUES (
     'Фролов',
     'Вячеслав',
     '',
     '1',
     '2',
     '',
     '',
     'Третий комментарий'
    );