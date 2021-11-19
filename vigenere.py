import string
import functools as ft
import math as mth

FreqIngles = [.082, .015, .028, .043, .127, .022, .020, .061,
              .070, .002, .008, .040, .024, .067, .075, .019,
              .001, .060, .063, .091, .028, .010, .023, .001,
              .020, .001]


def encriptar(texto: str, llave: str) -> str:
    texto = texto.lower()
    llave = llave.lower()
    s = [string.ascii_lowercase.index(texto[n]) for n in range(len(texto))]
    t = [string.ascii_lowercase.index(llave[n]) for n in range(len(llave))]
    r = [(s[i] + t[i % (len(t))]) % 26 for i in range(len(s))]
    return ''.join([string.ascii_lowercase[i] for i in r])


def kasiski(texto: str) -> list:
    texto = texto.lower()
    candidates = list()
    triplas = set()

    for i in range(len(texto) - 2):
        result = 0
        lengths = set()
        curr = texto[i:i + 3]
        if curr in triplas:
            continue
        else:
            triplas.add(curr)
        for j in range(i + 3, len(texto) - 2):
            if curr == texto[j:j + 3]:
                lengths.add(j - i)
        if lengths != set():
            result = ft.reduce(mth.gcd, list(lengths))
        if result > 1 and result not in candidates:
            candidates.append(result)
    candidates = list(set(candidates))
    candidates.sort()

    for i in range(len(candidates)):
        if candidates[i]:
            for j in range(len(candidates)):
                if i != j:
                    if candidates[j]:
                        if mth.gcd(candidates[j], candidates[i]) != 1:
                            candidates[i] = mth.gcd(candidates[j], candidates[i])
                            candidates[j] = 0
        else:
            continue
    return list(filter(lambda x: x != 0, candidates))


def indCoincidence(x: str):
    frequency = {u: sum([1 for r in x if u == r]) for u in string.ascii_lowercase}
    return sum([frequency[i] * (frequency[i] - 1) / (len(x) * (len(x) - 1)) for i in string.ascii_lowercase])
