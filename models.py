# Importo i moduli necessari al funzionamento dei modelli
from datetime import datetime
from flask_login import UserMixin
from db import db


# Definisco la classe User che estende UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    notes = db.Column(db.Text, nullable=True)
    role = db.Column(db.Enum('user', 'trainer', 'gym', 'admin'), default='user')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    # Costruttore User
    def __init__(self, username, password, email, name, last_name, is_active=True, notes=None, role='user'):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.last_name = last_name
        self.is_active = is_active
        self.notes = notes
        self.role = role


    # Funzione toString
    def __str__(self):
        return f"ID={self.id}, First Name={self.name}, Last Name={self.last_name}, Email={self.email}, Role={self.role}"


# Definisco la classe Membership
class Membership(db.Model):
    __tablename__ = 'memberships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    entrances = db.Column(db.Integer, nullable=True, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    # Costruttore Membership
    def __init__(self, name, description, price, entrances, is_active=True):
        self.name = name
        self.description = description
        self.price = price
        self.entrances = entrances
        self.is_active = is_active


# Definisco la classe UserSubscription
class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('memberships.id'), nullable=False)
    structure_id = db.Column(db.Integer, db.ForeignKey('structures.id'), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True, default=None)
    left_entrances = db.Column(db.Integer, nullable=True, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    # Relazioni tra modelli
    membership = db.relationship("Membership", backref="membership_subscriptions", lazy=True)
    user = db.relationship("User", backref="user_subscriptions", lazy=True)
    structure = db.relationship("Structure", back_populates="user_subscriptions", lazy=True)


    # Costruttore UserSubscription
    def __init__(self, user_id, subscription_id, structure_id=None, start_date=None, end_date=None, left_entrances=0):
        self.user_id = user_id
        self.subscription_id = subscription_id
        self.structure_id = structure_id
        self.start_date = start_date
        self.end_date = end_date
        self.left_entrances = left_entrances


# Definisco la classe Structure
class Structure(db.Model):
    __tablename__ = 'structures'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relazioni tra modelli
    user_subscriptions = db.relationship('UserSubscription', back_populates='structure', lazy=True)


    # Costruttore Structure
    def __init__(self, name, address=None, phone=None, email=None, website=None, logo=None):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.website = website
        self.logo = logo


    # Funzione toString
    def __str__(self):
        return f"Struttura: {self.name}, Indirizzo: {self.address}, Email: {self.email}"


# Definisco la classe Course
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    structure_id = db.Column(db.Integer, db.ForeignKey('structures.id'), nullable=False)


    # Relazioni tra modelli
    trainer = db.relationship('User', backref='courses')
    structure = db.relationship('Structure', backref='courses')
    schedules = db.relationship('CourseSchedule', back_populates='course', lazy=True)  # Aggiungi la relazione
    bookings = db.relationship('Booking', back_populates='course', lazy=True)


    # Costruttore Course
    def __init__(self, name, description, logo, trainer_id, structure_id):
        self.name = name
        self.description = description
        self.logo = logo
        self.trainer_id = trainer_id
        self.structure_id = structure_id


    # Funzione toString
    def __str__(self):
        return f"Corso: {self.name}, Descrizione: {self.description}, Logo: {self.logo}, Trainer: {self.trainer.name}"


    # Funzione per rappresentare il corso
    def __repr__(self):
        return f'<Corso {self.name}>'


# Definisco la classe CourseSchedule
class CourseSchedule(db.Model):
    __tablename__ = 'course_schedules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=30)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    used = db.Column(db.Integer, nullable=False, default=0)


    # Relazioni tra modelli
    course = db.relationship('Course', back_populates='schedules')
    bookings = db.relationship('Booking', back_populates='schedule', lazy=True)


    # Costruttore CourseSchedule
    def __init__(self, course_id, start_date, start_time, duration, capacity, used=0):
        self.course_id = course_id
        self.start_date = start_date
        self.start_time = start_time
        self.duration = duration
        self.capacity = capacity
        self.used = used


    # Funzione toString per il corso
    def __str__(self):
        return f"Corso: {self.course.name}, Data: {self.start_date}, Ora: {self.start_time}"


    # Funzione per rappresentare il corso
    def __repr__(self):
        return f'<CourseSchedule {self.start_date} {self.start_time}>'


# Definisco la classe Booking
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('course_schedules.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relazioni tra modelli
    course = db.relationship('Course', back_populates='bookings')
    schedule = db.relationship('CourseSchedule', back_populates='bookings', lazy=True)
    user = db.relationship('User', backref='bookings', lazy=True)

    # Costruttore Booking
    def __init__(self, course_id, user_id, schedule_id):
        self.course_id = course_id
        self.user_id = user_id
        self.schedule_id = schedule_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # Funzione toString
    def __str__(self):
        return f"Corso: {self.course.name}, Utente: {self.user.name}, Data: {self.schedule.start_date}, Ora: {self.schedule.start_time}"

    # Funzione per rappresentare il corso
    def __repr__(self):
        return f'<Booking User:{self.user_id} Course:{self.course_id} Schedule:{self.schedule_id}>'
