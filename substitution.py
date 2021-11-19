import math as mth
import functools as ft
import string


def permutar(tabla: dict, texto: str) -> str:
    texto = ''.join([i for i in texto if i in string.ascii_lowercase]).lower()
    return ''.join([tabla[i] for i in texto])


def decript(tabla: dict, texto: str) -> str:
    texto = ''.join([i for i in texto if i in string.ascii_lowercase]).lower()
    llave = {tabla[i]: i for i in tabla}
    return ''.join([llave[i] for i in texto])

