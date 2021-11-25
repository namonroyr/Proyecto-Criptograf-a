import math as mth
import functools as ft
import string
from typing import List, Union, Any
freqs: list[Union[float, Any]] = [.082, .015, .028, .043, .127, .022, .020, .061, .070, .002, .008, .040, .024, .067, .075, .019, .001, .060,
             .063, .091, .028, .010, .023, .001, .020, .001]

class substitution:
    freqs: list[Union[float, Any]] = [.082, .015, .028, .043, .127, .022, .020, .061, .070, .002, .008, .040, .024, .067, .075, .019, .001, .060,
             .063, .091, .028, .010, .023, .001, .020, .001]
    ALPHABETfreq = {string.ascii_lowercase[i]: freqs[i] for i in range(26)}

    DIGRAMAS = {'he': 0.0128, 'th': 0.0152, 'in': 0.0094, 'er': 0.0094, 'an': 0.0084, 're': 0.0064, 'nd': 0.0063,
                'at': 0.0059, 'on': 0.0057, 'nt': 0.0056, 'ha': 0.0056, 'es': 0.0056, 'st': 0.0055, 'en': 0.0055,
                'ed': 0.0053, 'to': 0.0052}
    TRIGRAMAS = {'the': 0.0181, 'and': 0.0073, 'tha': 0.0033, 'ent': 0.0042, 'ing': 0.007, 'ion': 0.0042, 'tio': 0.0031,
                 'for': 0.0034}

    def __init__(self, text: str):
        self.text = text
        self.work_text = "".join([i for i in text.lower() if i in string.ascii_lowercase])
        self.permutado = self.work_text
        self.freq_mono = {u: self.work_text.count(u) for u in set(self.work_text)}
        self.freq_di = {u: self._digrams.count(u) for u in set(self._digrams)}
        self.freq_tri = {u: self._trigrams.count(u) for u in set(self._trigrams)}
        self.key = {u: u for u in string.ascii_lowercase}
        self.keychain = [self.key]

    @property
    def _digrams(self):
        return [self.work_text[i:i + 2] for i in range(len(self.work_text) - 2)]

    @property
    def _trigrams(self):
        return [self.work_text[i:i + 3] for i in range(len(self.work_text) - 3)]

    def permutar(self, tabla: dict):
        for u in string.ascii_lowercase:
            if u not in tabla:
                tabla[u] = u
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
        self.permutar({v: k for k,v in self.key.items()})
