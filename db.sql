
-- Table director
CREATE TABLE director (
  idDirector SERIAL PRIMARY KEY,
  DirectorsName VARCHAR(45) NOT NULL
);

-- Table genes
CREATE TABLE genes (
  idGenes SERIAL PRIMARY KEY,
  GenerName VARCHAR(45) NOT NULL
);

-- Table films
CREATE TABLE films (
  idFilms SERIAL PRIMARY KEY,
  FilmName VARCHAR(45) NOT NULL,
  YearOfIssue DATE NOT NULL,
  idDirector INT NOT NULL,
  idGener INT NOT NULL,
  CONSTRAINT dir_fk FOREIGN KEY (idDirector) REFERENCES director(idDirector),
  CONSTRAINT gener_fk FOREIGN KEY (idGener) REFERENCES genes(idGenes)
);

-- Table halltype
CREATE TABLE halltype (
  idHallType SERIAL PRIMARY KEY,
  HallType VARCHAR(45) NOT NULL
);

-- Table halls
CREATE TABLE halls (
  idHalls SERIAL PRIMARY KEY,
  HallName VARCHAR(45) NOT NULL,
  Seat INT NOT NULL,
  idHallType INT NOT NULL,
  CONSTRAINT ht_fk FOREIGN KEY (idHallType) REFERENCES halltype(idHallType)
);

-- Table sessions
CREATE TABLE sessions (
  idSessions SERIAL PRIMARY KEY,
  Duration INT NOT NULL,
  idFilm INT NOT NULL,
  idHall INT NOT NULL,
  DateAndTimeStart TIMESTAMP NULL DEFAULT NULL,
  CONSTRAINT film_fk FOREIGN KEY (idFilm) REFERENCES films(idFilms),
  CONSTRAINT hall_fk FOREIGN KEY (idHall) REFERENCES halls(idHalls)
);

-- Table users
CREATE TABLE users (
  idUsers SERIAL PRIMARY KEY,
  Name VARCHAR(45) NOT NULL,
  Surname VARCHAR(45) NOT NULL,
  Email VARCHAR(45) NOT NULL,
  Phone VARCHAR(45) NOT NULL
);


-- Table booking
CREATE TABLE booking (
  idBooking SERIAL PRIMARY KEY,
  idUser INT NOT NULL,
  idSession INT NOT NULL,
  NumOfTic INT NOT NULL,
  AmountPaid NUMERIC(10,2) NOT NULL,
  BookingStatus SMALLINT NOT NULL DEFAULT 0,
  DateBooking TIMESTAMP NOT NULL,
  CONSTRAINT user_fk FOREIGN KEY (idUser) REFERENCES users(idUsers),
  CONSTRAINT session_fk FOREIGN KEY (idSession) REFERENCES sessions(idSessions)
);

-- Table hallcapacities
CREATE TABLE hallcapacities (
  idHall INT PRIMARY KEY,
  idHallType INT NOT NULL,
  Capacity VARCHAR(45) NOT NULL,
  CONSTRAINT hht_fk FOREIGN KEY (idHallType) REFERENCES halltype(idHallType)
);

-- Table rating
CREATE TABLE rating (
  idRating SERIAL PRIMARY KEY,
  idFilm INT NULL DEFAULT NULL,
  Rating VARCHAR(45) NULL DEFAULT NULL,
  CONSTRAINT film_rating_fk FOREIGN KEY (idFilm) REFERENCES films(idFilms)
);


CREATE TABLE TicketPrices (
  TicketPriceID SERIAL PRIMARY KEY,
  price DECIMAL
);

-- Создание таблицы tickets с ссылкой на TicketPrices
CREATE TABLE tickets (
  idTickets SERIAL PRIMARY KEY,
  idUser INT NOT NULL,
  idSession INT NOT NULL,
  TicketPriceID INT NOT NULL,
  CONSTRAINT user_tickets_fk FOREIGN KEY (idUser) REFERENCES users(idUsers),
  CONSTRAINT session_tickets_fk FOREIGN KEY (idSession) REFERENCES sessions(idSessions),
  CONSTRAINT ticket_price_fk FOREIGN KEY (TicketPriceID) REFERENCES TicketPrices(TicketPriceID)
);

CREATE TABLE film_images (
  id SERIAL PRIMARY KEY,
  film_id INT NOT NULL,
  image_url VARCHAR(255) NOT NULL,
  FOREIGN KEY (film_id) REFERENCES films(idFilms)
);


CREATE TABLE film_descriptions (
  id SERIAL PRIMARY KEY,
  film_id INT NOT NULL,
  description TEXT NOT NULL,
  FOREIGN KEY (film_id) REFERENCES films(idFilms)
);


INSERT INTO director (DirectorsName) VALUES ('Ашимбеков Нурдаулет'),('Джордж ЛукДжеймс Кэмеронас'),('Джордж Лукас'),('Рон Ховард'),('Роман Полански'),('Крис Коламбус');

INSERT INTO genes (genername) VALUES ('Ужасы'),('Драма'),('Фантастика'),('Биография'),('Военный'),('Фэнтези');

INSERT INTO halltype (halltype) VALUES ('2D'),('3D'),('IMax');

INSERT INTO hallcapacities VALUES (1,1,'110'),(2,2,'110'),(3,3,'90'),(4,1,'90'),(5,2,'90'),(6,1,'60');

INSERT INTO halls (hallname, seat, idhalltype) VALUES ('1',11,1),('2',11,2),('3',9,3),('4',9,1),('5',9,2),('6',6,1);

INSERT INTO films (FilmName, YearOfIssue, idDirector, idGener) VALUES ('Астрал','2010-01-30',1,1),('Титаник','1997-12-19',2,2),('Звездные Войны','1977-05-25',3,3),('Игра в имитацию','2001-12-25',4,4),('Пианист','2002-09-24',5,5),('Гарри Поттер','2001-11-04',6,6);

INSERT INTO users (Name, Surname,Email, Phone) VALUES ('Дарья','Медведева','ds@gmail.com','87777'),('Ильяс','Мадьяров','mad@gmail.com','87764'),('Альсина','Мекебаева','mek@gmail.com','87012'),('Нурбол','Сагентаев','sgnt@gmail.com','87075');


INSERT INTO film_images (film_id, image_url)
VALUES 
  (1, 'https://upload.wikimedia.org/wikipedia/ru/thumb/2/22/Insidious_The_Red_Door.jpg/800px-Insidious_The_Red_Door.jpg'),
  (2, 'https://upload.wikimedia.org/wikipedia/ru/1/19/Titanic_%28Official_Film_Poster%29.png'),
  (3, 'https://upload.wikimedia.org/wikipedia/ru/e/eb/Star_Wars_%E2%80%94_The_Rise_of_Skywalker_%28poster%29.jpg'),
  (4, 'https://a.d-cd.net/HvmbDGLOb_NQP0c4ip1l0tVW7VU-960.jpg'),
  (5, 'https://thumbs.dfs.ivi.ru/storage2/contents/8/2/14fab3b83c5b1c2a1cf0f42ce9f95e.jpg'),
  (6, 'https://upload.wikimedia.org/wikipedia/ru/b/b4/Harry_Potter_and_the_Philosopher%27s_Stone_%E2%80%94_movie.jpg');


INSERT INTO film_descriptions (film_id, description)
VALUES 
  (1, '"Астрал" - это американский хоррор-триллер режиссера Джеймса Вана, вышедший в 2010 году. Фильм рассказывает историю семьи Ламберт, которая переезжает в новый дом. После неожиданной смерти сына Дэла, странные и пугающие события начинают происходить в доме. Отец семейства, Джош, начинает видеть ужасающие видения и сталкивается с присутствием зловещих существ. Когда явления становятся все более интенсивными, семье приходится обратиться за помощью к экстрасенсу и духовному исследователю, чтобы понять, что происходит в их доме. Фильм оказывается захватывающим путешествием в мир астральных путешествий и сверхъестественных сил, которые угрожают семье Ламберт.'),
  (2, 'В основе сюжета фильма «Титаник» (Titanic) история, произошедшая   с британским судном. «Титаник» был построен в 1912 году, и на тот момент считался крупнейшим пассажирским лайнером в мире. Во время своего первого рейса он столкнулся с айсбергом и затонул. На борту корабля находилось 2208 человек, выжить удалось лишь 706 человекам. Катастрофа «Титаника» стала легендарной, поэтому неудивительно, что к этой истории неоднократно обращались различные режиссеры, среди которых Кэмерон не был первым, но, безусловно, стал самым удачливым, потому что именно его фильм снискал огромную популярность.

Исторические события в мелодраме «Титаник» служат лишь фоном для развития любовной линии. События развиваются в двух планах: это настоящее (1996 год) и прошлое (1912 год).

В настоящем охотники за сокровищами спускаются на дно Атлантического океана и исследуют затонувший лайнер «Титаник», их цель — поиск различных ценностей, хранящихся на дне. Результаты этой экспедиции освещает телеканал  CNN. Роза Дьюитт Бьюкейтер (Глория Стюарт), одна из пассажирок «Титаника», выжившая после крушения, видит по телевизору этот сюжет и  звонит охотнику за сокровищами Броку Лаветту (Билл Пэкстон).Она обещает раскрыть ему тайну сокровищ.

Второй план повествования – это история любви юной Розы (ее в молодости играет Кейт Уинслет). На борту судна она случайно знакомится с бродягой и художником по имени Джек Доусон (Леонардо ДиКаприо). По настоянию своей семьи Роза планирует выйти замуж за Каледона Хокли (Билли Зейн), которого не любит и не уважает. Она хочет совершить самоубийство, спрыгнув с кормы судна. Джек замечает её и не позволяет совершить столь опрометчивый поступок.

Джек влюбляется в Розу, но муж с помощью охраны судна контролирует все ее действия, и у молодых людей нет возможности видеться. Однако Розе все же удается встретиться с Джеком. Молодая женщина тоже понимает, что это любовь с первого взгляда. Однако их истории не суждено было продлиться: происходит крушение, Джек ценой собственной жизни спасает Розу. И все, что ей остается от этой короткой, но яркой встречи с настоящей любовью – это воспоминания о тех минутах, когда она была по-настоящему счастлива.'),
  (3, '"Звездные войны" - это культовая научно-фантастическая франшиза, созданная режиссером Джорджем Лукасом. Франшиза включает в себя множество фильмов, телевизионных шоу, книг, комиксов и видеоигр, которые рассказывают истории о далекой галактике, разделенной на светлую и темную стороны Силы, о борьбе за свободу и справедливость, о приключениях джедаев, ситхов, пилотов, контрабандистов и других персонажей.

Самая известная часть франшизы - история о Саге Скайуокеров, начиная с первой трилогии, которая включает в себя следующие фильмы:

"Звездные войны: Эпизод IV – Новая надежда" (1977) - начало истории, в которой молодой фермер Люк Скайуокер вступает в борьбу с Империей вместе с принцессой Леей, контрабандистом Ханом Соло и джедаем Оби-Ваном Кеноби.
"Звездные войны: Эпизод V – Империя наносит ответный удар" (1980) - продолжение приключений Люка, который обучается силам Джедая у мудрого мастера Йоды, в то время как Империя строит новое оружие для уничтожения повстанцев.
"Звездные войны: Эпизод VI – Возвращение джедая" (1983) - заключительная часть оригинальной трилогии, в которой Люк и его друзья сражаются с Императором Палпатином и его последними сторонниками, чтобы спасти галактику.
Каждая трилогия и дополнительные фильмы расширяют мир Звездных Войн, добавляя новые персонажи, сюжетные линии и визуальные эффекты, и вместе они создают богатый и увлекательный космический эпос.'),
  (4, '"Игра в имитацию" - это биографический драматический фильм, выпущенный в 2014 году и режиссированный Мортеном Тильдумом. Фильм основан на реальных событиях и рассказывает историю Алана Тьюринга, британского математика и криптографа, который во время Второй мировой войны играл ключевую роль в разгадке немецкого шифра "Энигма", что считается одним из важнейших событий в ходе войны.

Действие фильма происходит в двух временных периодах: во время войны и в 1950-х годах. Во время войны Тьюринг (сыгранный Бенедиктом Камбербэтчем) работает в тайной британской разведывательной организации, пытаясь разгадать шифр "Энигма" вместе с группой других ученых и лингвистов. В 1950-х годах он сталкивается с обвинениями в гомосексуализме, который в то время считался преступлением в Великобритании.

Фильм не только показывает важную историческую роль Тьюринга в разгадке шифра и его влияние на исследования в области информатики, но также затрагивает его личную жизнь, борьбу с социальными нормами и последствия его работы для его будущего. "Игра в имитацию" принесла признание за выдающиеся выступления актеров и заинтересовала зрителей своим проницательным взглядом на жизнь одного из самых ярких умов XX века.'),
  (5, '"Пианист" - это драматический военный фильм режиссёра Романа Полански, выпущенный в 2002 году. Он основан на автобиографических записях польского пианиста и композитора Владислава Шпильмана.

Фильм рассказывает о Шпильмане (сыгранном Адриеном Броуди), еврейском пианисте, который выживает во время Второй мировой войны в оккупированном нацистами Варшаве. Шпильман оказывается разделенным от своей семьи и сталкивается с ужасными условиями жизни в гетто и потом во время восстания в Варшавском гетто.

По мере того, как ситуация становится все более опасной для евреев, Шпильман вынужден скрываться и бороться за выживание, прячась от нацистских охотников за евреями. Его музыкальные навыки становятся ключом к его выживанию, а также источником надежды и вдохновения в мире разрушений и страданий.

"Пианист" восхваляется за свою правдивую и трогательную рассказ о выживании во время холокоста, за потрясающую игру актёров и за тонкое изображение человеческой силы в самых мрачных временах. Фильм удостоен множества наград, включая Оскар за лучший фильм, и стал одним из самых запоминающихся и влиятельных произведений о Холокосте.'),
  (6, '"Гарри Поттер и философский камень" - это первый фильм из серии экранизаций книг о Гарри Поттере, написанных Дж. К. Роулинг. Режиссёром фильма является Крис Коламбус. Фильм был выпущен в 2001 году.

История начинается с приема одиннадцатилетнего мальчика Гарри Поттера в Школу чародейства и волшебства Хогвартс. Он узнает, что он наследник известной волшебнической семьи и что его родители были убиты тёмным волшебником по имени Волан-де-Морт, известным также как Лорд Волдеморт. В Хогвартсе Гарри встречает новых друзей, Ронуи Уизли и Гермиону Грейнджер, и они вместе начинают исследовать тайны, связанные с прошлым Гарри и его родителей.

Центральным сюжетным элементом фильма является поиск "философского камня", магического артефакта, который придает бессмертие. Однако, они понимают, что камень находится в опасности, так как Лорд Волдеморт и его приверженцы стремятся к его власти. Гарри и его друзья должны использовать свои навыки и смекалку, чтобы защитить камень и предотвратить его попадание в руки злодея.

Фильм "Гарри Поттер и философский камень" завоевал популярность благодаря своей магии, приключениям и чудесному воплощению мира, описанного в книгах Роулинг. Он стал первым шагом в путешествии Гарри Поттера через мир магии и приключений.');

UPDATE tickets
SET TicketPriceID = 3
WHERE idTickets = 3;


DELETE FROM booking;

SELECT h.idHalls, h.HallName, h.Seat, hc.Capacity
FROM halls h
JOIN halltype ht ON h.idHallType = ht.idHallType
JOIN hallcapacities hc ON h.idHallType = hc.idHallType
WHERE ht.HallType = '2D';


INSERT INTO booking (idUser, idSession, NumOfTic, AmountPaid, BookingStatus, DateBooking, BookedSeats)
VALUES (1, 1, 2, 20.00, 0, NOW(), ARRAY[2, 9]);

ALTER TABLE booking
ADD COLUMN BookedSeats INT[] NOT NULL;

UPDATE booking
SET BookedSeats = BookedSeats || ARRAY[ваш_выбранный_номер_места]
WHERE [условие_бронирования];

SELECT h.Seat - COUNT(b.BookedSeats) AS FreeSeats
FROM halls h
LEFT JOIN booking b ON h.idHalls = b.idHalls
WHERE b.idSession = ваш_выбранный_сеанс_или_условие_сеанса
GROUP BY h.idHalls, h.Seat;

