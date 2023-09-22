# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 19:22:19 2022

@author: Bartosz Tłuczkiewicz

Program działa dla grafów skierowanych
"""
import math
import re
import igraph as ig

# EDYTOWALNE
# grafInStr = "3.txt"
inf = math.inf

# STRUKTURA grafDictWezly:
# grafDictTemplatka = {
#     1 : {
#         "pos" : [0, 0],
#         "f": inf,
#         "g": inf,
#         "h": inf
#             },
#     2 : {
#         "pos" : [0, 0],
#         "f": inf,
#         "g": inf,
#         "h": inf
#             },
#     ...
#     }


grafDictTemplatka = {
    "pos": [0, 0],
    # f = g + h
    "f": inf,
    "g": inf,
    "h": inf
}

grafDictWezly = {}
grafMeta = [0, 0]
grafDlug = []

## Definicje


def OtworzGraf(plikStr):

    plikDictWezly = {}
    plikMeta = [0, 0]
    plikDlug = []

    with open(plikStr, "rt") as plikInGraf:
        plikInGrafTab = plikInGraf.readlines()
        # print(plikInGrafTab)

        # Wspolrzedne punktow grafu
        # Regex \( (.*?) \) znajduje najmniejsze (ilosc zankow) grupy pomiedzy 
        # nawiasami zawierajace cokolwiek potem rozdziela je wzgledem ',' i wpisuje
        # do slownika

        plikInGrafKoord = re.findall("\((.*?)\)", plikInGrafTab[0])

        for it, koord in enumerate(plikInGrafKoord):
            plikDictWezly[it+1] = grafDictTemplatka.copy()
            tmpKoord = (koord.lstrip()).split(', ')
            plikDictWezly[it+1]["pos"] = [tmpKoord[0], tmpKoord[1]]

        plikMeta = plikInGrafTab[1].split(' ')

        # Tabela długosci
        for it, linijka in enumerate(plikInGrafTab):
            if it <= 1:
                continue
            plikDlug.append((linijka.lstrip()).split(' '))


        return [plikDictWezly, plikMeta, plikDlug]


def Heurestyka(meta, grafDict, dlugTab):
    for x in grafDict:
        grafDict[x]["h"] = math.sqrt((int(grafDict[x]["pos"][0]) - int(grafDict[meta]["pos"][0])) ** 2 +
                                     (int(grafDict[x]["pos"][1]) - int(grafDict[meta]["pos"][1])) ** 2)
    return


def AGwiazdka(start, meta, grafDict, dlugTab):

    roz = [start]
    Z = [0] * len(grafDict)
    grafDict[start]["f"] = 0
    grafDict[start]["g"] = 0

    # x i y sa od 1 nie od 0 (rzeczywiste nazwy wezlow)

    while len(roz) != 0:
        # x = min(grafDict,key = lambda k: grafDict[k]["f"])
        x = MinRoz(roz, grafDict)
        if x == meta:
            # print("Koszt:")
            # print(grafDict[x]["g"])
            OdtworzTrase(start, x, Z)
            return
        roz.remove(x)
        for y in Sasiad(x, dlugTab):
            tmpg = grafDict[x]["g"] + float(dlugTab[x-1][y-1])
            if tmpg < grafDict[y]["g"]:
                Z[y-1] = x
                grafDict[y]["g"] = tmpg
                grafDict[y]["f"] = grafDict[y]["g"] + grafDict[y]["h"]
                if roz.count(y) == 0:
                    roz.append(y)
    print("Nie wykryto trasy")
    return


def MinRoz(lista, graf):
    tmpMin = inf
    tmpX = 0
    for x in lista:
        if graf[x]["f"] < tmpMin:
            tmpMin = graf[x]["f"]
            tmpX = x
    return tmpX


def Sasiad(x, dlug):
    wynik = []
    for it, a in enumerate(dlug[x-1]):
        if float(a) > 0:
            wynik.append(it+1)
    return wynik


def OdtworzTrase(start, x, Z):
    
    out = []
    # print("Trasa:")
    while x != start:
        # print(x, end=(''))
        # print("<-", end=(''))
        out.insert(0, x)
        x = Z[x-1] 
    
    # print(x)
    out.insert(0, x)
    
    for wiersz in out:
        print(wiersz,end = (' '))
    
    return


## Main

inNazwa = input()
grafInStr = inNazwa
[grafDictWezly, grafMeta, grafDlug] = OtworzGraf(grafInStr)
Heurestyka(int(grafMeta[1]), grafDictWezly, grafDlug)
AGwiazdka(int(grafMeta[0]), int(grafMeta[1]), grafDictWezly, grafDlug)
pass

