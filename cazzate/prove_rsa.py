__author__ = 'Davide'

import rsa

if __name__ == "__main__":
    pbk, prk = rsa.newkeys(128)
    msg = b"a" * 5
    print(msg)
    encoded = rsa.encrypt(msg, pbk)
    print(encoded)
    decoded = rsa.decrypt(encoded, prk)
    print(decoded)

    print(list(msg))
    print(pbk)
    print(prk)
    print(list(encoded))