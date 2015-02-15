import csv
from operator import itemgetter
import numpy as np
import itertools as it
from collections import defaultdict, Counter
from scipy.sparse import dok_matrix
from scipy.sparse.sparsetools import csr_scale_columns

try:
    import oracle
except ImportError:
    from trustRank import oracle


def parser_file(file_in_path):
    """
    Fa il parsing del file in input, contenente il grafo
    di advogato nel formato "source;target;role".

    Restituisce:
    - la matrice T (di adiacenza trasposta) normalizzata
    - la matrice U (di adiacenza) normalizzata
    - la dimensione delle matrici
    - il dizionario contenente per ogni utente gli in-neighbors
    - il vettore che associa ad ogni utente il suo out-degree
    """

    with open(file_in_path, "r", newline="") as in_file:
        reader = csv.reader(in_file, delimiter=";")

        # Salta la riga corrsipondente all'header del file
        iter_reader = iter(reader)
        next(iter_reader)

        # Sovradimensiono la matrice
        dim = 700000
        U = dok_matrix((dim, dim))
        T = dok_matrix((dim, dim))

        # Lettura file
        dim = 0
        in_neighbors_role = defaultdict(Counter)
        for row in iter_reader:
            if len(row) != 0:
                source, target, role = map(int, row)
                dim = max(dim, source, target)
                U[source, target] = 1.
                T[target, source] = 1.
                in_neighbors_role[target][role] += 1

        # conversione in matrice CSR
        dim += 1
        U = U.tocsr()[:dim, :dim]
        T = T.tocsr()[:dim, :dim]

        # normalizzo U per colonna
        in_degree = U.sum(axis=0)
        in_degree[in_degree == 0] = 1
        in_degree = 1.0 / in_degree
        in_degree = np.array(in_degree)[0]

        csr_scale_columns(U.shape[0], U.shape[1], U.indptr,
                          U.indices, U.data, in_degree)

        # normalizzo T per colonna
        out_degree = T.sum(axis=0)
        out_degree = np.array(out_degree)[0]
        out_degree_copy = out_degree.copy()
        out_degree_copy[out_degree_copy == 0] = 1
        out_degree_copy = 1.0 / out_degree_copy

        csr_scale_columns(T.shape[0], T.shape[1], T.indptr,
                          T.indices, T.data, out_degree_copy)

    return T, U, dim, in_neighbors_role, out_degree


def select_seed_inv_pr(U, n, decay_factor, num_interations=-1):
    """
    Metodo per selezionare il seed set con l'algoritmo dell'inverse PageRank.

    @param U: la matrice di adiacenza trasposta.
    @param n: il numero di utenti.
    @param decay_factor: parametro del PageRank.
    @param num_interations: Numero di iterazioni (o -1 per andare a convergenza).

    @return: il vettore rappresentante il punteggio di PageRank inverso e il numero di iterazioni.
    """
    inv_pr = np.ones(n)
    it_counts = it.count(1) if num_interations == -1 else range(1, num_interations + 1)
    for cur_iteration in it_counts:
        inv_pr_pre = inv_pr
        inv_pr = decay_factor * U.dot(inv_pr) + (1 - decay_factor) / n
        if np.allclose(inv_pr, inv_pr_pre):
            break
        if cur_iteration % 10 == 0:
            print("Inverse PR: iterazione", cur_iteration)
    return inv_pr, cur_iteration


def select_seed_degree_ratio(in_degree, out_degree):
    """
    Metodo per selezione il seed set tenendo conto il rapporto dell'in-degree e dell'out-degree.

    @param in_degree: dizionario utente-counter dei ruoli.
    @param out_degree: vettore contenente gli out_degree degli utenti.

    @return: il vettore dei punteggi, e il numero di iterazioni (0 in questo caso).
    """
    scores = 1.0 / (out_degree + 1)
    for user, roles in in_degree.items():
        # sum(roles.values()) e' l'in-degree del nodo
        scores[user] *= sum(roles.values()) + 1
    return scores, 0


def rank(scores):
    """
    Riceve scores (calcolati con l'inv. PR o con il degree_ratio) e restituisce
    una permutazione degli interi 0..|scores|-1 ordinata in base agli scores.
    @param scores: il vettore dei punteggi
    @return: una lista di interi da 0 a |scores|-1 ordinata
    """
    return [pair[0] for pair in sorted(list(enumerate(scores)), key=itemgetter(1),
                                       reverse=True)]


def get_oracle_result(sigma, limit_oracle, oracle_type, in_neighbors_roles=None, mapping=None):
    """
    Invoca l'oracolo sui primi limit_oracle utenti contenuti in sigma.

    @param sigma: la permutazione degli utenti ordinata per scores.
    @param limit_oracle: il numero di chiamate dell'oracolo.
    @param oracle_type: "m", "mj", "um" o "umj".
    @param in_neighbors_roles: dizionario utente-counter dei ruoli assegnatigli dagli in-neighbor (ignorato se non
           serve).
    @param mapping: il mapping utente-certificato (ignorato se non serve).
    @return: gli indici degli utenti "good" in sigma.
    """
    if oracle_type in ("m", "mj"):
        ofun = oracle.oracle_max_master if oracle_type == "m" else oracle.oracle_max_master_or_journeyer
        oracle_vec = np.frompyfunc(ofun, 1, 1)
        indexes = np.where(oracle_vec([in_neighbors_roles[user] for user in sigma[:limit_oracle]]))[0]
    elif oracle_type in ("um", "umj"):
        ofun = (oracle.oracle_users_certifications_max_master if oracle_type == "um"
                else oracle.oracle_users_certifications_max_master_or_journeyer)
        mapping_users_cert = oracle.get_mapping_user(mapping)
        oracle_vec = np.frompyfunc(ofun, 2, 1)
        indexes = np.where(oracle_vec(mapping_users_cert, sigma[:limit_oracle]))[0]
    else:
        raise ValueError("oracolo non valido: {}".format(oracle_type))

    return indexes


def compute_initial_vector(U, decay_factor_u, num_interations_u, num_users, limit_oracle, in_neighbors_roles,
                           out_degree, select_mode, oracle_type, mapping=None):
    """
    Calcola il vettore iniziale del TrustRank.

    @param U: la matrice di adiacenza normalizzata.
    @param decay_factor_u: parametro per l'inverse PR (ignorato se si usa degree_ratio).
    @param num_interations_u: numero di iterazioni dell'inv. PR (o -1 per la convergenza).
    @param num_users: numero di utenti.
    @param limit_oracle: numero di chiamate dell'oracolo (< N).
    @param in_neighbors_roles: dizionario utente-counter dei ruoli assegnatigli dagli in-neighbor.
    @param out_degree: vettore degli out-degree degli utenti.
    @param select_mode: "invPR" o "degree_ratio"
    @param oracle_type: "m", "mj", "um", "umj"
    @param mapping: il mapping utente-certificato (ignorato se non serve).
    @return: il punteggio iniziale del TrustRank, il numero di iterazioni
             e gli indici degli utenti "good" nel seed_set.
    """
    select_mode = select_mode.lower()
    if select_mode == "invpr":
        scores, it_select = select_seed_inv_pr(U, num_users, decay_factor_u, num_interations_u)
    elif select_mode == "degree_ratio":
        scores, it_select = select_seed_degree_ratio(in_neighbors_roles, out_degree)
    else:
        raise ValueError("Tipo di select non valida: {}".format(select_mode))
    sigma = np.array(rank(scores))
    indexes = get_oracle_result(sigma, limit_oracle, oracle_type, in_neighbors_roles, mapping)
    # compute score distribution and normalize
    d = np.zeros(num_users)
    d[sigma[indexes]] = 1
    d /= d.sum()
    return d, it_select, indexes


def compute_trustrank(T, U, num_users, limit_oracle, decay_factor_t,
                      decay_factor_u, num_interations_t, num_interations_u,
                      in_neighbors_roles, out_degree, select_mode, oracle_type, mapping):
    """
    Calcola il TrustRank.

    @param T: la matrice di adiacenza trasposta normalizzata.
    @param U: la matrice di adiacenza normalizzata.
    @param num_users: numero di utenti.
    @param limit_oracle: numero di chiamate dell'oracolo (< N).
    @param decay_factor_t: parametro per TrustRank.
    @param decay_factor_u: parametro per l'inverse PR (ignorato se si usa degree_ratio).
    @param num_interations_t: numero di iterazioni del TrustRank (o -1 per la convergenza).
    @param num_interations_u: numero di iterazioni dell'inv. PR (o -1 per la convergenza).
    @param in_neighbors_roles: dizionario utente-counter dei ruoli assegnatigli dagli in-neighbor.
    @param out_degree: vettore degli out-degree degli utenti.
    @param select_mode: "invPR" o "degree_ratio"
    @param oracle_type: "m", "mj", "um", "umj"
    @param mapping: il mapping utente-certificato (ignorato se non serve).
    @return: il vettore di TrustRank, il numero di iterazioni di TrustRank, il numero di iterazioni dell'inv. PR
             e gli indici degli utenti "good" nel seed_set.
    """
    score_distr, it_inv_pr, indexes = compute_initial_vector(U, decay_factor_u, num_interations_u,
                                                             num_users, limit_oracle,
                                                             in_neighbors_roles, out_degree,
                                                             select_mode, oracle_type, mapping)
    trust = score_distr
    it_counts = it.count(1) if num_interations_t == -1 else range(1, num_interations_t + 1)
    for cur_iteration in it_counts:
        trust_pre = trust
        trust = decay_factor_t * T.dot(trust) + (1 - decay_factor_t) * score_distr
        if np.allclose(trust, trust_pre):
            break
        if cur_iteration % 10 == 0:
            print("TrustRank: iterazione", cur_iteration)
    return trust, cur_iteration, it_inv_pr, indexes


def print_result(trust, out_file_path):
    """
    Stampa su file i risultati, sotto forma di coppie
    user_id;trust_value.

    @param trust: Il vettore contenente i valori di trust.
    @param out_file_path: Il percorso dove scrivere il file.
    """
    with open(out_file_path, "w") as out_file:
        out_file.write("User_id;trust_value\n")
        for user_id, trust_val in enumerate(trust):
            out_file.write("{};{}\n".format(user_id, trust_val))


if __name__ == '__main__':
    file_in_path = r"..."
    file_out_path = r"..."
    # utile solo se c'e' un file di mapping utente-certificato
    mapping_path = r"..."

    T, U, num_users, in_neighbors_role, out_degree = parser_file(file_in_path)

    print("Read file,", num_users, "users.")

    percent = .1  # percentuale di utenti nel seed set
    limit_oracle = int(num_users * percent)

    # specificare m se si vuole l'oracolo che da' 1 solo agli utenti con maggioranza di master
    # specificare mj se si vuole l'oracolo che da' 1 solo agli utenti con maggioranza di master o journeyer
    # specificare um se si vuole l'oracolo con file di mapping che da' 1 solo per i master
    # specificare umj se si vuole l'oracolo con file di mapping che da' 1 solo per i master o journeyer
    oracle_type = "umj"

    # specificare invpr se si vuole usare l'inverse PageRank
    # specificare degree_ratio se si vuole usare il degree_ratio
    select_mode = "degree_ratio"

    trust, it_tr, it_inv_pr, indexes = compute_trustrank(T, U, num_users, limit_oracle, .85, .85, -1, -1,
                                                         in_neighbors_role, out_degree, select_mode,
                                                         oracle_type, mapping_path)
    good = int(len(indexes))

    print("Writing trust values to", file_out_path)
    print_result(trust, file_out_path)

    print("Numero di iterazioni effettuate dal TrustRank:", it_tr)
    if select_mode == "invpr":
        print("Numero di iterazioni effettuate dall'inverse PR:", it_inv_pr)
    print("Numero di nodi good nel seed set:", good / limit_oracle * 100, "%")
    print("Numero di nodi bad nel seed set:", (1 - good / limit_oracle) * 100, "%")






