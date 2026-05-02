import bcrypt

# Funzione per cifrare la password.
def encrypt_password(password):
    """
    Cifra una password usando l'algoritmo bcrypt.
    :param password: La password in chiaro.
    :return: La password criptata (bytes).
    """
    # bcrypt genera un salt casuale e lo include nell'hash per sicurezza.
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

# Funzione per verificare la password.
def verify_password(password, hashed_password):
    """
    Verifica se la password in chiaro corrisponde a quella criptata.
    :param password: La password in chiaro inserita.
    :param hashed_password: La password criptata salvata nel database.
    :return: True se le password corrispondono, False altrimenti.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
