print(
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#####################    Tema n. 1 - Traccia n.1.4   ############################
#                    La digitalizzazione dell’impresa                           #
#                             Marco Matteocci                                   #
#################################################################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
)

# Importo i moduli necessari al funzionamento dell'applicazione
from os import path
from sqlalchemy import or_
from collections import defaultdict
from datetime import datetime, timedelta, time, date
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash
from models import User, Structure, Membership, Course, Booking, CourseSchedule, UserSubscription
from db import db
from seeded_data import seeded_users, seeded_structures, seeded_memberships, seeded_courses
import random

# Istanzo e inizializzo l'applicazione Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///gymcourses.db"
# Consiglio di generare un nuova chiave usando os.urandom(24).hex()
app.config['SECRET_KEY'] = "7026ca2d23dd9c138855eddb733c97f3dd7de2f849160c5b"

# Utilizzo CSRFProtect per proteggere le form dalle vulnerabilità CSRF
csrf = CSRFProtect(app)

# Inizializzo l'instance di LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
login_manager.login_message = 'Effettua il login per visualizzare la pagina'


# Funzione per ottenere l'utente corrente (sessione)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Funzione per ottenere le prenotazioni di un utente
def get_booking_user(user_id):
    # Ottieni tutte le prenotazioni fatte dall'utente
    bookings = Booking.query.filter_by(user_id=user_id).all()

    if not bookings:
        print(f"Nessuna prenotazione trovata per l'utente con ID {user_id}")
        return []

    return bookings


# Funzione per ottenere tutte le membership di un utente
def get_user_memberships(user_id):
    user_subscriptions = db.session.query(UserSubscription) \
        .join(Membership, UserSubscription.subscription_id == Membership.id) \
        .filter(UserSubscription.user_id == user_id) \
        .all()

    if not user_subscriptions:
        print(f"Nessuna membership trovata per l'utente con ID {user_id}")
        return

    memberships_info = []

    # Stampa le informazioni delle membership
    for subscription in user_subscriptions:
        membership = subscription.membership
        icon = get_membership_icon(membership.name)
        memberships_info.append({
            "name": membership.name,
            "description": membership.description,
            "start_date": subscription.start_date.strftime("%Y-%m-%d"),
            "left_entrance": subscription.left_entrances,
            "end_date": subscription.end_date.strftime("%Y-%m-%d") if subscription.end_date else "Illimitato",
            "icon": icon
        })

    return memberships_info


# Funzione per ottenere tutte i corso disponibili per tipo di utente
def get_available_courses(user_id):
    user = User.query.get(user_id)
    if not user:
        print(f"Utente con ID {user_id} non trovato.")
        return []

    # Controllo le associazioni
    structure_ids = [subscription.structure_id for subscription in user.user_subscriptions if
                     subscription.structure_id]

    if not structure_ids:
        print(f"L'utente con ID {user_id} non è associato a nessuna struttura.")
        return []

    if user.role == 'user':
        # Cerco i corsi associati all'utente e alla struttura
        courses_in_structures = Course.query.filter(Course.structure_id.in_(structure_ids)).all()
        return courses_in_structures

    elif user.role == 'trainer':
        return Course.query.filter(Course.trainer_id.in_(user.id)).all()

    elif user.role == 'gym':
        structure = user.structure
        return Course.query.filter_by(structure_id=structure.id).all() if structure else []

    return Course.query.all()


# Funzione per ottenere tutte i corso disponibili per utente
def get_available_courses(user_id):
    # Controllo l'utente se esiste
    user = User.query.get(user_id)
    if not user:
        print(f"Utente con ID {user_id} non trovato.")
        return []

    # Controllo le associazioni
    structure_ids = [subscription.structure_id for subscription in user.user_subscriptions if subscription.structure_id]

    if not structure_ids:
        print(f"L'utente con ID {user_id} non è associato a nessuna struttura.")
        return []

    # Recupero i corsi associati all'utente e alla struttura
    courses_in_structures = (
        Course.query.filter(Course.structure_id.in_(structure_ids))
        .all()
    )

    return courses_in_structures


# Funzione per ottenere tutte le membership disponibili
def get_available_memberships():
    memberships = Membership.query.filter(
        Membership.is_active == True,
        ~Membership.name.ilike('%Unlimited%')
    ).all()
    memberships_info = []
    for membership in memberships:
        icon = get_membership_icon(membership.name)
        memberships_info.append({
            "name": membership.name,
            "description": membership.description,
            "price": f"{membership.price:.2f} €",
            "icon": icon
        })

    return memberships_info


# Funzione per ottenere icona in base al membership
def get_membership_icon(membership_name):
    if "Mensile" in membership_name:
        return "bi-calendar"
    elif "Trimestrale" in membership_name:
        return "bi-calendar3"
    elif "Annuale" in membership_name:
        return "bi-calendar4"
    elif "Ingressi" in membership_name:
        return "bi-ticket"
    else:
        return "bi-gem"


# Funzione per ottenere la struttura in base all'user_id
def get_user_structure(user_id):
    # Ottieni l'abbonamento dell'utente (order_by per ottenere il più recente)
    subscription = UserSubscription.query.filter_by(user_id=user_id).order_by(
        UserSubscription.start_date.desc()
    ).first()

    if subscription and subscription.structure:
        return subscription.structure

    return None


# Funzione per ottenere il corso in base al suo id
def get_course(course_id):
    if course_id:
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            print(f"Nessun corso trovato.")
        return course
    return None


# Defisco la route per la homepage - se autenticato va su profilo
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template("home.html")


# Route per la gestione del login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        messaggio_errore = "Username o password non validi"
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('profile'))
            else:
                flash(messaggio_errore, category='error')
        else:
            flash(messaggio_errore, category='error')

    return render_template("login.html", users=User.query.all())


# Route per il logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Route per la prenotazione
@app.route('/book/<int:course_id>/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def book(course_id, schedule_id):
    # Trova l'orario (schedule) selezionato
    selected_schedule = CourseSchedule.query.get_or_404(schedule_id)

    # Verifica se l'utente ha già una prenotazione per questo corso nello stesso giorno
    existing_booking = Booking.query.join(CourseSchedule).filter(
        Booking.user_id == current_user.id,
        Booking.course_id == course_id,
        CourseSchedule.start_date == selected_schedule.start_date
    ).first()

    if existing_booking:
        # L'utente ha già una prenotazione in quel giorno:
        if request.method == 'POST' and 'confirm' in request.form:
            # Cancello la vecchia prenotazione
            db.session.delete(existing_booking)

            # Creo la nuova prenotazione
            new_booking = Booking(
                course_id=course_id,
                schedule_id=schedule_id,
                user_id=current_user.id
            )
            db.session.add(new_booking)
            db.session.commit()

            flash('La tua prenotazione è stata modificata con successo!', 'success')
            return redirect(url_for('courses'))

        return render_template('confirm.html',
                               existing_booking=existing_booking,
                               new_schedule=selected_schedule,
                               action="book"
                               )

    # Se non c'è una prenotazione esistente per quel giorno, crea una nuova prenotazione
    if request.method == 'POST' and 'confirm' in request.form:
        new_booking = Booking(
            course_id=course_id,
            schedule_id=schedule_id,
            user_id=current_user.id
        )
        db.session.add(new_booking)

        # Aggiorna il numero di posti usati nello schedule
        selected_schedule.used += 1

        schedule = CourseSchedule.query.get(schedule_id)
        # Decrementa i posti utilizzati nello schedule
        if schedule.used > 0:
            schedule.used -= 1

        db.session.commit()

        flash('Prenotazione effettuata con successo!', 'success')
        return redirect(url_for('courses'))

    else:  # Mostra il messaggio di conferma
        course = Course.query.get_or_404(course_id)
        schedule = CourseSchedule.query.get_or_404(schedule_id)

        return render_template('confirm.html',
                               course=course,
                               schedule=schedule,
                               action="confirm"
                               )


# Route per la gestione dei corsi
@app.route("/courses")
@login_required
def courses():
    bookings = []
    available_courses = []

    # Filtra i corsi e le prenotazioni in base al ruolo dell'utente
    if current_user.role == 'admin':
        # Gli admin vedono tutti i corsi e prenotazioni
        bookings = Booking.query.all()
        available_courses = Course.query.all()

    elif current_user.role == 'trainer':
        # I trainer vedono solo i corsi dove sono assegnati come trainer
        bookings = Booking.query.join(Course).filter(Course.trainer_id == current_user.id).all()
        available_courses = Course.query.filter_by(trainer_id=current_user.id).all()

    elif current_user.role == 'gym':
        # I proprietari delle palestre vedono solo i corsi relativi alla loro struttura
        user_structure = get_user_structure(current_user.id)
        if user_structure:
            bookings = Booking.query.join(Course).filter(Course.structure_id == user_structure.id).all()
            available_courses = Course.query.filter_by(structure_id=user_structure.id).all()

    else:
        # Gli utenti normali vedono solo i corsi prenotati da loro
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        available_courses = get_available_courses(current_user.id)

    # Raggruppa le prenotazioni per corso
    course_bookings = defaultdict(list)
    for booking in bookings:
        course_bookings[booking.course].append(booking)

    if current_user.role == 'user':
        users = User.query.options(
            db.joinedload(User.bookings).joinedload(Booking.course).joinedload(Course.structure)
        ).filter_by(id=current_user.id).all()
    elif current_user.role == 'trainer':
        # I trainer vedono solo le prenotazioni dei corsi che insegnano
        users = User.query.options(
            db.joinedload(User.bookings).joinedload(Booking.course).joinedload(Course.structure)
        ).join(Booking.course).filter(Course.trainer_id == current_user.id).all()  # Filtra per l'ID del trainer loggato
    else:
        users = User.query.options(
            db.joinedload(User.bookings).joinedload(Booking.course).joinedload(Course.structure)
        ).all()

    # Passiamo il dizionario raggruppato al template
    return render_template("courses.html",
                           structure=get_user_structure(current_user.id),
                           available_courses=available_courses,
                           bookings=bookings,
                           users=users,
                           course_bookings=course_bookings
                           )


# Route per la visualizzazione di un singolo corso
@app.route("/course/<int:course_id>")
@login_required
def course(course_id):
    if current_user.role == 'trainer':
        flash("Non hai i permessi per visualizzare la pagina.", "warning")
        return redirect(url_for('courses'))

    course = get_course(course_id)
    user_structure = get_user_structure(current_user.id)

    if not user_structure or user_structure.id != course.structure_id:
        flash("Non sei autorizzato a visualizzare questo corso.", "danger")
        return redirect(url_for('courses'))

    user_bookings = Booking.query.filter_by(course_id=course_id, user_id=current_user.id).all()
    booked_schedule_ids = set([booking.schedule_id for booking in user_bookings])

    return render_template("detail.html",
                           course=course,
                           booked_schedule_ids=booked_schedule_ids)


# Route per la cancellazione di una prenotazione
@app.route("/cancel/<int:course_id>/<int:schedule_id>/<int:user_id>", methods=['GET', 'POST'])
@login_required
def cancel(course_id, schedule_id, user_id):
    if current_user.role == 'trainer':
        flash("Non hai i permessi per visualizzare la pagina.", "warning")
        return redirect(url_for('courses'))

    booking = Booking.query.filter_by(
        user_id=user_id,
        course_id=course_id,
        schedule_id=schedule_id
    ).first()

    if not booking:
        flash("Non hai prenotato questo corso per questo orario.", "warning")
        return redirect(url_for('courses'))

    schedule = CourseSchedule.query.get(schedule_id)
    if not schedule:
        flash("L'orario del corso non esiste.", "danger")
        return redirect(url_for('courses'))

    if booking:
        if request.method == 'POST' and 'confirm' in request.form:
            # Rimuovi la prenotazione dal database
            db.session.delete(booking)

            # Decrementa i posti utilizzati nello schedule
            if schedule.used > 0:
                schedule.used -= 1
            db.session.commit()

            flash("Prenotazione cancellata con successo.", "warning")
            return redirect(url_for('courses'))

        # Mostra il messaggio di conferma
        return render_template('confirm.html',
                               existing_booking=booking,
                               action="cancel"
                               )


# Route per il profilo utente (solo per utenti loggati)
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html",
                           user_memberships=get_user_memberships(current_user.id),
                           structure=get_user_structure(current_user.id),
                           memberships=get_available_memberships(),
                           bookings=get_booking_user(current_user.id),
                           )


# Route per visualizzare gli abbonamenti
@app.route("/subscriptions")
@login_required
def subscriptions():
    return render_template("subscriptions.html",
                           user_memberships=get_user_memberships(current_user.id),
                           structure=get_user_structure(current_user.id),
                           memberships=get_available_memberships()
                           )


# Route per visualizzare gli utenti (solo admin)
@app.route("/users")
@login_required
def users():
    if current_user.role != 'admin':
        flash("Non hai i permessi per accedere a questa pagina.", "danger")
        return redirect(url_for('index'))

    users = User.query.options(
        db.joinedload(User.bookings).joinedload(Booking.course).joinedload(Course.structure),
        db.joinedload(User.user_subscriptions).joinedload(UserSubscription.structure)
    ).filter(or_(User.role == 'user', User.role == 'trainer')).all()

    return render_template('users.html', users=users)


# Route per visualizzare le strutture (solo admin)
@app.route("/structures")
@login_required
def structures():
    if current_user.role != 'admin':
        flash("Non hai i permessi per accedere a questa pagina.", "danger")
        return redirect(url_for('index'))

    users = User.query.options(
        db.joinedload(User.bookings).joinedload(Booking.course).joinedload(Course.structure),
        db.joinedload(User.user_subscriptions).joinedload(UserSubscription.structure)
    ).filter_by(role='gym').all()

    return render_template('users.html', structures=True, users=users)


# Gestisce la pagina di errore 404
@app.errorhandler(404)
def not_found(error):
    return render_template("error_404.html"), 404


# Iserisco dati iniziali nel database
def seed_database():
    if User.query.count() == 0:
        print('## Aggiungo dati al database per la demo')
        seed_users()
        seed_memberships()
        seed_structures()
        seed_courses_and_schedules_and_bookings()
        seed_user_subscriptions()
        seed_course_schedules()
        seed_bookings()


# Inserisco le prenotazioni iniziali nel database
def seed_bookings():
    bookings = [{"user_id": 2, "course_id": 9, "schedule_id": 338}, {"user_id": 2, "course_id": 10, "schedule_id": 507}]

    for booking in bookings:
        new_booking = Booking(**booking)
        db.session.add(new_booking)
        db.session.commit()


# Inserisco le fasce orarie disponibli per i corsi in maniera casuale
def seed_course_schedules():
    courses = Course.query.all()

    # Fasce orarie possibili per i corsi: 9:00, 11:00, 13:00, 15:00, 17:00, 19:00
    possible_times = [time(9, 0), time(11, 0), time(13, 0), time(15, 0), time(17, 0), time(19, 0)]

    for course in courses:
        for day_offset in range(14):  # Per i prossimi 14 giorni
            # Genera una data per ogni giorno delle prossime 2 settimane
            schedule_date = date.today() + timedelta(days=day_offset)

            # Seleziona due orari casuali tra le fasce orarie disponibili
            schedule_times = random.sample(possible_times, 4)

            # Creazione dei due orari per il giorno specifico
            # Capacità casuale tra 2 e 15 posti
            # Durata casuale tra 30, 45 e 60 minuti
            schedule1 = CourseSchedule(
                course_id=course.id,
                start_date=schedule_date,
                start_time=schedule_times[0],
                duration=random.choice([30, 45, 60]),
                capacity=random.randint(2, 15),
                used=0
            )
            schedule2 = CourseSchedule(
                course_id=course.id,
                start_date=schedule_date,
                start_time=schedule_times[1],
                duration=random.choice([30, 45, 60]),
                capacity=random.randint(2, 15),
                used=0
            )
            schedule3 = CourseSchedule(
                course_id=course.id,
                start_date=schedule_date,
                start_time=schedule_times[2],
                duration=random.choice([30, 45, 60]),
                capacity=random.randint(2, 15),
                used=0
            )

            db.session.add(schedule1)
            db.session.add(schedule2)
            db.session.add(schedule3)
    db.session.commit()


# Inserisco corsi e schedule di esempio nel database
def seed_courses_and_schedules_and_bookings():
    structures = Structure.query.all()
    trainers = User.query.filter_by(role="trainer").all()

    for structure in structures:
        for _ in seeded_courses:
            c = random.choice(seeded_courses)
            trainer = random.choice(trainers)

            # Controlla se esiste già un corso con lo stesso nome
            existing_course = Course.query.filter_by(name=c["name"], structure_id=structure.id).first()

            if not existing_course:
                new_course = Course(
                    name=c["name"],
                    description=c["description"],
                    trainer_id=trainer.id,
                    structure_id=structure.id,
                    logo=c["logo"]
                )
                db.session.add(new_course)
                db.session.commit()
                print(f"Corso {new_course.name} aggiunto per la struttura {structure.name} con trainer {trainer.name}.")

    print("Corsi di esempio aggiunti con successo.")


# Inserisco utenti di prova nel database
def seed_users():
    for user in seeded_users:
        # Constrollo se gli utenti non esistono nel database prima di inserirli
        if not User.query.filter_by(username=user["username"]).first():
            new_user = User(
                username=user["username"],
                password=user["password"],
                email=user["email"],
                name=user["name"],
                last_name=user["last_name"],
                notes=user["notes"],
                role=user["role"]
            )

            db.session.add(new_user)
            db.session.commit()
            print(f"User {new_user.username} aggiunto.")


# Inserisco strutture di prova nel database
def seed_structures():
    for structure in seeded_structures:
        if not Structure.query.filter_by(name=structure["name"]).first():
            new_structure = Structure(
                name=structure["name"],
                address=structure["address"],
                phone=structure["phone"],
                email=structure["email"],
                website=structure["website"],
                logo=structure["logo"],
            )
            db.session.add(new_structure)
            db.session.commit()
            print(f"Struttura {new_structure.name} aggiunta.")


# Inserisco membership di prova nel database
def seed_memberships():
    for membership in seeded_memberships:
        # Controllo se le membership non esistono nel database prima di inserirli
        if not Membership.query.filter_by(name=membership["name"]).first():
            new_membership = Membership(
                name=membership["name"],
                description=membership["description"],
                price=membership["price"],
                entrances=membership.get("entrances", 0),
            )
            db.session.add(new_membership)
            db.session.commit()
            print(f"Membership {membership['name']} aggiunta.")


# Inserisco sottoscrizioni di prova nel database
def seed_user_subscriptions():
    users = User.query.all()
    memberships = Membership.query.all()
    structures = Structure.query.all()
    if not users or not memberships:
        print("Controllo di avere utenti e membership nel database prima di creare le associazioni.")
        return

    # Esempi di sottoscrizioni, con date casuali
    subscriptions = [
        {
            "user_id": users[0].id,  # admin
            "subscription_id": memberships[5].id,  # unlimited
            "structure_id": structures[1].id,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": None
        },
        {
            "user_id": users[1].id,
            "subscription_id": memberships[1].id,
            "structure_id": structures[1].id,
            "start_date": datetime.now() - timedelta(days=15),
            "end_date": datetime.now() + timedelta(days=75)
        },
        {
            "user_id": users[2].id,  # ingressi
            "subscription_id": memberships[4].id,  # 20 ingressi
            "structure_id": structures[0].id,
            "start_date": datetime.now() - timedelta(days=60),
            "left_entrance": 18,
            "end_date": None
        },
        {
            "user_id": users[3].id,  # trainer
            "subscription_id": memberships[5].id,  # unlimited
            "structure_id": structures[2].id,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": None
        },
        {
            "user_id": users[4].id,  # trainer
            "subscription_id": memberships[5].id,  # unlimited
            "structure_id": structures[1].id,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": None
        },
        {
            "user_id": users[5].id,  # gym
            "subscription_id": memberships[5].id,  # unlimited
            "structure_id": structures[0].id,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": None
        },
        {
            "user_id": users[6].id,  # gym
            "subscription_id": memberships[5].id,  # unlimited
            "structure_id": structures[1].id,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": None
        }
    ]

    for subscription in subscriptions:
        if not UserSubscription.query.filter_by(user_id=subscription["user_id"],
                                                subscription_id=subscription["subscription_id"]).first():
            new_subscription = UserSubscription(
                user_id=subscription["user_id"],
                subscription_id=subscription["subscription_id"],
                structure_id=subscription["structure_id"],
                left_entrances=subscription.get("left_entrance", 0),
                start_date=subscription["start_date"],
                end_date=subscription["end_date"]
            )
            db.session.add(new_subscription)
            db.session.commit()
            print(
                f"Associo "
                f"la Membership {Membership.query.filter_by(id=subscription['subscription_id']).first().name} "
                f"la Structure {Structure.query.filter_by(id=subscription['structure_id']).first().name} "
                f"a {User.query.filter_by(id=subscription['user_id']).first().username} ")


# Avvio GymCourses con Flask e controllo esistenza DB all'avvio
if __name__ == "__main__":
    with app.app_context():
        if not path.exists('instance/gymcourses.db'):
            print('######################    SEEDERS RICHIESTI PER LA DEMO  ########################\n'
                  '# Per favore esegui il seguente comando per continuare:                         #\n'
                  '# >>>  python seeders.py                                                        #\n'
                  '#################################################################################')
        else:
            db.init_app(app)
            # Eseguo l'applicazione in modalità debug
            app.run(debug=True, port=5000)
