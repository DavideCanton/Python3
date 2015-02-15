def oracle_max_master(in_neighbors_roles):
    """
    Restituisce 1 se l'utente ha come maggioranza
    di certificati il valore 1 (ovvero master).

    @param in_neighbors_roles: un Counter che contiene
    per ogni tipo di certificato il numero di certificazioni
    ricevute dall'utente.

    Ad esempio, se l'utente u1 ha associato un Counter
    del tipo {"master":10, "journeyer":5, "apprentice":3, "observer":3}
    sara' certificato come master, per cui l'oracolo restituira' 1.
    """
    if in_neighbors_roles:
        role_max, _ = in_neighbors_roles.most_common(1)[0]
        if role_max == 1:
            return 1
    return 0


def oracle_max_master_or_journeyer(in_neighbors_roles):
    """
    Restituisce 1 se l'utente ha come maggioranza
    di certificati i valori 1 o 2 (ovvero master o journeyer).

    @param in_neighbors_roles: un Counter che contiene
    per ogni tipo di certificato il numero di certificazioni
    ricevute dall'utente.
    """
    if in_neighbors_roles:
        role_max, _ = in_neighbors_roles.most_common(1)[0]
        if role_max <= 2:
            return 1
    return 0


def get_mapping_user(mapping):
    """
    Carica il mapping utente-certificato.

    @param mapping: il percorso del file contenente il mapping,
    nel formato "utente certificato"

    I certificati sono stati codificati con interi:
    1-master, 2-journeyer, 3-apprentice, 4-observer
    """
    diz = {}
    with open(mapping, newline="") as mapp:
        for row in mapp:
            splitted = row.split()
            diz[int(splitted[0])] = int(splitted[1])
    return diz


def oracle_users_certifications_max_master(mapping, user):
    """
    Restituisce 1 se l'utente ha associato nel mapping un
    certificato master.
    Se l'utente non e' presente, restituisce 0.
    """
    return int(mapping.get(user, 10) == 1)


def oracle_users_certifications_max_master_or_journeyer(mapping, user):
    """
    Restituisce 1 se l'utente ha associato nel mapping un
    certificato master o journeyer.
    Se l'utente non e' presente, restituisce 0.
    """
    return int(mapping.get(user, 10) <= 2)
