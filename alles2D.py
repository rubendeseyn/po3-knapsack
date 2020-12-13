from random import randint
import copy
from VisueelFuncties import *

def GenereerDozen(aantal,ondergrens,bovengrens):
    dozen=[]
    for i in range(aantal):
        dozen+=[[i+1,randint(ondergrens,bovengrens),randint(ondergrens,bovengrens)]]
    return dozen
def LijstDimensies(dozen):
    lijst = dict()
    for i in range(len(dozen)):
        for j in dozen[i]:
            if j in lijst:
                lijst[j] += 1
            else:
                lijst[j] = 1
    return lijst
#Leest een Knapsack2Dbestand in en returnt de dimensies van de container en de matrix van de dozen
def LeesBestand2D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    #We lezen eerst de dimensies van de container in
    dim, breedteContainer, hoogtecontainer=(bestand.readlines()[0].rstrip("\n")).split(", ")
    container=[int(breedteContainer), int(hoogtecontainer)]
    bestand.close()

    dozen=LeesDozen2D(bestandsnaam)

    return container,dozen
# We lezen vervolgens de dimensies van alle dozen in een matrix
#       met per rij: indexDoos, breedteDoos, hoogteDoos
def LeesDozen2D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    # rect= rectangle (gebruiken we niet)
    # i = index van de doos, w = width, h = height
    # p = the profit of the rectangle (gebruiken we niet)
    # c = the number of times that rectangle is repeated (gebruiken we niet)
    dozen=[]
    for line in bestand.readlines()[1:]:
        line=line.rstrip("\n")
        rect, i, w, h, p, c = line.split(", ")
        for j in range(int(c)):
            dozen+=[[int(i)+1,int(w),int(h)]] #we starten met doos 1 i.p.v. 0 drm int(i)+1
    bestand.close()
    return dozen
#Leest een Knapsack3Dbestand in en returnt de dimensies van de container en de matrix van de dozen
def LeesBestand3D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    #We lezen eerst de dimensies van de container in
    dim, breedteContainer, hoogteContainer, lengteContainer, =(bestand.readlines()[0].rstrip("\n")).split(", ")
    container=[int(breedteContainer), int(hoogteContainer), int(lengteContainer)]
    bestand.close()

    dozen=LeesDozen3D(bestandsnaam)
    return container,dozen
# We lezen vervolgens de dimensies van alle dozen in een matrix
#       met per rij: indexDoos, breedteDoos, hoogteDoos, lengteDoos
def LeesDozen3D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    # box(gebruiken we niet)
    # i = index van de doos, w = width, h = height
    # p = the profit of the rectangle (gebruiken we niet)
    # c = the number of times that rectangle is repeated (gebruiken we niet)
    dozen=[]
    for line in bestand.readlines()[1:]:
        line=line.rstrip("\n")
        box, i, w, h, d, p, c = line.split(", ")
        for j in range(int(c)):
            dozen+=[[int(i)+1,int(w),int(h), int(d)]] #we starten met doos 1 i.p.v. 0 drm int(i)+1
    bestand.close()
    return dozen

def LijstDimensies2D(dozen):
    afmetingen = dict()
    for i in range(len(dozen)):
        for j in range(1, 3):
            if j == 1:
                if dozen[i][j] in afmetingen:
                    afmetingen[dozen[i][j]] += 1
                else:
                    afmetingen[dozen[i][j]] = 1
            else:
                if dozen[i][1] != dozen[i][j]:
                    if dozen[i][j] in afmetingen:
                        afmetingen[dozen[i][j]] += 1
                    else:
                        afmetingen[dozen[i][j]] = 1
    return afmetingen

def KleinsteWaarde2D(dozen):
    minimum = 1000000
    for i in range(len(dozen)):
        for j in range(1, 3):
            if dozen[i][j] < minimum:
                minimum = dozen[i][j]
    return minimum

def Laag2D(dozen, container, eerste=True):
    hoogteContainer, breedteContainer = container[0], container[1]
    hoogte = 0
    Laag = []
    KleinsteWaarde = 0

    while hoogteContainer - hoogte >= KleinsteWaarde:
        Rij = []
        breedte = 0
        TeVerwijderen = []
        sleutel = 0
        if eerste:
            for x in range(len(dozen)):
                if dozen[x][1] <= hoogteContainer - hoogte:
                    sleutel = dozen[x][1]
                    break
                elif dozen[x][2] <= hoogteContainer - hoogte:
                    sleutel = dozen[x][2]
                    break
        else:
            afmetingen = LijstDimensies2D(dozen)
            afmetingen = {k: v for k, v in sorted(afmetingen.items(), reverse=True, key=lambda item: item[1])}
            for w in afmetingen.keys():
                if w <= hoogteContainer - hoogte:
                    sleutel = w
                    break
        hoogte += sleutel

        for doos in dozen :
            for j in range(1, 3):
                if doos[j] == sleutel:
                    if doos[1] == doos[2] and j == 1:
                        pass
                    else:
                        if j == 2:
                            a = doos[1]
                            b = doos[2]
                            doos[1] = b
                            doos[2] = a

                        if doos[2] <= breedteContainer - breedte:
                            Rij.append(doos)
                            TeVerwijderen.append(doos)
                            breedte += doos[2]

        for x in TeVerwijderen:
            index = dozen.index(x)
            dozen.pop(index)
        TeVerwijderen = []

        afmetingen = LijstDimensies2D(dozen)
        afm = list(afmetingen.keys())
        afm.sort(reverse=True)
        if len(afm)==0:
            pass
        elif sleutel < afm[-1]:
            pass
        else:
            for x in afm:
                if x > sleutel:
                    pass
                else:
                    for doos in dozen:
                        for j in range(1, 3):
                            if doos[j] == x:
                                if doos[1] == doos[2] and j == 1:
                                    pass
                                else:
                                    if j == 2:
                                        a = doos[1]
                                        b = doos[2]
                                        doos[1] = b
                                        doos[2] = a

                                    if doos[2] <= breedteContainer - breedte:
                                        Rij.append(doos)
                                        TeVerwijderen.append(doos)
                                        breedte += doos[2]
                    for x in TeVerwijderen:
                        index = dozen.index(x)
                        dozen.pop(index)
                    TeVerwijderen = []
        Laag.append(Rij)
        KleinsteWaarde = KleinsteWaarde2D(dozen)
    #print('Overige dozen:', dozen)
    #print('Aantal:', len(dozen))
    return Laag, dozen, hoogte

def EvalueerContainer(laag2D, container):
    opp_cont = container[0] * container[1]
    gebruikte_dozen = GebruikteDozenLaag2D(laag2D)
    opp_dozen = 0
    for doos in gebruikte_dozen:
        opp_dozen += doos[1] * doos[2]

    return opp_dozen / opp_cont


def GebruikteDozen(gevulde_cont):
    gebruiktedozen = []
    for rij in gevulde_cont:
        for doos in rij:
            gebruiktedozen.append(doos)
    return gebruiktedozen


def RandomIndices(dozen):
    aantaldozen = len(dozen)
    indices = list(range(0, aantaldozen))
    random.shuffle(indices)
    nieuwe_volgorde = [dozen[i] for i in indices]
    return nieuwe_volgorde

def Diversificatie(dozen, aantal_begindozen):
    indices = []
    for x in range(aantal_begindozen):
        check = False
        while check == False:
            index = randint(aantal_begindozen, len(dozen)-1)
            if index not in indices:
                a, b = dozen[x], dozen[index]
                dozen[x], dozen[index] = b, a
                indices.append(index)
                check = True
    return dozen

def PercentageOpgevuld2D(dozen, container):
    opvulling = Laag2D(dozen, container)[0]
    gebruikte = GebruikteDozen(opvulling)
    PercentageGevuld = EvalueerContainer(gebruikte, container)
    return PercentageGevuld

def nOplossingen(n=10):
    resultaten = [["Oplossing","Totaal dozen","Gebruikte dozen","Percentage gevuld", "Maximaal percentage","EfficiÃ«ntie inhoud"]]
    for i in range(1,n+1):
        resultaat = [i]
        container, DozenOver, Opvulling2D, hoogte_over = BeginOplossing()
        matrix = VulMatrix(Opvulling2D, container)
        VisualiseerMatrix2(matrix,i)
        GenereerCsv(matrix,'matrix')

        begindozen = GebruikteDozen(Opvulling2D)+ DozenOver
        resultaat.append(len(begindozen))

        gebruikteDozen = GebruikteDozen(Opvulling2D) #aantal gebruikte dozen
        resultaat.append(len(gebruikteDozen) )
        PercentageGevuld = EvalueerContainer(gebruikteDozen, container)

        resultaat.append(str(round(PercentageGevuld*100,2)) + '\%') #percentage gevuld

        PercentageMaximaal = EvalueerContainer(begindozen, container)
        if PercentageMaximaal>1:
            PercentageMaximaal=1
        resultaat.append(str(round(PercentageMaximaal * 100, 2)) + '\%')#maximaal percentage

        #efficiente inhoud
        resultaat.append(str(round(PercentageGevuld * 100 / PercentageMaximaal, 2)) + '\%')
        resultaten.append(resultaat)

        with open("resultaten.csv", "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(resultaten)
    return resultaten

def BeginOplossing(bestand):
    #genereert een random startoplossing uit een dataset
    #Input: /
    #Output: container [hoogte,breedte], DozenOver[doos1,doos2..], Opvulling [[laag],[laag]], hoogte_over= overige hoogte in container

    data = list(LeesBestand2D(bestand))
    container = data[0]
    begindozen = data[1]

    begindozen = RandomIndices(begindozen)
    startdozen = list(begindozen)
    Opvulling2D, DozenOver, hoogte_over = Laag2D(startdozen, container)
    #hoogte_over = container[0]-gebruiktehoogte
    return container, DozenOver, Opvulling2D, hoogte_over

def VerwijderRij(Opvulling2D, hoogte_over, dozenover, container, aantalverwijder=1):
    #verwijdert een laag van een oplossing
    #Input: Opvulling [[laag],[laag]], hoogte_over = overige hoogte in cont, dozenover [doos1,doos2...]
    #Output: Opvulling[#laag-1], hoogte_over: -hoogte laag, dozenover
    #VisualiseerMatrix(Opvulling2D, container,startopl)
    aantal_lagen = len(Opvulling2D)
    if aantalverwijder>=aantal_lagen:   #anders foutmelding bij pop van lege lijst
        aantalverwijder=aantal_lagen-1
    #print("voor verwijderen", Opvulling2D)


    # Dimensie bepalen
    doos1 = Opvulling2D[0][0]
    while type(doos1[0]) is not int:
        doos1 = doos1[0]
    dimensie = len(doos1) - 1

    # bepalen welke rijen er verwijderd worden
    te_verwijderen_rijnummers = []
    percentages = []
    for rij in Opvulling2D:
        percentages.append(EvalueerContainer([[rij]], [container[1], rij[0][1]]))

    for i in range(aantalverwijder):
        minimum = min(percentages)
        index = percentages.index(minimum)
        te_verwijderen_rijnummers.append(index)
        percentages[index] = 1


    #dozen van de te verwijderen rijen toevoegen aan dozenover
    for rijnr in te_verwijderen_rijnummers:
        for doos in Opvulling2D[rijnr]:
            dozenover.append(doos)
        #hoogte_over = hoogte_over + Opvulling2D[rijnr][0][1]

    #lijstnummers sorteren en dan omdraaien zodat rijnummers overeen komen
    te_verwijderen_rijnummers=sorted(te_verwijderen_rijnummers)
    list.reverse(te_verwijderen_rijnummers)

    #print("rijnummers verwijderen", te_verwijderen_rijnummers)
    #rijen verwijderen
    for rijnr in te_verwijderen_rijnummers:
        Opvulling2D.pop(rijnr)
    #print("na lagen verwijderd",Opvulling2D)
    hoogte = 0

    for rij in Opvulling2D:
        hoogte += rij[0][1]
    hoogte_over = container[0] - hoogte
    #VisualiseerMatrix(Opvulling2D, container,lagenVerwijderd)
    return Opvulling2D, hoogte_over, dozenover


def Acceptatie(beste_opl, vorige_opl, nieuwe_opl, container, alfa=0.00):
    #aan de hand van 3 oplossingen geeft deze functie de beste oplossing en oplossing waar we mee verderwerken
    #Input: beste_oplossing [[]], vorige_opl [[]], nieuwe_opl [[]], container[hoogte, breedte], alfa= percentage om toch te accepteren
    beste_percentage = EvalueerContainer(beste_opl, container)
    vorige_percentage = EvalueerContainer(vorige_opl, container)
    #print(vorige_percentage)
    nieuwe_percentage = EvalueerContainer(nieuwe_opl, container)
    #print(nieuwe_percentage)
    #print("nieuwpercentage",nieuwe_percentage,"bestepercentage",beste_percentage,"vorigepercentage",vorige_percentage)
    beterdanvorige = False
    beterdanbeste = False
    if nieuwe_percentage > (vorige_percentage-alfa): #percentage verschil om accepteren
        beterdanvorige = True

    if nieuwe_percentage > beste_percentage:
        beterdanbeste = True
    return beterdanvorige,beterdanbeste

def VerbeterOpl(beginverz, besteverz, container, aantalRijenVerwijderen=1):
    #beginelementen = [beginoplossing,hoogte_over_begin, dozenover_begin]
    #besteelementen = [beste_oplossing, hoogte_over_best ,dozenover_best]
    #deze functie verwijdert een laag en kijkt of het beter is

    beginoplossing, hoogte_over_begin, dozenover_begin = copy.deepcopy(beginverz[0]),beginverz[1],beginverz[2]
    beste_oplossing,hoogte_over_best, dozenover_best = copy.deepcopy(besteverz[0]),besteverz[1],besteverz[2]


    vorige_oplossing = copy.deepcopy(beginoplossing)
    vorige_hoogte_over = int(hoogte_over_begin)
    vorige_dozen_over  = list(dozenover_begin)

    nieuwe_oplossing_zonder_laag, hoogte_over_nieuweopl, dozenover_zonder_laag = VerwijderRij(vorige_oplossing,vorige_hoogte_over,vorige_dozen_over, container, aantalRijenVerwijderen)
    verbeterde_deeloplossing, dozenover_nieuweopl, hoogte_over_nieuweopl = Laag2D(dozenover_zonder_laag,[hoogte_over_nieuweopl,container[1]])
    #VisualiseerMatrix(Opvulling2D, container, deelopl)
    nieuwe_oplossing = copy.deepcopy(nieuwe_oplossing_zonder_laag + verbeterde_deeloplossing)
    #VisualiseerMatrix(Opvulling2D, container, nieuwe_oplossing)
    #print("evt nieuwe op", nieuwe_oplossing)
    #print('eff nieuw',EvalueerContainer(GebruikteDozen(nieuwe_oplossing),container))

    beterdanvorige, beterdanbeste = Acceptatie(beste_oplossing, beginoplossing, nieuwe_oplossing, container)
    if beterdanvorige == True:
        huidige_oplossing,hoogte_over_huidig, dozenover_huidig = copy.deepcopy(nieuwe_oplossing), int(hoogte_over_nieuweopl), list(dozenover_nieuweopl)
    else:
        huidige_oplossing, hoogte_over_huidig, dozenover_huidig = copy.deepcopy(beginoplossing), int(hoogte_over_begin), list(dozenover_begin)

    if beterdanbeste == True:
        beste_oplossing, hoogte_over_best, dozenover_best = copy.deepcopy(nieuwe_oplossing), int(hoogte_over_nieuweopl), list(dozenover_nieuweopl)


    return [huidige_oplossing, hoogte_over_huidig, dozenover_huidig], [beste_oplossing, hoogte_over_best, dozenover_best]



def IntensRij(container, beginverz, aantalverbeter, aantalRijenVerwijderen):
    #beginverz = beginopln beginhoogte, dozenoverbegin
    beginverz = [copy.deepcopy(beginverz[0]), beginverz[1], beginverz[2]]
    besteverz = [copy.deepcopy(beginverz[0]), beginverz[1], beginverz[2]]

    for i in range(aantalverbeter):
        beginverz, besteverz = VerbeterOpl(copy.deepcopy(beginverz),copy.deepcopy(besteverz), container, aantalRijenVerwijderen)

    return besteverz

def BerekenHoogte2D(laag):
    hoogte=0
    for rij in laag:
        hoogte+=rij[0][1]
    return hoogte

def ControleerOpl2D(opvulling, container):
    fouten = []
    rijnr = 1
    som_hoogtes = 0
    for rij in opvulling:
        som_breedte = 0
        rij_hoogte = rij[0][1]
        som_hoogtes += rij_hoogte
        for doos in rij:
            som_breedte += doos[2]
            if doos[1] > rij_hoogte:
                bds = 'Doos met index ' + str(doos[0]) + ' in rijnummer ' + str(rijnr) + ' is hoger dan de rijhoogte'
                fouten.append(bds)
        if som_breedte > container[1]:
            bds = 'Rijnr ' + str(rijnr) + ' is te breed'
            fouten.append(bds)
        rijnr += 1
    if som_hoogtes > container[0]:
        bds = 'Laag is te hoog'
        fouten.append(bds)
    return fouten

def TestLaag():
    data = ['Data1.2kp', 'Data3.2kp', 'Data3.2kp', 'Data4.2kp', 'Data5.2kp', 'Data6.2kp']
    for x in data:
        container, dozen = LeesBestand2D(x)
        Opvulling2D, DozenOver, hoogte = Laag2D(dozen, container)
        controle = ControleerOpl2D(Opvulling2D, container)
        if len(controle) != 0:
            bds = 'Fout bij ' + x +':'
            print(bds)
            print(controle)
        else:
            bds = 'Laag ok'
            print(bds)
    return None
