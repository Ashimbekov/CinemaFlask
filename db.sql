
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

INSERT INTO director VALUES (1,'Ашимбеков Нурдаулет'),(2,'Джордж ЛукДжеймс Кэмеронас'),(3,'Джордж Лукас'),(4,'Рон Ховард'),(5,'Роман Полански'),(6,'Крис Коламбус');

UPDATE tickets
SET TicketPriceID = 3
WHERE idTickets = 3;


DELETE FROM booking;

