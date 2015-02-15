__author__ = 'davide'

import hashlib as hl
from check_new import get_hash, get_sess_id

u = b"glennhk"
p = b"55thginkyloH"[::-1]
sess_id = b"88bee7270723b77b21adcc00ad83cf2e"
exp = b"99f4e5eeff4fe78083d9213737d0aec15d353156"

def hashTest():
    m = get_hash(u, p, sess_id).encode()
    print(m)
    print(exp)
    assert m == exp
