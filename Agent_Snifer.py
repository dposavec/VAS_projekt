#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
from spade import quit_spade
from Funkcije_Snifera import *
from binascii import hexlify


class Snifer(Agent):

    class Slusac(CyclicBehaviour):

        async def run(self):
            print("Slusam...")
            self.msg = None
            self.msg = await self.receive(timeout=10)
            if self.msg:
                veza = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
                while True:
                    okvir, ostatak = veza.recvfrom(65535)                  
                    eth = ethernet_okvir(okvir)
                    print('\nEthernet okvir:')
                    print('\tOdredisni MAC: {}, Izvorni MAC: {}, Protokol: {}'.format(eth['odr_mac'], eth['izv_mac'],eth['protokol']))
                    adresa = ''
                    if eth['protokol'] == 8:
                        ipv4 = ipv4_okvir(eth['ostatak'])
                        adresa = ipv4['izv_ip']
                        print('\tIPv4 paket:')
                        print('\t\tProtokol: {}, Izvorni IP: {}, Odredisni IP: {}'.format(ipv4['protokol'], ipv4['izv_ip'], ipv4['odr_ip']))
                        if adresa.startswith('10.') == False and adresa.startswith('127.0.') == False and adresa.startswith('192.168') == False:
                            await self.slanje_inspektoru(adresa)
                    elif eth['protokol'] == 1544:
                        arp = arp_okvir(eth['ostatak'])
                        adresa = arp['izv_ip']
                        print('\tARP paket: ')
                        print('\t\tIzvorni MAC: {}, Izvorni IP: {}'.format(arp['izv_mac'], arp['izv_ip']))
                        print('\t\tOdredisni MAC: {}, Odredisni IP: {}'.format(arp['odr_mac'], arp['odr_ip']))
                        if adresa.startswith('10.') == False and adresa.startswith('127.0.') == False and adresa.startswith('192.168') == False:
                            await self.slanje_inspektoru(adresa)

        async def slanje_inspektoru(self, adresa):
            msg = Message(
                    to="dposavec1@rec.foi.hr",
                    metadata={"ontology": "snifanje"},
                    body=adresa)
            await self.send(msg)

    async def setup(self):
        print("Snifer Agent Postavljen.")
        m = Template(metadata={"ontology": "snifanje"})
        slusac = self.Slusac()
        self.add_behaviour(slusac, m)
        print("Zavrseno postavljanje Snifer Agent.")

if __name__ == "__main__":
    a = Snifer("dposavec@rec.foi.hr", "dposavec1")
    a.start()

    input("Press ENTER to exit.\n")
    a.stop()
    quit_spade()

