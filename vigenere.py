import string
import functools as ft
import math as mth
from typing import List
FreqIngles = [.082, .015, .028, .043, .127, .022, .020, .061,
              .070, .002, .008, .040, .024, .067, .075, .019,
              .001, .060, .063, .091, .028, .010, .023, .001,
              .020, .001]

alphabet = {u[0]: u[1] for u in zip(string.ascii_lowercase, range(0, 26))}


def encriptar(texto: str, llave: str):
    texto = texto.lower()
    llave = llave.lower()
    texto = ''.join([u for u in texto if u in string.ascii_lowercase])
    s = [alphabet[texto[n]] for n in range(len(texto))]
    t = [alphabet[llave[n]] for n in range(len(llave))]
    r = [(s[i] + t[i % (len(t))]) % 26 for i in range(len(s))]
    return ''.join([string.ascii_lowercase[i] for i in r]).upper()


def kasiski(texto: str):
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


def Mg(y: str):
    freq = [y.count(string.ascii_lowercase[i]) for i in range(len(string.ascii_lowercase))]
    Mgs = []
    n = len(y)
    for j in range(26):
        mg = 0.0
        for i in range(26):
            pos = (i + j) % 26
            mg += ((FreqIngles[i] * freq[pos]) / float(n))
        Mgs.append(mg)
    return Mgs


def decriptar(texto: str, llave: str):
    plano: str = ''
    texto = texto.lower()
    texto = ''.join([i for i in texto if i in string.ascii_lowercase])
    llave = llave.lower()
    for i in range(len(texto)):
        inverso = 26 - (alphabet[llave[i % len(llave)]])
        plano = plano + string.ascii_lowercase[(alphabet[texto[i]] + inverso) % 26]
    return plano.upper()


def examinarM(subcadenas: List[str], m: int):
    listaPrima = list()
    for i in range(m):
        palabra = ''.join([subcadena[i] for subcadena in subcadenas if len(subcadena) > i])
        listaPrima.append(palabra)
    listaSecunda = [indCoincidence(r) for r in listaPrima]
    return sum(listaSecunda) / float(len(listaPrima))


def vigenereAttack(texto: str):
    texto = texto.lower()
    texto = ''.join([i for i in texto if i in string.ascii_lowercase])
    m_p = kasiski(texto)
    m_analizado = [m for m in m_p if
                   abs(0.065 - examinarM([texto[i:i + m] for i in range(0, len(texto), m)], m)) <= 0.005]
    for m in m_analizado:
        llave = list()
        subcadenas = [texto[i:i + m] for i in range(0, len(texto), m)]
        listaPrima = list()
        for i in range(m):
            listaPrima.append(
                ''.join([palabra[i] for palabra in subcadenas if len(palabra) > i])
            )
        for i in range(m):
            Mg_lista = Mg(listaPrima[i])
            llave.append(Mg_lista.index(max(Mg_lista)))
        llave_palabra = ''.join([string.ascii_lowercase[i] for i in llave])
        yield llave_palabra, decriptar(texto, llave_palabra)
