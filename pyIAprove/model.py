from pyIA.logic import Parser

while True:
    try:
        fs = input("Formula>")
        heads = input("Teste>").split()
        formula = Parser().build_formula(fs)
        formula.set_heads(heads)
        print("Formula:", formula.imply_form)
        if formula.is_horn:
            print("Modello minimo:")
            print(formula.minimal_model)
        print("Modelli:")
        for model in formula.models:
            print(model)
        print("Modelli stabili:")
        for model in formula.stable_models:
            print(model)
    except EOFError:
        break
