import psycopg2
from flask import Flask, jsonify, request, render_template, redirect

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="aliya",
    user="postgres",
    password="nurik",
    host="localhost",
    port="5432"
)
# cur = conn.cursor()

@app.route('/directors', methods=['GET'])
def get_directors():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM director")
        directors = cur.fetchall()
        output = [{'idDirector': row[0], 'DirectorsName': row[1]} for row in directors]
        return jsonify({'directors': output})

@app.route('/genes', methods=['GET'])
def get_genes():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM genes")
        genes = cur.fetchall()
        output = [{'idGenes': row[0], 'GenerName': row[1]} for row in genes]
        return jsonify({'genes': output})


@app.route('/films', methods=['GET'])
def get_films():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM films JOIN director ON films.idDirector = director.idDirector JOIN genes ON films.idGener = genes.idGenes")
        films = cur.fetchall()
        return render_template('films.html', films=films)

# @app.route('/add_film', methods=['GET', 'POST'])
# def add_film():
#     if request.method == 'POST':
#         data = request.form
#         cur.execute("INSERT INTO films (FilmName, YearOfIssue, idDirector, idGener) VALUES (%s, %s, %s, %s)", (data['name'], data['year'], data['director'], data['genre']))
#         conn.commit()
#         return redirect('/films')
#     return render_template('add_film.html')

@app.route('/add_film', methods=['GET', 'POST'])
def add_film():
    with conn.cursor() as cur:
        if request.method == 'POST':
            data = request.form
            cur.execute("INSERT INTO films (FilmName, YearOfIssue, idDirector, idGener) VALUES (%s, %s, %s, %s)", (data['name'], data['year'], data['director'], data['genre']))
            conn.commit()
            return redirect('/films')
    return render_template('add_film.html')

@app.route('/update_film/<int:film_id>', methods=['GET', 'POST'])
def update_film(film_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM films WHERE idFilms = %s", (film_id,))
        film = cur.fetchone()
        if request.method == 'POST':
            data = request.form
            cur.execute("UPDATE films SET FilmName = %s, YearOfIssue = %s, idDirector = %s, idGener = %s WHERE idFilms = %s", (data['name'], data['year'], data['director'], data['genre'], film_id))
            conn.commit()
            return redirect('/films')
    return render_template('update_film.html', film=film)

@app.route('/delete_film/<int:film_id>', methods=['GET', 'POST'])
def delete_film(film_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM films WHERE idFilms = %s", (film_id,))
        film = cur.fetchone()
        if request.method == 'POST':
            cur.execute("DELETE FROM films WHERE idFilms = %s", (film_id,))
            conn.commit()
            return redirect('/films')
    return render_template('delete_film.html', film=film)

@app.route('/halltypes', methods=['GET'])
def get_halltypes():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM halltype")
        halltypes = cur.fetchall()
        return render_template('halltypes.html', halltypes=halltypes)

@app.route('/add_halltype', methods=['GET', 'POST'])
def add_halltype():
    with conn.cursor() as cur:
        if request.method == 'POST':
            data = request.form
            cur.execute("INSERT INTO halltype (halltype) VALUES (%s)", (data['halltype'],))
            conn.commit()
            return redirect('/halltypes')
    return render_template('add_halltype.html')

@app.route('/update_halltype/<int:halltype_id>', methods=['GET', 'POST'])
def update_halltype(halltype_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM halltype WHERE idHallType = %s", (halltype_id,))
        halltype = cur.fetchone()
        if request.method == 'POST':
            data = request.form
            cur.execute("UPDATE halltype SET HallType = %s WHERE idHallType = %s", (data['halltype'], halltype_id))
            conn.commit()
            return redirect('/halltypes')
    return render_template('update_halltype.html', halltype=halltype)

@app.route('/delete_halltype/<int:halltype_id>', methods=['GET', 'POST'])
def delete_halltype(halltype_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM halltype WHERE idHallType = %s", (halltype_id,))
        halltype = cur.fetchone()
        if request.method == 'POST':
            cur.execute("DELETE FROM halltype WHERE idHallType = %s", (halltype_id,))
            conn.commit()
            return redirect('/halltypes')
    return render_template('delete_halltype.html', halltype=halltype)

@app.route('/halls', methods=['GET'])
def get_halls():
    with conn.cursor() as cur:
        cur.execute("SELECT halls.*, halltype.HallType FROM halls JOIN halltype ON halls.idHallType = halltype.idHallType")
        halls = cur.fetchall()
        cur.execute("SELECT * FROM halltype")
        halltypes = cur.fetchall()
        return render_template('halls.html', halls=halls, halltypes=halltypes)

@app.route('/add_hall', methods=['GET', 'POST'])
def add_hall():
    with conn.cursor() as cur:
        if request.method == 'POST':
            data = request.form
            cur.execute("INSERT INTO halls (HallName, Seat, idHallType) VALUES (%s, %s, %s)", (data['hallname'], data['seat'], data['halltype']))
            conn.commit()
            return redirect('/halls')
        cur.execute("SELECT * FROM halltype")
        halltypes = cur.fetchall()
    return render_template('add_hall.html', halltypes=halltypes)

@app.route('/update_hall/<int:hall_id>', methods=['GET', 'POST'])
def update_hall(hall_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM halls WHERE idHalls = %s", (hall_id,))
        hall = cur.fetchone()
        cur.execute("SELECT * FROM halltype")
        halltypes = cur.fetchall()
        if request.method == 'POST':
            data = request.form
            cur.execute("UPDATE halls SET HallName = %s, Seat = %s, idHallType = %s WHERE idHalls = %s", (data['hallname'], data['seat'], data['halltype'], hall_id))
            conn.commit()
            return redirect('/halls')
    return render_template('update_hall.html', hall=hall, halltypes=halltypes)

@app.route('/delete_hall/<int:hall_id>', methods=['GET', 'POST'])
def delete_hall(hall_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM halls WHERE idHalls = %s", (hall_id,))
        hall = cur.fetchone()
        if request.method == 'POST':
            cur.execute("DELETE FROM halls WHERE idHalls = %s", (hall_id,))
            conn.commit()
            return redirect('/halls')
    return render_template('delete_hall.html', hall=hall)



@app.route('/sessions', methods=['GET'])
def get_sessions():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM sessions JOIN films ON sessions.idFilm = films.idFilms JOIN halls ON sessions.idHall = halls.idHalls")
        sessions = cur.fetchall()
        return render_template('sessions.html', sessions=sessions)

@app.route('/add_session', methods=['GET', 'POST'])
def add_session():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM films")
        films = cur.fetchall()
        cur.execute("SELECT * FROM halls")
        halls = cur.fetchall()
        if request.method == 'POST':
            data = request.form
            cur.execute("INSERT INTO sessions (Duration, idFilm, idHall, DateAndTimeStart) VALUES (%s, %s, %s, %s)", (data['duration'], data['film'], data['hall'], data['date']))
            conn.commit()
            return redirect('/sessions')
    return render_template('add_session.html', films=films, halls=halls)

@app.route('/update_session/<int:session_id>', methods=['GET', 'POST'])
def update_session(session_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM sessions WHERE idSessions = %s", (session_id,))
        session = cur.fetchone()
        cur.execute("SELECT * FROM films")
        films = cur.fetchall()
        cur.execute("SELECT * FROM halls")
        halls = cur.fetchall()
        if request.method == 'POST':
            data = request.form
            cur.execute("UPDATE sessions SET Duration = %s, idFilm = %s, idHall = %s, DateAndTimeStart = %s WHERE idSessions = %s", (data['duration'], data['film'], data['hall'], data['date'], session_id))
            conn.commit()
            return redirect('/sessions')
    return render_template('update_session.html', session=session, films=films, halls=halls)

@app.route('/delete_session/<int:session_id>', methods=['GET', 'POST'])
def delete_session(session_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM sessions WHERE idSessions = %s", (session_id,))
        session = cur.fetchone()
        if request.method == 'POST':
            cur.execute("DELETE FROM sessions WHERE idSessions = %s", (session_id,))
            conn.commit()
            return redirect('/sessions')
    return render_template('delete_session.html', session=session)

@app.route('/users', methods=['GET'])
def get_users():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        return render_template('users.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    with conn.cursor() as cur:
        if request.method == 'POST':
            data = request.form
            cur.execute("INSERT INTO users (Name, Surname, Email, Phone) VALUES (%s, %s, %s, %s)", (data['name'], data['surname'], data['email'], data['phone']))
            conn.commit()
            return redirect('/users')
    return render_template('add_user.html')

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE idUsers = %s", (user_id,))
        user = cur.fetchone()
        if request.method == 'POST':
            data = request.form
            cur.execute("UPDATE users SET Name = %s, Surname = %s, Email = %s, Phone = %s WHERE idUsers = %s", (data['name'], data['surname'], data['email'], data['phone'], user_id))
            conn.commit()
            return redirect('/users')
    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE idUsers = %s", (user_id,))
        user = cur.fetchone()
        if request.method == 'POST':
            cur.execute("DELETE FROM users WHERE idUsers = %s", (user_id,))
            conn.commit()
            return redirect('/users')
    return render_template('delete_user.html', user=user)


@app.route('/booking', methods=['GET'])
def get_booking():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM booking")
        bookings = cur.fetchall()
        output = [{'idBooking': row[0], 'idUser': row[1], 'idSession': row[2], 'NumOfTic': row[3], 'AmountPaid': row[4], 'BookingStatus': row[5], 'DateBooking': row[6]} for row in bookings]
        return jsonify({'bookings': output})

@app.route('/booking', methods=['POST'])
def add_booking():
    data = request.json
    with conn.cursor() as cur:
        cur.execute("INSERT INTO booking (idUser, idSession, NumOfTic, AmountPaid, BookingStatus, DateBooking) VALUES (%s, %s, %s, %s, %s, %s)", (data['idUser'], data['idSession'], data['NumOfTic'], data['AmountPaid'], data['BookingStatus'], data['DateBooking']))
        conn.commit()
        return jsonify({'message': 'Booking added successfully'})

@app.route('/booking/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.json
    with conn.cursor() as cur:
        cur.execute("UPDATE booking SET idUser = %s, idSession = %s, NumOfTic = %s, AmountPaid = %s, BookingStatus = %s, DateBooking = %s WHERE idBooking = %s", (data['idUser'], data['idSession'], data['NumOfTic'], data['AmountPaid'], data['BookingStatus'], data['DateBooking'], booking_id))
        conn.commit()
        return jsonify({'message': 'Booking updated successfully'})

@app.route('/booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM booking WHERE idBooking = %s", (booking_id,))
        conn.commit()
        return jsonify({'message': 'Booking deleted successfully'})

@app.route('/hallcapacities', methods=['GET'])
def get_hallcapacities():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hallcapacities")
        hallcapacities = cur.fetchall()
        output = [{'idHall': row[0], 'idHallType': row[1], 'Capacity': row[2]} for row in hallcapacities]
        return jsonify({'hallcapacities': output})

@app.route('/hallcapacities', methods=['POST'])
def add_hallcapacity():
    data = request.json
    with conn.cursor() as cur:
        cur.execute("INSERT INTO hallcapacities (idHall, idHallType, Capacity) VALUES (%s, %s, %s)", (data['idHall'], data['idHallType'], data['Capacity']))
        conn.commit()
        return jsonify({'message': 'Hall capacity added successfully'})

@app.route('/hallcapacities/<int:hall_id>', methods=['PUT'])
def update_hallcapacity(hall_id):
    data = request.json
    with conn.cursor() as cur:
        cur.execute("UPDATE hallcapacities SET idHallType = %s, Capacity = %s WHERE idHall = %s", (data['idHallType'], data['Capacity'], hall_id))
        conn.commit()
        return jsonify({'message': 'Hall capacity updated successfully'})

@app.route('/hallcapacities/<int:hall_id>', methods=['DELETE'])
def delete_hallcapacity(hall_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hallcapacities WHERE idHall = %s", (hall_id,))
        conn.commit()
        return jsonify({'message': 'Hall capacity deleted successfully'})

@app.route('/rating', methods=['GET'])
def get_rating():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM rating")
        ratings = cur.fetchall()
        output = [{'idRating': row[0], 'idFilm': row[1], 'Rating': row[2]} for row in ratings]
        return jsonify({'ratings': output})

@app.route('/rating', methods=['POST'])
def add_rating():
    data = request.json
    with conn.cursor() as cur:
        cur.execute("INSERT INTO rating (idFilm, Rating) VALUES (%s, %s)", (data['idFilm'], data['Rating']))
        conn.commit()
        return jsonify({'message': 'Rating added successfully'})

@app.route('/rating/<int:rating_id>', methods=['PUT'])
def update_rating(rating_id):
    data = request.json
    with conn.cursor() as cur:
        cur.execute("UPDATE rating SET idFilm = %s, Rating = %s WHERE idRating = %s", (data['idFilm'], data['Rating'], rating_id))
        conn.commit()
        return jsonify({'message': 'Rating updated successfully'})

@app.route('/rating/<int:rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM rating WHERE idRating = %s", (rating_id,))
        conn.commit()
        return jsonify({'message': 'Rating deleted successfully'})

@app.route('/ticket_prices', methods=['GET'])
def get_ticket_prices():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM TicketPrices")
        ticket_prices = cur.fetchall()
        return render_template('ticket_prices.html', ticket_prices=ticket_prices)

@app.route('/add_ticket_price', methods=['GET', 'POST'])
def add_ticket_price():
    if request.method == 'POST':
        data = request.form
        with conn.cursor() as cur:
            cur.execute("INSERT INTO TicketPrices (price) VALUES (%s)", (data['price'],))
            conn.commit()
        return redirect('/ticket_prices')
    return render_template('add_ticket_price.html')

@app.route('/update_ticket_price/<int:ticket_price_id>', methods=['GET', 'POST'])
def update_ticket_price(ticket_price_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM TicketPrices WHERE TicketPriceID = %s", (ticket_price_id,))
        ticket_price = cur.fetchone()
    if request.method == 'POST':
        data = request.form
        with conn.cursor() as cur:
            cur.execute("UPDATE TicketPrices SET price = %s WHERE TicketPriceID = %s", (data['price'], ticket_price_id))
            conn.commit()
        return redirect('/ticket_prices')
    return render_template('update_ticket_price.html', ticket_price=ticket_price)

@app.route('/delete_ticket_price/<int:ticket_price_id>', methods=['GET', 'POST'])
def delete_ticket_price(ticket_price_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM TicketPrices WHERE TicketPriceID = %s", (ticket_price_id,))
        ticket_price = cur.fetchone()
    if request.method == 'POST':
        with conn.cursor() as cur:
            cur.execute("DELETE FROM TicketPrices WHERE TicketPriceID = %s", (ticket_price_id,))
            conn.commit()
        return redirect('/ticket_prices')
    return render_template('delete_ticket_price.html', ticket_price=ticket_price)

@app.route('/tickets', methods=['GET'])
def get_tickets():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tickets")
        tickets = cur.fetchall()
    return render_template('tickets.html', tickets=tickets)

@app.route('/add_ticket', methods=['GET', 'POST'])
def add_ticket():
    if request.method == 'POST':
        data = request.form
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tickets (idUser, idSession, TicketPriceID) VALUES (%s, %s, %s)", (data['user_id'], data['session_id'], data['ticket_price_id']))
            conn.commit()
        return redirect('/tickets')
    return render_template('add_ticket.html')

@app.route('/update_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tickets WHERE idTickets = %s", (ticket_id,))
        ticket = cur.fetchone()
    if request.method == 'POST':
        data = request.form
        with conn.cursor() as cur:
            cur.execute("UPDATE tickets SET idUser = %s, idSession = %s, TicketPriceID = %s WHERE idTickets = %s", (data['user_id'], data['session_id'], data['ticket_price_id'], ticket_id))
            conn.commit()
        return redirect('/tickets')
    return render_template('update_ticket.html', ticket=ticket)

@app.route('/delete_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def delete_ticket(ticket_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tickets WHERE idTickets = %s", (ticket_id,))
        ticket = cur.fetchone()
    if request.method == 'POST':
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tickets WHERE idTickets = %s", (ticket_id,))
            conn.commit()
        return redirect('/tickets')
    return render_template('delete_ticket.html', ticket=ticket)




# @app.route('/book_ticket', methods=['GET'])
# def book_ticket_page():
#     cur.execute("SELECT * FROM films")
#     films = cur.fetchall()
#     cur.execute("SELECT * FROM sessions")
#     sessions = cur.fetchall()
#     return render_template('booking.html', films=films, sessions=sessions)

# @app.route('/book_ticket', methods=['GET'])
# def book_ticket_page():
#     cur.execute("SELECT * FROM films")
#     films = cur.fetchall()
#     return render_template('booking.html', films=films)

@app.route('/')
def index():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM films")
        films = cur.fetchall()
    return render_template('index.html', films=films)


@app.route('/book_ticket', methods=['GET'])
def book_ticket_page():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM films")
        films = cur.fetchall()
        cur.execute("SELECT * FROM sessions")
        sessions = cur.fetchall()
        cur.execute("SELECT idUsers, Name, Surname FROM users")
        users = cur.fetchall()
        cur.execute("SELECT * FROM halltype")
        hall_types = cur.fetchall()
        cur.execute("SELECT * FROM ticketprices")
        ticket_prices = cur.fetchall()
    return render_template('booking.html', films=films, sessions=sessions, users=users, hall_types=hall_types, ticket_prices=ticket_prices)


# @app.route('/book_ticket', methods=['GET'])
# def book_ticket_page():
#     cur.execute("SELECT * FROM sessions")
#     sessions = cur.fetchall()
#     return render_template('booking.html', sessions=sessions)

# @app.route('/get_sessions_by_film', methods=['POST'])
# def get_sessions_by_film():
#     film_id = request.form.get('film_id')  
#     cur.execute("SELECT * FROM sessions WHERE idFilm = %s", (film_id,))
#     sessions = cur.fetchall()
#     return jsonify(sessions)

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    if request.method == 'POST':
        data = request.form
        film_id = data['film_id']
        session_id = data['session_id']
        user_id = data['user_id']
        seat = data['seat']
        hall_type = data['hall_type']
        ticket_price_id = data['ticket_price_id']
        
        conn.rollback()  
        conn.autocommit = True 
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM halls WHERE idHalls = %s", (seat,))
            hall_data = cur.fetchone()

            if hall_data:
                cur.execute("INSERT INTO tickets (idUser, idSession, TicketPriceID) VALUES (%s, %s, %s)", (user_id, session_id, ticket_price_id))
                conn.commit()
                return redirect('/tickets')
            else:
                return "Место не найдено или уже занято"



@app.route('/films/<int:film_id>')
def show_film_info(film_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT f.FilmName, f.YearOfIssue, d.DirectorsName, g.GenerName, fi.image_url, fd.description, r.Rating
            FROM films f
            JOIN director d ON f.idDirector = d.idDirector
            JOIN genes g ON f.idGener = g.idGenes
            LEFT JOIN film_images fi ON f.idFilms = fi.film_id
            LEFT JOIN film_descriptions fd ON f.idFilms = fd.film_id
            LEFT JOIN rating r ON f.idFilms = r.idFilm
            WHERE f.idFilms = %s
        """, (film_id,))
        film_info = cur.fetchone()
    return render_template('film_info.html', film_info=film_info)


if __name__ == '__main__':
    app.run(debug=True)
