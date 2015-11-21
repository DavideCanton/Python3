__author__ = 'Davide'


def check(porzioni):
    piccioni = 0
    mangiare_necessario = 0
    tempo = 1

    while mangiare_necessario < porzioni:
        piccioni += tempo
        mangiare_necessario += piccioni
        tempo += 1

    tempo -= 1
    piccioni_pre = piccioni - tempo

    while mangiare_necessario > porzioni:
        if piccioni > piccioni_pre:
            piccioni -= 1
        else:
            break
        mangiare_necessario -= 1

    return piccioni


if __name__ == "__main__":
    for i in range(0, 21):
        print(i, "->", check(i))