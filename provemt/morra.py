__author__ = 'davide'

print("Hai giocato {1}, il pc ha giocato {2}, quindi {0}".format(
    *(lambda s:
      (lambda s1=s, s2=__import__("random").choice(["sasso", "carta", "forbici"]): ("Pareggio", s1, s2)
      if s1 == s2 else ("hai perso... :(", s1, s2) if (s1, s2) in {
          ("sasso", "carta"), ("carta", "forbici"), ("forbici", "sasso")} else ("hai vinto! :)", s1, s2)))
    (input("Scelta giocatore>").lower())
    ()))