# Importo la libreria Werkzeug per la generazione di password
from werkzeug.security import generate_password_hash

seeded_bookings = [{"user_id": 2, "course_id": 9, "schedule_id": 338},
                   {"user_id": 2, "course_id": 10, "schedule_id": 507}]
seeded_users = [
    {
        "username": "admin",
        "password": generate_password_hash("admin", method='pbkdf2:sha256', salt_length=16),
        "email": "admin@gymcourses.com",
        "name": "Marco",
        "last_name": "GymCourses",
        "notes": "Utente amministratore",
        "role": "admin"
    },
    {
        "username": "demo_user",
        "password": generate_password_hash("demo_user", method='pbkdf2:sha256', salt_length=16),
        "email": "demo_user@gymcourses.com",
        "name": "Marco",
        "last_name": "Matteocci",
        "notes": "Utente standard con corsi prenotati",
        "role": "user"
    },
    {
        "username": "demo_user_ingressi",
        "password": generate_password_hash("demo_user_ingressi", method='pbkdf2:sha256', salt_length=16),
        "email": "demo_user_ingressi@gymcourses.com",
        "name": "Demo",
        "last_name": "User Ingressi",
        "notes": "Utente demo con abbonamento a ingressi",
        "role": "user"
    },
    {
        "username": "trainer_beatrice",
        "password": generate_password_hash("trainer_beatrice", method='pbkdf2:sha256', salt_length=16),
        "email": "trainer_beatrice@gymcourses.com",
        "name": "Beatrice",
        "last_name": "Trainer",
        "notes": "Trainer che vede i propri corsi",
        "role": "trainer"
    },
    {
        "username": "trainer_leonardo",
        "password": generate_password_hash("trainer_leonardo", method='pbkdf2:sha256', salt_length=16),
        "email": "trainer_leonardo@gymcourses.com",
        "name": "Leonardo",
        "last_name": "Trainer",
        "notes": "Trainer che vede i propri corsi",
        "role": "trainer"
    },
    {
        "username": "gym_gioia",
        "password": generate_password_hash("gym_gioia", method='pbkdf2:sha256', salt_length=16),
        "email": "gym_gioia@gymcourses.com",
        "name": "Gym Gioia",
        "last_name": None,
        "notes": "Profilo palestra che gestisce gli iscritti",
        "role": "gym"
    },
    {
        "username": "gym_fit_point",
        "password": generate_password_hash("gym_fit_point", method='pbkdf2:sha256', salt_length=16),
        "email": "gym_fit_point@gymcourses.com",
        "name": "Gym Fit Point",
        "last_name": None,
        "notes": "Profilo palestra che gestisce gli iscritti",
        "role": "gym"
    }
]

seeded_structures = [
    {
        "name": "Gym Gioia",
        "phone": "+3912341234",
        "email": "gym.gioia@gmail.com",
        "website": "https://www.passionfitness.it",
        "address": "Via di test - Perugia (PG)",
        "logo": "bi-person-arms-up",
    },
    {
        "name": "Gym Fit Point",
        "phone": "+39399341234",
        "email": "gym.fit.point@gmail.com",
        "website": "https://www.fitpoint.it",
        "address": "Via di test - Rieti (RI)",
        "logo": "bi-person-arms-up",
    },
    {
        "name": "Gym Easy",
        "phone": "+39399341456",
        "email": "gym.easy@gmail.com",
        "website": "https://www.easyfitness.it",
        "address": "Via di test - Roma (RM)",
        "logo": "bi-person-arms-up",
    }
]

seeded_memberships = [
    {
        "name": "Mensile",
        "description": "Accesso illimitato alla palestra per 30 giorni. Ideale per chi vuole provare i nostri servizi senza impegni a lungo termine.",
        "price": 49.99,
    },
    {
        "name": "Trimestrale",
        "description": "Accesso illimitato per 3 mesi consecutivi con uno sconto sul prezzo mensile. Perfetto per chi vuole allenarsi regolarmente.",
        "price": 129.99,
    },
    {
        "name": "Annuale",
        "description": "La nostra membership più conveniente. Allenati tutto l'anno con accesso illimitato e vantaggi esclusivi come lezioni personalizzate gratuite.",
        "price": 499.99,
    },
    {
        "name": "10 Ingressi",
        "description": "Perfetto per chi vuole flessibilità senza abbonamento. 10 ingressi validi per 6 mesi, utilizzabili in qualsiasi momento.",
        "price": 89.99,
        "entrances": 10
    },
    {
        "name": "20 Ingressi",
        "description": "Un pacchetto conveniente per chi frequenta regolarmente. 20 ingressi validi per 12 mesi.",
        "price": 149.99,
        "entrances": 20
    },
    {
        "name": "Unlimited",
        "description": "Accesso illimitato agli Admins e Trainers.",
        "price": 0,
        "entrances": 0
    }
]

seeded_courses = [
    {
        "name": "Yoga",
        "description": "Un'attività che unisce respirazione e movimenti per migliorare flessibilità e rilassarsi.",
        "logo": "bi-person-standing"
    },
    {
        "name": "Pilates",
        "description": "Esercizi per postura, flessibilità e forza muscolare, con movimenti controllati.",
        "logo": "bi-activity"
    },
    {
        "name": "Spinning",
        "description": "Allenamento cardio su bici stazionaria, ideale per bruciare calorie velocemente.",
        "logo": "bi-bicycle"
    },
    {
        "name": "Zumba",
        "description": "Danza e fitness su ritmi latini, divertente e perfetto per bruciare calorie.",
        "logo": "bi-music-note-beamed"
    },
    {
        "name": "CrossFit",
        "description": "Allenamento funzionale ad alta intensità che combina pesi, cardio e ginnastica.",
        "logo": "bi-lightning"
    },
    {
        "name": "Kickboxing",
        "description": "Arte marziale che combina calci e pugni, migliorando resistenza e coordinazione.",
        "logo": "bi-hand-thumbs-up"
    },
    {
        "name": "Aerobica",
        "description": "Allenamento di gruppo cardio con musica, perfetto per migliorare la resistenza.",
        "logo": "bi-chevron-contract"
    },
    {
        "name": "Danza a corpo libero",
        "description": "Fitness e danza su ritmi latini per tonificare e divertirsi.",
        "logo": "bi-music-note-list"
    },
    {
        "name": "Stretching",
        "description": "Attività per aumentare flessibilità e prevenire infortuni tramite l'allungamento muscolare.",
        "logo": "bi-arrows-move"
    },
    {
        "name": "GAG",
        "description": "Allenamento mirato per rafforzare gambe, addominali e glutei.",
        "logo": "bi-bullseye"
    },
    {
        "name": "Salsa Fitness",
        "description": "Allenamento che combina i movimenti della salsa con esercizi di fitness.",
        "logo": "bi-music-note-list"
    }
]
