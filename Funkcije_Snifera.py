#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import socket
import ipaddress


def ispisi_ip(bajtovi):
    return '.'.join("{:%d}".format(bajt) for bajt in bajtovi)


def ispisi_mac(bajtovi):
    return ':'.join('%02x' % ord(bajt) for bajt in bajtovi)


def ethernet_okvir(bajtovi_paketa):
    odr_mac, izv_mac, protokol = struct.unpack('! 6s 6s H', bajtovi_paketa[:14])
    odredisna_mac_adresa = ':'.join(odr_mac.hex()[i:i+2] for i in range(0, len(odr_mac.hex()), 2))
    izvorna_mac_adresa = ':'.join(izv_mac.hex()[i:i+2] for i in range(0, len(izv_mac.hex()), 2))
    return {'odr_mac': odredisna_mac_adresa, 'izv_mac': izvorna_mac_adresa, 'protokol': socket.htons(protokol), 'ostatak': bajtovi_paketa[14:]}


def arp_okvir(bajtovi_paketa):
    izv_mac, izv_ip, odr_mac, odr_ip = struct.unpack('8x 6s 4s 6s 4s', bajtovi_paketa[:28])
    return {'izv_mac': ispisi_mac(izv_mac), 'izv_ip': ispisi_ip(izv_ip), 'odr_mac': ispisi_mac(odr_mac),
            'odr_ip': ispisi_ip(odr_ip)}


def ipv4_okvir(bajtovi_paketa):
    izvorna_ip_adresa = socket.inet_ntoa(struct.unpack('! 8x B B 2x 4s 4s', bajtovi_paketa[:20])[2])
    odredisna_ip_adresa = socket.inet_ntoa(struct.unpack('! 8x B B 2x 4s 4s', bajtovi_paketa[:20])[3])
    ttl, protokol, izv_ip, odr_ip = struct.unpack('! 8x B B 2x 4s 4s', bajtovi_paketa[:20])
    return {'ttl': ttl, 'protokol': protokol, 'izv_ip': izvorna_ip_adresa, 'odr_ip': odredisna_ip_adresa, 'verzija': 4}


def tcp_segment(bajtovi_paketa):
    izv_port, odr_port, redni_broj, broj_potvrde, zastavice_pomaka = struct.unpack('! H H L L H', bajtovi_paketa[:14])
    return {'izv_port': izv_port, 'odr_port': odr_port, 'redni_broj': redni_broj, 'broj_potvrde': broj_potvrde,
            'urg': (zastavice_pomaka & 32) >> 5, 'ack': (zastavice_pomaka & 16) >> 4,
            'psh': (zastavice_pomaka & 8) >> 3, 'rst': (zastavice_pomaka & 4) >> 2, 'syn': (zastavice_pomaka & 2) >> 1,
            'fin': zastavice_pomaka & 1}


def udp_segment(bajtovi_paketa):
    izv_port, odr_port, velicina = struct.unpack('! H H 2x H', bajtovi_paketa[:8])
    return {'izv_port': izv_port, 'odr_port': odr_port, 'velicina': velicina}