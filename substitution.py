import math as mth
import functools as ft
import string


class substitution:
    ALPHABET = {}
    def __init__(self, text: str):
        self.text = text
        self.work_text = "".join([i for i in text.lower() if i in string.ascii_lowercase])
        self.permutado = self.work_text
        self.freq_mono = {u: self.work_text.count(u) for u in set(self.work_text)}
        self.freq_di = {u: self._digrams.count(u) for u in set(self._digrams)}
        self.freq_tri = {u: self._trigrams.count(u) for u in set(self._trigrams)}
        self.key = {u : u for u in string.ascii_lowercase}
        self.keychain = [self.key]

    @property
    def _digrams(self):
        return [self.work_text[i:i+2] for i in range(len(self.work_text)-2)]

    @property
    def _trigrams(self):
        return [self.work_text[i:i+3] for i in range(len(self.work_text)-3)]

    def permutar(self, tabla: dict):
        if tabla != self.key:
            self.keychain.append(tabla)
            self.key = self.keychain[-1]
            self.permutado = ''.join([tabla[i] for i in self.work_text])
        else:
            self.permutado = ''.join([tabla[i] for i in self.work_text])

    def revert(self):
        if len(self.keychain) > 1:
            self.keychain.pop()
            self.key = self.keychain[-1]
            self.permutar(self.key)

    def invert(self):
        self.permutar({self.key[u]:u for u in self.key})


