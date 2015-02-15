from ICampusHandler import *
from CryptData import decipher
import getpass
import sys


def printLine():
    print("*" * 80)


def printStatus(corsiList):
    if corsiList:
        printLine()
        print("Corsi a cui sei attualmente iscritto:\n")
        for c in corsiList:
            print(c)
        printLine()
    print("s) cerca corso")
    print("a) aggiungi corso")
    print("r) rimuovi corso")
    print("q) esci")
    printLine()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        data = decipher(sys.argv[1], int(sys.argv[2]))
        try:
            print("Connessione...")
            handler = ICampusHandler(data)
            print("Sei connesso come utente {}".format(data[0]))
        except ICampusLoginError:
            exit("I dati immessi non sono validi")
    else:
        while True:
            data = input("Nome utente>"), getpass.getpass("Password>")
            try:
                print("Connessione...")
                handler = ICampusHandler(data)
                print("Sei connesso come utente {}".format(data[0]))
                break
            except ICampusLoginError:
                print("I dati immessi non sono validi")
                s = input("Vuoi continuare?")
                if s.lower() != "s":
                    exit()
    del data  # remove login data from memory
    while True:
        printStatus(handler.getCorsi())
        while True:
            try:
                inputString = input("Scelta> ").split()
                if len(inputString) == 1 and inputString[0] == "q":
                    print("Uscita")
                    exit()
                if len(inputString) != 2:
                    print("Formato non valido")
                    continue
                choice, arg = inputString
                if choice in ('s', 'a', 'r'):
                    break
                else:
                    print("Comando {} non riconosciuto".format(choice))
            except ICampusParserError as ex:
                exit(str(ex))
        if choice == "s":
            print("Cerco i corsi contenenti {}...".format(arg))
            result = handler.searchCorso(arg)
            if result:
                print("Risultati:")
                for c in result:
                    print(c)
            else:
                print("Nessun corso corrisponde ai criteri")
        elif choice == "a":
            print("Aggiungo il corso {}...".format(arg))
            res = handler.addCorso(arg)
            if res:
                print("Aggiunta effettuata con successo!")
            else:
                print("Errore nell'aggiunta!")
        elif choice == "r":
            print("Rimuovo il corso {}...".format(arg))
            res = handler.removeCorso(arg)
            if res:
                print("Rimozione effettuata con successo!")
            else:
                print("Errore nella rimozione!")
