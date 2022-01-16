#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randrange


def posalji_na_phpot(adresa):

    random_number = randrange(125)
    prijetnja = 'Vrlo mala prijetnja.'
    if random_number > 100:
        prijetnja = 'Vrlo velika prijetnja!!!'
    elif random_number > 50:
        prijetnja = 'Velika prijetnja!!'
    elif random_number > 25:
        prijetnja = 'Srednje velika prijetnja!'
    elif random_number > 10:
        prijetnja = 'Mala prijetnja.'
    return {'nadjeno': 'da', 'naziv': None, 'faktor': random_number, 'prijetnja': prijetnja}
