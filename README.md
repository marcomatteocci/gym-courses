
# GymCourses - Rivoluziona il tuo allenamento in palestra

**GymCourses** è un'applicazione web progettata per aiutare le palestre a gestire e pianificare corsi, prenotazioni e abbonamenti. Consente agli utenti di prenotare slot di corsi disponibili, gestire le proprie prenotazioni e visualizzare informazioni dettagliate sui corsi e sugli orari.

## Funzionalità

- **Autenticazione utenti**: Login sicuro e gestione del profilo per i membri della palestra.
- **Gestione corsi**: Visualizzazione dei corsi disponibili con date e fasce orarie.
- **Sistema di prenotazione**: Prenotazione e gestione degli slot di corso, con risoluzione automatica dei conflitti di prenotazione giornaliera.
- **Pannello amministrativo**: Gestione di utenti, abbonamenti e dettagli dei corsi.
- **Conferme modali**: Conferma delle modifiche o cancellazioni delle prenotazioni prima di finalizzare le azioni.

## Struttura del progetto

```bash
gymCourses/
├── gymcourses.py              # File principale dell'applicazione Flask
├── instance/                  # Cartella temporanea (generato automaticamente)
│   └── gymcourses.db          # Database SQLite (generato automaticamente)
├── requirements.txt           # Elenco delle dipendenze del progetto
├── gym-courses-env            # Ambiente virtuale (creato con venv)
├── templates/                 # Cartella dei template HTML da renderizzare
│   ├── base.html              # Template base da cui estendo gli altri template
│   ├── confirm.html           # Pagina di conferma azioni
│   ├── courses.html           # Pagina con la lista dei corsi disponibili
│   ├── detail.html            # Pagina dettagli del corso scelto
│   ├── error_404.html         # Pagina di errore 404
│   ├── home.html              # Pagina iniziale dell'applicazione
│   ├── login.html             # Pagina di login per gli utenti
│   ├── profile.html           # Pagina profilo utente
│   ├── subscriptions.html     # Pagina che mostra l'abbonamento attivo 
│   └── users.html             # Pagina per la gestione utenti (solo per admin)
└─ static/                     # Cartella per i file statici (CSS e JS)
    ├── css/                   # Cartella CSS
    │   └── styles.css         # Fogli di stile CSS del progetto
    └── js/                    # Cartella JS
        └── scripts.js         # Codice JavaScript personalizzato
```

## Installazione e primo avvio

Per eseguire il progetto in locale, segui questi passaggi:

1. **Clona il repository**:
   ```bash
   git clone https://github.com/marcomatteocci/gym-courses.git
   cd gym-courses
   ```

2. **Crea un ambiente virtuale** (opzionale ma consigliato):
   ```bash
   python -m venv gym-courses-env
   source gym-courses-env/bin/activate  # Su Windows: gym-courses-env\Scripts\activate
   ```

3. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura il database**:
- Esegui il seeder per popolare il database con dati di esempio:
     ```bash
   python seeders.py
     ```

5. **Esegui l'applicazione**:
   ```bash
   python gymcourses.py
   ```

6. Apri il browser e naviga su `http://127.0.0.1:5000`.

## Tecnologie usate

- **Backend**: Python 3.10, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap, JavaScript (template Jinja)
- **Database**: SQLite (per sviluppo locale) / PostgreSQL (per rilascio in produzione)
