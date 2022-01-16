#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
from spade import quit_spade
from PHP_API import *
from VT_API import *

lista_adresa = []


class Inspektor(Agent):

    class Pokretac(OneShotBehaviour):

        async def run(self):
            print("Postavljen setup pokretača!")
            msg = Message(
                to="dposavec@rec.foi.hr",
                metadata={"ontology": "snifanje"},
                body="Zapocni"
            )
            await self.send(msg)

    class Istrazivac(CyclicBehaviour):

        async def run(self):
            print("Pokrecem istrazivača...")
            global lista_adresa
            self.msg = None
            self.msg = await self.receive(timeout=10)
            if self.msg:
                dobivena_adresa = self.msg.body
                print(dobivena_adresa)
                if dobivena_adresa in lista_adresa:
                    pass
                else:
                    lista_adresa.append(dobivena_adresa)
                    odgovor_php = posalji_na_phpot(dobivena_adresa)
                    if odgovor_php['nadjeno'] == 'greska':
                        print('Odgovor sa Project Honey Pota-a:')
                        print('\tIP adresa ' + dobivena_adresa + ' nije važeća ili upit nije dobro sastavljen...')
                        for i in range(0, 2):
                            print('\n')
                    elif odgovor_php['nadjeno'] == 'da':
                        print('Odgovor sa Project Honey Pota-a:')
                        if odgovor_php['naziv'] == None:
                            print('\tAdresa: ' + dobivena_adresa)
                            print('\tFaktor prijetnje: ' + str(odgovor_php['faktor']) + ', tj. ' + odgovor_php['prijetnja'])
                            print('\tTip prijetnje: ' + odgovor_php['prijetnja'])
                        else:
                            print('\tPod ovom IP adresom (' + dobivena_adresa + ') registrirana je tražilica ' + odgovor_php['naziv'])
                        for i in range(0, 2):
                            print('\n')
                    
    async def setup(self):
        print("Setupiran Inspektor...")
        m = Template(metadata={"ontology": "snifanje"})
        istrazivac = self.Istrazivac()
        pokretac = self.Pokretac()
        self.add_behaviour(istrazivac, m)
        self.add_behaviour(pokretac)
        print("Zavrsen setup..")

if __name__ == "__main__":
    a = Inspektor("dposavec1@rec.foi.hr", "dposavec2")
    a.start()
    input("Press ENTER to exit.\n")
    a.stop()
    quit_spade()