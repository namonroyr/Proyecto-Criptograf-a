import math as mth
import functools as ft
import string

TRIGRAMAS = ['THE', 'ING', 'AND',
             'HER', 'ERE', 'ENT',
             'THA', 'NTH', 'WAS',
             'ETH', 'FOR', 'DTH']
DIGRAMAS = ['TH', 'HE', 'IN', 'ER', 'AN',
            'RE', 'ED', 'ON', 'ES', 'ST',
            'EN', 'AT', 'TO', 'NT', 'HA',
            'ND', 'OU', 'EA', 'NG', 'AS',
            'OR', 'TI', 'IS', 'ET', 'IT',
            'AR', 'TE', 'SE', 'HI', 'OF']
MONOGRAMAS = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R']

ALFABETO = {string.ascii_lowercase[i]: i for i in range(26)}


def permutar(tabla: dict, texto: str) -> str:
    texto = ''.join([i for i in texto if i in string.ascii_lowercase]).lower()
    return ''.join([tabla[i] for i in texto])


def decript(tabla: dict, texto: str) -> str:
    texto = ''.join([i for i in texto if i in string.ascii_lowercase]).lower()
    llave = {tabla[i]: i for i in tabla}
    return ''.join([llave[i] for i in texto])


def monoFreq(x: str) -> list[int]:
    charCount = {i: list(x).count(i) for i in x}
    listaPrima = sorted(charCount, key=lambda x: charCount[x])
    listaPrima.reverse()
    return listaPrima


def diFreq(x: str) -> list[str]:
    diCount = {}
    digramas = [x[i:i + 2] for i in range(len(x))]
    for di in digramas:
        if monoFreq(x)[0] in di:
            if di in diCount:
                diCount[di] += 1
            else:
                diCount[di] = 1
    listaPrima = sorted(diCount, key=lambda x: diCount[x])
    listaPrima.reverse()
    return listaPrima


def substitutionAttack(x: str):
    FreqDigra = diFreq(x)
    FreqMonoGram = monoFreq(x)
