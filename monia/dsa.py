import numpy

def derivate(points):
    """
    Derivazione dei punti presenti in points
    """
    diff = []
    for i in range(len(points)):
        if i == 0:
            diff.append(float(points[1] - points[0]))
        elif i == len(points) - 1:
            diff.append(float(points[-1] - points[-2]))
        else:
            diff.append((points[i + 1] - points[i - 1]) / 2.) 
    return diff

def segmentation(points, eps):
    """
    Segmentazione dei punti in points rispetto alla soglia eps
    """
    media = float("inf")
    n = 0
    segmenti = []
    for elem in points:
        diff = abs(media - elem)
        if diff <= eps:
            segmenti[-1].append(elem)
            n += 1
            media = ((n - 1) * media + elem) / n
        else:
            segmenti.append([elem])
            media = elem
            n = 1
    return segmenti

def approx(segments):
    """
    Approssimazione dei segmenti, associando ad ognuno di essi
    la sua pendenza seg la rispettiva lunghezza
    """
    acc = 0
    ris = []
    for seg in segments:        
        appr = numpy.arctan(numpy.mean(seg)) / numpy.pi + 0.5
        acc += len(seg)
        ris.append((appr, acc))
    return ris

def fill(der):
    """
    Ad ogni segmento s di lunghezza x e pendenza y,
    si associa ad ogni punto in s il valore y
    """
    mapping = {}
    for y, x in der:
        mapping[x] = y
        x -= 1
        while x > 0 and x not in mapping:
            mapping[x] = y
            x -= 1
    filled = list(mapping.items())
    filled.sort()
    return filled
