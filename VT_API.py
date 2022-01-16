#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import json

API_KLUC = '76fb17091992dfadab1c3a524905b5c22f9ac9adff15913dd7858d8417d69ec0'


def posalji_na_vt(adresa):
    url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    parametri = {'ip': adresa, 'apikey': API_KLUC}
    odgovor = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parametri))).read()
    odgovor = json.loads(odgovor.decode('utf-8'))
    if odgovor == b'':
        return []
    else:
        if odgovor['detected_urls'][0]:
            lista_urlova = []
            for url in odgovor['detected_urls']:
                faktor = str(url['positives'])
                lista_urlova.append(' detekcija, url: '.join([faktor, url['url']]))
            return lista_urlova
        else:
            return []
