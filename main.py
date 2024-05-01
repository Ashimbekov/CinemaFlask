from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nurik@localhost:5432/cinema'

db = SQLAlchemy(app)

class Director(db.Model):
    idDirector = db.Column(db.Integer, primary_key=True)
    DirectorsName = db.Column(db.String(45), nullable=False)

class Genes(db.Model):
    idGenes = db.Column(db.Integer, primary_key=True)
    GenerName = db.Column(db.String(45), nullable=False)

class Films(db.Model):
    idFilms = db.Column(db.Integer, primary_key=True)
    FilmName = db.Column(db.String(45), nullable=False)
    YearOfIssue = db.Column(db.Date, nullable=False)
    idDirector = db.Column(db.Integer, db.ForeignKey('director.idDirector'), nullable=False)
    idGener = db.Column(db.Integer, db.ForeignKey('genes.idGenes'), nullable=False)
    director = db.relationship('Director', backref='films')
    genes = db.relationship('Genes', backref='films')

class HallType(db.Model):
    idHallType = db.Column(db.Integer, primary_key=True)
    HallType = db.Column(db.String(45), nullable=False)

class Halls(db.Model):
    idHalls = db.Column(db.Integer, primary_key=True)
    HallName = db.Column(db.String(45), nullable=False)
    Seat = db.Column(db.Integer, nullable=False)
    idHallType = db.Column(db.Integer, db.ForeignKey('halltype.idHallType'), nullable=False)
    halltype = db.relationship('HallType', backref='halls')

class Sessions(db.Model):
    idSessions = db.Column(db.Integer, primary_key=True)
    Duration = db.Column(db.Integer, nullable=False)
    idFilm = db.Column(db.Integer, db.ForeignKey('films.idFilms'), nullable=False)
    idHall = db.Column(db.Integer, db.ForeignKey('halls.idHalls'), nullable=False)
    DateAndTimeStart = db.Column(db.TIMESTAMP, nullable=True)
    film = db.relationship('Films', backref='sessions')
    hall = db.relationship('Halls', backref='sessions')

class Users(db.Model):
    idUsers = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(45), nullable=False)
    Surname = db.Column(db.String(45), nullable=False)
    Email = db.Column(db.String(45), nullable=False)
    Phone = db.Column(db.String(45), nullable=False)

class Booking(db.Model):
    idBooking = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('users.idUsers'), nullable=False)
    idSession = db.Column(db.Integer, db.ForeignKey('sessions.idSessions'), nullable=False)
    NumOfTic = db.Column(db.Integer, nullable=False)
    AmountPaid = db.Column(db.Numeric(10, 2), nullable=False)
    BookingStatus = db.Column(db.SmallInteger, nullable=False, default=0)
    DateBooking = db.Column(db.TIMESTAMP, nullable=False)
    user = db.relationship('Users', backref='bookings')
    session = db.relationship('Sessions', backref='bookings')

class HallCapacities(db.Model):
    idHall = db.Column(db.Integer, db.ForeignKey('halls.idHalls'), primary_key=True)
    idHallType = db.Column(db.Integer, db.ForeignKey('halltype.idHallType'), nullable=False)
    Capacity = db.Column(db.String(45), nullable=False)
    halltype = db.relationship('HallType', backref='hallcapacities')

class Rating(db.Model):
    idRating = db.Column(db.Integer, primary_key=True)
    idFilm = db.Column(db.Integer, db.ForeignKey('films.idFilms'))
    Rating = db.Column(db.String(45))
    film = db.relationship('Films', backref='ratings')

class TicketPrices(db.Model):
    TicketPriceID = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.DECIMAL)

class Tickets(db.Model):
    idTickets = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('users.idUsers'), nullable=False)
    idSession = db.Column(db.Integer, db.ForeignKey('sessions.idSessions'), nullable=False)
    TicketPriceID = db.Column(db.Integer, db.ForeignKey('ticketprices.TicketPriceID'), nullable=False)
    user = db.relationship('Users', backref='tickets')
    session = db.relationship('Sessions', backref='tickets')
    ticketprice = db.relationship('TicketPrices', backref='tickets')

@app.route('/directors', methods=['GET'])
def get_directors():
    directors = Director.query.all()
    output = []
    for director in directors:
        director_data = {'idDirector': director.idDirector, 'DirectorsName': director.DirectorsName}
        output.append(director_data)
    return jsonify({'directors': output})

@app.route('/genes', methods=['GET'])
def get_genes():
    genes = Genes.query.all()
    output = []
    for gene in genes:
        gene_data = {'idGenes': gene.idGenes, 'GenerName': gene.GenerName}
        output.append(gene_data)
    return jsonify({'genes': output})

@app.route('/films', methods=['GET'])
def get_films():
    films = Films.query.all()
    output = []
    for film in films:
        film_data = {
            'idFilms': film.idFilms,
            'FilmName': film.FilmName,
            'YearOfIssue': film.YearOfIssue.strftime('%Y-%m-%d'),  # Convert date to string
            'Director': film.director.DirectorsName,
            'Genre': film.genes.GenerName
        }
        output.append(film_data)
    return jsonify({'films': output})

@app.route('/films', methods=['POST'])
def add_film():
    data = request.json
    new_film = Films(FilmName=data['FilmName'], YearOfIssue=data['YearOfIssue'], idDirector=data['idDirector'], idGener=data['idGener'])
    db.session.add(new_film)
    db.session.commit()
    return jsonify({'message': 'Film added successfully'})

@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    film = Films.query.get(film_id)
    data = request.json
    film.FilmName = data['FilmName']
    film.YearOfIssue = data['YearOfIssue']
    film.idDirector = data['idDirector']
    film.idGener = data['idGener']
    db.session.commit()
    return jsonify({'message': 'Film updated successfully'})

@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film = Films.query.get(film_id)
    db.session.delete(film)
    db.session.commit()
    return jsonify({'message': 'Film deleted successfully'})

@app.route('/halltypes', methods=['GET'])
def get_halltypes():
    halltypes = HallType.query.all()
    output = []
    for halltype in halltypes:
        halltype_data = {'idHallType': halltype.idHallType, 'HallType': halltype.HallType}
        output.append(halltype_data)
    return jsonify({'halltypes': output})

@app.route('/halls', methods=['POST'])
def add_hall():
    data = request.json
    new_hall = Halls(HallName=data['HallName'], Seat=data['Seat'], idHallType=data['idHallType'])
    db.session.add(new_hall)
    db.session.commit()
    return jsonify({'message': 'Hall added successfully'})

@app.route('/halls/<int:hall_id>', methods=['PUT'])
def update_hall(hall_id):
    hall = Halls.query.get(hall_id)
    data = request.json
    hall.HallName = data['HallName']
    hall.Seat = data['Seat']
    hall.idHallType = data['idHallType']
    db.session.commit()
    return jsonify({'message': 'Hall updated successfully'})

@app.route('/halls/<int:hall_id>', methods=['DELETE'])
def delete_hall(hall_id):
    hall = Halls.query.get(hall_id)
    db.session.delete(hall)
    db.session.commit()
    return jsonify({'message': 'Hall deleted successfully'})

@app.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = Sessions.query.all()
    output = []
    for session in sessions:
        session_data = {
            'idSessions': session.idSessions,
            'Duration': session.Duration,
            'idFilm': session.idFilm,
            'idHall': session.idHall,
            'DateAndTimeStart': session.DateAndTimeStart
        }
        output.append(session_data)
    return jsonify({'sessions': output})

@app.route('/sessions', methods=['POST'])
def add_session():
    data = request.json
    new_session = Sessions(
        Duration=data['Duration'],
        idFilm=data['idFilm'],
        idHall=data['idHall'],
        DateAndTimeStart=data['DateAndTimeStart']
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'message': 'Session added successfully'})

@app.route('/sessions/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    session = Sessions.query.get(session_id)
    data = request.json
    session.Duration = data['Duration']
    session.idFilm = data['idFilm']
    session.idHall = data['idHall']
    session.DateAndTimeStart = data['DateAndTimeStart']
    db.session.commit()
    return jsonify({'message': 'Session updated successfully'})

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Sessions.query.get(session_id)
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session deleted successfully'})

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    output = []
    for user in users:
        user_data = {
            'idUsers': user.idUsers,
            'Name': user.Name,
            'Surname': user.Surname,
            'Email': user.Email,
            'Phone': user.Phone
        }
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = Users(
        Name=data['Name'],
        Surname=data['Surname'],
        Email=data['Email'],
        Phone=data['Phone']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.query.get(user_id)
    data = request.json
    user.Name = data['Name']
    user.Surname = data['Surname']
    user.Email = data['Email']
    user.Phone = data['Phone']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


@app.route('/booking', methods=['GET'])
def get_booking():
    bookings = Booking.query.all()
    output = []
    for booking in bookings:
        booking_data = {
            'idBooking': booking.idBooking,
            'idUser': booking.idUser,
            'idSession': booking.idSession,
            'NumOfTic': booking.NumOfTic,
            'AmountPaid': str(booking.AmountPaid),
            'BookingStatus': booking.BookingStatus,
            'DateBooking': booking.DateBooking
        }
        output.append(booking_data)
    return jsonify({'bookings': output})

@app.route('/booking', methods=['POST'])
def add_booking():
    data = request.json
    new_booking = Booking(
        idUser=data['idUser'],
        idSession=data['idSession'],
        NumOfTic=data['NumOfTic'],
        AmountPaid=data['AmountPaid'],
        BookingStatus=data['BookingStatus'],
        DateBooking=data['DateBooking']
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking added successfully'})

@app.route('/booking/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    data = request.json
    booking.idUser = data['idUser']
    booking.idSession = data['idSession']
    booking.NumOfTic = data['NumOfTic']
    booking.AmountPaid = data['AmountPaid']
    booking.BookingStatus = data['BookingStatus']
    booking.DateBooking = data['DateBooking']
    db.session.commit()
    return jsonify({'message': 'Booking updated successfully'})

@app.route('/booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted successfully'})

@app.route('/hallcapacities', methods=['GET'])
def get_hallcapacities():
    hallcapacities = HallCapacities.query.all()
    output = []
    for hallcapacity in hallcapacities:
        hallcapacity_data = {
            'idHall': hallcapacity.idHall,
            'idHallType': hallcapacity.idHallType,
            'Capacity': hallcapacity.Capacity
        }
        output.append(hallcapacity_data)
    return jsonify({'hallcapacities': output})

@app.route('/hallcapacities', methods=['POST'])
def add_hallcapacity():
    data = request.json
    new_hallcapacity = HallCapacities(
        idHall=data['idHall'],
        idHallType=data['idHallType'],
        Capacity=data['Capacity']
    )
    db.session.add(new_hallcapacity)
    db.session.commit()
    return jsonify({'message': 'Hall capacity added successfully'})

@app.route('/hallcapacities/<int:hall_id>', methods=['PUT'])
def update_hallcapacity(hall_id):
    hallcapacity = HallCapacities.query.get(hall_id)
    data = request.json
    hallcapacity.idHallType = data['idHallType']
    hallcapacity.Capacity = data['Capacity']
    db.session.commit()
    return jsonify({'message': 'Hall capacity updated successfully'})

@app.route('/hallcapacities/<int:hall_id>', methods=['DELETE'])
def delete_hallcapacity(hall_id):
    hallcapacity = HallCapacities.query.get(hall_id)
    db.session.delete(hallcapacity)
    db.session.commit()
    return jsonify({'message': 'Hall capacity deleted successfully'})


@app.route('/rating', methods=['GET'])
def get_rating():
    ratings = Rating.query.all()
    output = []
    for rating in ratings:
        rating_data = {
            'idRating': rating.idRating,
            'idFilm': rating.idFilm,
            'Rating': rating.Rating
        }
        output.append(rating_data)
    return jsonify({'ratings': output})

@app.route('/rating', methods=['POST'])
def add_rating():
    data = request.json
    new_rating = Rating(
        idFilm=data['idFilm'],
        Rating=data['Rating']
    )
    db.session.add(new_rating)
    db.session.commit()
    return jsonify({'message': 'Rating added successfully'})

@app.route('/rating/<int:rating_id>', methods=['PUT'])
def update_rating(rating_id):
    rating = Rating.query.get(rating_id)
    data = request.json
    rating.idFilm = data['idFilm']
    rating.Rating = data['Rating']
    db.session.commit()
    return jsonify({'message': 'Rating updated successfully'})

@app.route('/rating/<int:rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    rating = Rating.query.get(rating_id)
    db.session.delete(rating)
    db.session.commit()
    return jsonify({'message': 'Rating deleted successfully'})


@app.route('/TicketPrices', methods=['GET'])
def get_ticket_prices():
    ticket_prices = TicketPrices.query.all()
    output = []
    for ticket_price in ticket_prices:
        ticket_price_data = {
            'TicketPriceID': ticket_price.TicketPriceID,
            'price': str(ticket_price.price)
        }
        output.append(ticket_price_data)
    return jsonify({'ticket_prices': output})

@app.route('/TicketPrices', methods=['POST'])
def add_ticket_price():
    data = request.json
    new_ticket_price = TicketPrices(
        price=data['price']
    )
    db.session.add(new_ticket_price)
    db.session.commit()
    return jsonify({'message': 'Ticket price added successfully'})

@app.route('/TicketPrices/<int:ticket_price_id>', methods=['PUT'])
def update_ticket_price(ticket_price_id):
    ticket_price = TicketPrices.query.get(ticket_price_id)
    data = request.json
    ticket_price.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Ticket price updated successfully'})

@app.route('/TicketPrices/<int:ticket_price_id>', methods=['DELETE'])
def delete_ticket_price(ticket_price_id):
    ticket_price = TicketPrices.query.get(ticket_price_id)
    db.session.delete(ticket_price)
    db.session.commit()
    return jsonify({'message': 'Ticket price deleted successfully'})


@app.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = Tickets.query.all()
    output = []
    for ticket in tickets:
        ticket_data = {
            'idTickets': ticket.idTickets,
            'idUser': ticket.idUser,
            'idSession': ticket.idSession,
            'TicketPriceID': ticket.TicketPriceID
        }
        output.append(ticket_data)
    return jsonify({'tickets': output})

@app.route('/tickets', methods=['POST'])
def add_ticket():
    data = request.json
    new_ticket = Tickets(
        idUser=data['idUser'],
        idSession=data['idSession'],
        TicketPriceID=data['TicketPriceID']
    )
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket added successfully'})

@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = Tickets.query.get(ticket_id)
    data = request.json
    ticket.idUser = data['idUser']
    ticket.idSession = data['idSession']
    ticket.TicketPriceID = data['TicketPriceID']
    db.session.commit()
    return jsonify({'message': 'Ticket updated successfully'})

@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Tickets.query.get(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
