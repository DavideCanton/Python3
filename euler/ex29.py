__author__ = 'Davide'

if __name__ == "__main__":
    print(len({a ** b for a in range(2, 101) for b in range(2, 101)}))