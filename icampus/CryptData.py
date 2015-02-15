import getpass

__author__ = 'davide'


def cipher(login, pw, dest, key):
    login_b = login.encode()
    pw_b = bytes(((c + key) % 256) for c in pw.encode())

    with open(dest, "wb") as f:
        f.write(login_b)
        f.write(b'\0')
        f.write(pw_b)


def decipher(src, key):
    with open(src, "rb") as f:
        s = f.read()
    login, pw = s.decode().split('\0')
    pw = "".join(map(chr, (((c - key + 256) % 256) for c in pw.encode())))
    return login, pw

if __name__ == "__main__":
    f = input("File>")
    login = input("Nome utente>")
    pw = getpass.getpass("Password>")
    key = int(input("Key>"))
    cipher(login, pw, f, key)
    print("Cifratura effettuata con successo!")
