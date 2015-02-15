import re
from collections import defaultdict
import datetime

def parse_next_user(in_file, row_buffer):
    """
    Lettura di in_file in blocchi contenenti informazioni sulle azioni 
    effettuate dall'utente j e dei suoi followers rispetto alle prime.
    Creazione inoltre di due strutture dati, post_info e interactions_info, 
    in cui vengono memorizzati  rispettivamente i dati riguardanti
    i post e le risposte dei followers.
    Il parametro row_buffer assumera' valore None quando si va a leggere
    per la prima volta il file, mentre successivamente conterra' 
    i dati riguardanti i post effettuati da un utente successivo da quello 
    corrispondente al blocco appena letto.
    """

    # Dizionario contenente le informazioni relative 
    # ai post creati da ogni utente, memorizzate 
    # nel seguente formato : {(userid, post_id):timestamp_post}
    posts_info = {}
    
    # Dizionario contenete le informazioni relative alle interazioni tra due utenti.
    # Formato:{(userid, follower_id, post_id): (timestamp_interaction, frequency)}
    interaction_info = defaultdict(list)
    
    # Effettuato quando si legge un blocco successivo al primo,
    # in quanto row_buffer conterra' i dati dei post a cui riferisce il blocco
    if row_buffer is not None:
        add_posts(posts_info, row_buffer)
    for row in in_file:
        # Salto le eventuali righe vuote e l'header
        if not row or not row[0].isdigit():
            continue
        # Suddivido ogni riga del file in una lista di token saltando i separatori
        tokens = re.split("[; ,]+", row)
        # Lettura della prima riga del blocco(escluso l'header) alla prima chiamata
        if row_buffer is None:
            row_buffer = tokens
        # Passaggio da blocco corrente al successivo
        # (l'utente a cui si fa riferimento per i post e' cambiato)
        elif row_buffer[0] != tokens[0]:
            row_buffer = tokens
            break
        if tokens[1] == "_":
            add_posts(posts_info, tokens)
        else:
            add_interaction(interaction_info, tokens)
    else:
        # Siamo alla fine del file
        row_buffer = []
    return posts_info, interaction_info, row_buffer


def grouper(iterable, n):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip(*args)

def add_posts(posts_info, tokens):
    """
    Metodo con cui si inseriscono i dati riguardanti i post 
    effettuati da userid in post_info
    """
    userid = tokens[0]
    for time, post_id, _ in grouper(tokens[2:], 3):
        # Suddivisione del timestamo in anno, mese, giorno
        t_tokens = map(int, time.split("-"))
        # creazione dell'oggetto data
        t_date = datetime.date(*t_tokens)
        posts_info[userid, post_id] = t_date
        
def add_interaction(interaction_info, tokens):
    """
    Metodo con cui si inseriscono i dati riguardanti
    le interazioni tra coppie di utenti
    """
    userid = tokens[0]
    follower_id = tokens[1]
    for time, post_id, freq in grouper(tokens[2:], 3):
        # Suddivisione del timestamo in anno, mese, giorno
        t_tokens = map(int, time.split("-"))
        # creazione dell'oggetto data
        t_date = datetime.date(*t_tokens)
        interaction_info[userid, follower_id].append((t_date, post_id, int(freq)))