from os import path
from gymcourses import app, seed_database
from db import db

# Creo la struttura DB e dati iniziali
def create_database():
    if not path.exists('instance/gymcourses.db'):
        print('##### Creo database iniziale #####')
        db.create_all()
        seed_database()


# Avvio GymCourses con Flask e creo DB all'avvio
if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        create_database()
