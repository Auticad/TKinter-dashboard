import sqlite3
import datetime
from utils import encrypt_password

# Nome del file del database
DB_NAME = 'users.db'

# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Funzione per creare la tabella degli utenti
def create_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id_utente INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            eta INTEGER,
            data_di_nascita TEXT,
            data_di_registrazione TEXT,
            password TEXT NOT NULL
        )
    ''')
    conn.commit() # salvare in modo permanente
    conn.close()

# Funzione per controllare se un utente con lo stesso username o email esiste già
def user_exists(username, email, id_utente=None):
    conn = get_db_connection()
    c = conn.cursor()# creare un oggetto cursore che ti
    # fornisce tutti i metodi necessari per comunicare in modo efficace con il database
    
    if id_utente:
        # Controlla per la modifica (escludendo l'utente corrente)
        c.execute('''
            SELECT * FROM users WHERE (username = ? OR email = ?) AND id_utente != ?
        ''', (username, email, id_utente))
    else:
        # Controlla per la creazione di un nuovo utente
        c.execute('''
            SELECT * FROM users WHERE username = ? OR email = ?
        ''', (username, email))
    result = c.fetchone()
    conn.close()
    return result is not None

# Funzione per salvare un nuovo utente
def save_user(username, email, eta, data_di_nascita, password):
    if user_exists(username, email):
        return False, "Username o Email già in uso."
    
    conn = get_db_connection()
    c = conn.cursor()
    data_di_registrazione = datetime.date.today().isoformat()
    hashed_password = encrypt_password(password)

    c.execute('''
        INSERT INTO users (username, email, eta, data_di_nascita, data_di_registrazione, password)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, email, eta, data_di_nascita, data_di_registrazione, hashed_password))
    
    conn.commit()
    conn.close()
    return True, "Utente salvato con successo."

# Funzione per ottenere tutti gli utenti
def get_all_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall() # recupera tutte le righe del risultato della query e le restituisce come una lista di tuple o di oggetti.
    conn.close()
    return users

# Funzione per aggiornare un utente esistente
def update_user(id_utente, username, email, eta, data_di_nascita, password=None):
    if user_exists(username, email, id_utente):
        return False, "Username o Email già in uso."

    conn = get_db_connection()
    c = conn.cursor()
    
    # Se una nuova password è fornita, criptala e aggiorna il campo password.
    if password:
        hashed_password = encrypt_password(password)
        c.execute('''
            UPDATE users SET username = ?, email = ?, eta = ?, data_di_nascita = ?, password = ?
            WHERE id_utente = ?
        ''', (username, email, eta, data_di_nascita, hashed_password, id_utente))
    else:
        # Altrimenti, aggiorna senza cambiare la password.
        c.execute('''
            UPDATE users SET username = ?, email = ?, eta = ?, data_di_nascita = ?
            WHERE id_utente = ?
        ''', (username, email, eta, data_di_nascita, id_utente))
    
    conn.commit()
    conn.close()
    return True, "Utente aggiornato con successo."

# Funzione per eliminare un utente
def delete_user(id_utente):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id_utente = ?', (id_utente,))
    conn.commit()
    conn.close()
