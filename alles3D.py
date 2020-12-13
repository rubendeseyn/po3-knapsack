from alles2D import *

def GenereerDozen(aantal, ondergrens, bovengrens):
    dozen = []
    for i in range(aantal):
        dozen += [[i + 1, randint(ondergrens, bovengrens), randint(ondergrens, bovengrens)]]
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


# Leest een Knapsack2Dbestand in en returnt de dimensies van de container en de matrix van de dozen
def LeesBestand2D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    # We lezen eerst de dimensies van de container in
    dim, breedteContainer, hoogtecontainer = (bestand.readlines()[0].rstrip("\n")).split(", ")
    container = [int(breedteContainer), int(hoogtecontainer)]
    bestand.close()

    dozen = LeesDozen2D(bestandsnaam)

    return container, dozen


# We lezen vervolgens de dimensies van alle dozen in een matrix
#       met per rij: indexDoos, breedteDoos, hoogteDoos
def LeesDozen2D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    # rect= rectangle (gebruiken we niet)
    # i = index van de doos, w = width, h = height
    # p = the profit of the rectangle (gebruiken we niet)
    # c = the number of times that rectangle is repeated (gebruiken we niet)
    dozen = []
    for line in bestand.readlines()[1:]:
        line = line.rstrip("\n")
        rect, i, w, h, p, c = line.split(", ")
        for j in range(int(c)):
            dozen += [[int(i) + 1, int(w), int(h)]]  # we starten met doos 1 i.p.v. 0 drm int(i)+1
    bestand.close()
    return dozen


# Leest een Knapsack3Dbestand in en returnt de dimensies van de container en de matrix van de dozen
def LeesBestand3D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    # We lezen eerst de dimensies van de container in
    dim, breedteContainer, hoogteContainer, lengteContainer, = (bestand.readlines()[0].rstrip("\n")).split(", ")
    container = [int(breedteContainer), int(hoogteContainer), int(lengteContainer)]
    bestand.close()

    dozen = LeesDozen3D(bestandsnaam)

    return container, dozen


# We lezen vervolgens de dimensies van alle dozen in een matrix
#       met per rij: indexDoos, breedteDoos, hoogteDoos, lengteDoos
def LeesDozen3D(bestandsnaam):
    bestand = open(bestandsnaam, "r")

    # box(gebruiken we niet)
    # i = index van de doos, w = width, h = height
    # p = the profit of the rectangle (gebruiken we niet)
    # c = the number of times that rectangle is repeated (gebruiken we niet)
    dozen = []
    for line in bestand.readlines()[1:]:
        line = line.rstrip("\n")
        box, i, w, h, d, p, c = line.split(", ")
        for j in range(int(c)):
            dozen += [[int(i) + 1, int(w), int(h), int(d)]]  # we starten met doos 1 i.p.v. 0 drm int(i)+1
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


def EvalueerContainer(gevulde_cont, container):
    gebruiktedozen = GebruikteDozenLaag2D(gevulde_cont)
    opp_cont = container[0] * container[1]
    opp_dozen = 0
    for doos in gebruiktedozen:
        opp_dozen += doos[1] * doos[2]
    return opp_dozen / opp_cont


def EvalueerContainer3D(gevulde_cont, container):
    gebruiktedozen = GebruikteDozen3D(gevulde_cont)

    opp_cont = container[0] * container[1] * container[2]
    opp_dozen = 0
    for doos in gebruiktedozen:
        opp_dozen += doos[1] * doos[2] * doos[3]
    return opp_dozen / opp_cont


def EvalueerLaag3D(laag, afmetingen):
    gebruiktedozen = []
    for rij in laag:
        for doos in rij:
            gebruiktedozen.append(doos)
    opp_cont = afmetingen[0] * afmetingen[1] * afmetingen[2]
    opp_dozen = 0
    for doos in gebruiktedozen:
        opp_dozen += doos[1] * doos[2] * doos[3]
    return opp_dozen / opp_cont


def GenereerLagen(dozen, container, omdraaien=True):
    lagen = []
    hoogtelagen = []
    while len(dozen) > 0:
        hoogte = dozen[0][3]
        hoogtelagen.append(hoogte)
        dozenlaag = []
        # afmetingen overlopen
        for doos in dozen:
            if omdraaien == True:
                tel = []
                for x in range(1, 4):
                    if doos[x] <= hoogte:  # z-as
                        tel.append(doos[x])
                if len(tel) == 0:
                    continue
                maximum = max(tel)
                index = doos.index(maximum)
                if index != 3:
                    a = doos[index]
                    b = doos[3]
                    doos[index] = b
                    doos[3] = a
                dozenlaag.append(doos)
            else:
                if doos[3] <= hoogte:
                    dozenlaag.append(doos)

        for doos in dozenlaag:
            index = dozen.index(doos)
            dozen.pop(index)
        dozenlaag.sort(key=lambda x: x[3], reverse=True)
        laag, overigedozen, nutteloos = Laag2D(dozenlaag, container)
        lagen.append(laag)
        for doos in overigedozen:
            dozen.append(doos)
    return lagen, hoogtelagen


def BesteAfmetingen(dozen):
    inhoud = 0
    container = []
    for doos in dozen:
        inhoud += doos[1] * doos[2] * doos[3]
    x = inhoud ** (1 / 3)
    x = round(x + 1)
    for i in range(3):
        container.append(x)
    return container


def MaakOpvulling3D(dozen, container, draaien=True):
    ongebruiktedozen = []
    lagen, hoogtelagen = GenereerLagen(dozen, container, draaien)

    percentages = []
    volgorde = []
    hoogte = 0
    opvulling = []
    for i in range(len(lagen)):
        per = EvalueerLaag3D(lagen[i], [container[0], container[1], hoogtelagen[i]])
        per /= hoogtelagen[i]
        percentages.append(per)
    for i in range(len(percentages)):
        maximum = max(percentages)
        ind = percentages.index(maximum)
        volgorde.append(ind)
        hoogtelagen[i], hoogtelagen[ind] = hoogtelagen[ind], hoogtelagen[i]
        percentages[ind] = 0

    for i in range(len(volgorde)):
        hoogtelaag = BerekenMaxHoogteLaag3D(lagen[i])
        if hoogte + hoogtelaag <= container[2]:
            opvulling.append(lagen[i])
            hoogte += hoogtelaag
        else:
            ongebruiktedozen += GebruikteDozen(lagen[i])

    # procent = EvalueerContainer3D(opvulling,container)
    hoogte_over = container[2] - hoogte
    return opvulling, ongebruiktedozen, hoogte_over


def Knapsack3D(dozen, container, stappen):
    beginoplossing = copy.copy(dozen)
    beter = 0
    beginwaarde = MaakOpvulling3D(dozen, container)
    besteoplossing = copy.copy(beginoplossing)
    for x in range(stappen):
        poging = random.sample(beginoplossing, len(beginoplossing))
        # print(MaakOpvulling3D(poging, container))
        if MaakOpvulling3D(poging, container) > beginwaarde:
            beter += 1
        if MaakOpvulling3D(poging, container) > MaakOpvulling3D(besteoplossing, container):
            besteoplossing = poging
    # print('Aantal beter dan beginoplossing:', beter)
    # print('Beginoplossing:', beginoplossing)
    return besteoplossing, MaakOpvulling3D(besteoplossing, container)

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

def BeginOplossing3D(bestandsnaam="Data3.3kp", aantalDozenDivers=10):
    #genereert een random startoplossing uit een dataset
    #Input: /
    #Output: container [hoogte,breedte], DozenOver[doos1,doos2..], Opvulling [[laag],[laag]], hoogte_over= overige hoogte in container
    container, dozen = LeesBestand3D(bestandsnaam)


    begindozen = list(dozen)
    #begindozen = RandomIndices(begindozen) #!!!!!!!!!!
    begindozen=Diversificatie(begindozen,aantalDozenDivers)
    startdozen = list(begindozen)
    opvulling, overigedozen, hoogte_over = MaakOpvulling3D(startdozen, container)

    #GenereerCsv(opvulling,'beginopl3D')
    #Opvulling2D, DozenOver, hoogte_over = Laag2D2(startdozen, container)
    #hoogte_over = container[0]-gebruiktehoogte
    return container, overigedozen, opvulling, hoogte_over

def Acceptatie3D(beste_opl, vorige_opl, nieuwe_opl, container,verwerpingsgrens=0):
    #aan de hand van 3 oplossingen geeft deze functie de beste oplossing en oplossing waar we mee verderwerken
    #Input: beste_oplossing [[]], vorige_opl [[]], nieuwe_opl [[]], container[hoogte, breedte], alfa= percentage om toch te accepteren
    beste_percentage = EvalueerContainer3D(beste_opl, container)
    vorige_percentage = EvalueerContainer3D(vorige_opl, container)
    nieuwe_percentage = EvalueerContainer3D(nieuwe_opl, container)
    #temp_acceptatie = max(0.01,temp_acceptatie) #!!!!!!!! nog op lossen
    #resultaatexp=exp((nieuwe_percentage-vorige_percentage)/temp_acceptatie) #opm: (nieuwe_percentage-vorige_percentage) is een neg. getal
    # exp()is een getal dicht bij 1, hoe kleiner het verschil hoe dichter bij 1 (wnr temp=1)

    beterdanvorige = False
    beterdanbeste = False
    if nieuwe_percentage+verwerpingsgrens > vorige_percentage:
        beterdanvorige = True
        #temp_acceptatie-=verlaagTempStap
        #temperatuur moet verlaagd worden zodat resultaatexp kleiner wordt en het accepteren dus moeilijk wordt

    if nieuwe_percentage > beste_percentage:
        beterdanbeste = True

    return beterdanvorige, beterdanbeste

def VerwijderLaag(Opvulling3D, hoogte_over, dozenover, aantalverwijder=1):
    #verwijdert een laag van een oplossing
    #Input: Opvulling [[laag],[laag]], hoogte_over = overige hoogte in cont, dozenover [doos1,doos2..]
    #Output: Opvulling[#laag-1], hoogte_over: -hoogte laag, dozenover

    aantal_lagen = len(Opvulling3D)
    #print("voor lagen verwijderd",Opvulling3D)
    if aantalverwijder >= aantal_lagen:
        aantalverwijder = aantal_lagen-1

    te_verwijderen_laagnummers = []
    for i in range(aantalverwijder):  # bepalen welke lagen er verwijdert worden
        if aantal_lagen==0:
            print("Dit is een lege laag!")
            #return Opvulling3D, hoogte_over, dozenover
        if aantal_lagen==1:
            laagnr=0
        else:
            laagnr = randint(0, aantal_lagen - 1)

        controle = 0  # zort ervoor dat we niet in een oneindige lus terechtkomen
        while laagnr in te_verwijderen_laagnummers and controle < 10:  # zo vermijden dat er 2 keer zelfde laag wordt verwijdert
            laagnr = randint(0, aantal_lagen - 1)
            controle += 1

        te_verwijderen_laagnummers.append(laagnr)

    hoogte_over=hoogte_over
    # dozen van de te verwijderen lagen toevoegen aan dozenover
    for laagnr in te_verwijderen_laagnummers:
        for rij in Opvulling3D[laagnr]:
            for doos in rij:
                dozenover.append(doos)
        hoogte_over+=Opvulling3D[laagnr][0][0][3]

    # lijstnummers sorteren en dan omdraaien zodat laagnummers overeen komen
    te_verwijderen_laagnummers = sorted(te_verwijderen_laagnummers)
    list.reverse(te_verwijderen_laagnummers)

   # print("laagnummers verwijderen", te_verwijderen_laagnummers)
    # rijen verwijderen
    for laagnr in te_verwijderen_laagnummers:
        Opvulling3D.pop(laagnr)
   # print("na lagen verwijderd",Opvulling3D)
    return Opvulling3D, hoogte_over, dozenover



def VerbeterOpl3D(beginverz, besteverz, container,aantal_laag_verwijderen,verwerpingsgrens):
    #beginelementen = [beginoplossing,hoogte_over_begin, dozenover_begin]
    #besteelementen = [beste_oplossing, hoogte_over_best ,dozenover_best]
    #deze functie verwijdert een laag en kijkt of het beter is

    beginoplossing,hoogte_over_begin, dozenover_begin = copy.deepcopy(beginverz[0]),beginverz[1],beginverz[2]
    beste_oplossing, hoogte_over_best, dozenover_best = copy.deepcopy(besteverz[0]),besteverz[1],besteverz[2]

    vorige_oplossing = copy.deepcopy(beginoplossing)
    vorige_hoogte_over = int(hoogte_over_begin)
    vorige_dozen_over  = list(dozenover_begin)

    nieuwe_oplossing_zonder_laag, hoogte_over_nieuweopl, dozenover_zonder_laag = VerwijderLaag(vorige_oplossing,vorige_hoogte_over,vorige_dozen_over,aantal_laag_verwijderen)

    verbeterde_deeloplossing, dozenover_nieuweopl, hoogte_over_nieuweopl = MaakOpvulling3D(dozenover_zonder_laag,[container[0],container[1],hoogte_over_nieuweopl])
    nieuwe_oplossing = copy.deepcopy(nieuwe_oplossing_zonder_laag + verbeterde_deeloplossing)

    #print('eff nieuw',EvalueerContainer(GebruikteDozen(nieuwe_oplossing),container))

    beterdanvorige, beterdanbeste = Acceptatie3D(beste_oplossing, beginoplossing, nieuwe_oplossing, container,verwerpingsgrens)
    if beterdanvorige == True:
        huidige_oplossing,hoogte_over_huidig, dozenover_huidig = copy.deepcopy(nieuwe_oplossing), hoogte_over_nieuweopl, dozenover_nieuweopl
    else:
        huidige_oplossing, hoogte_over_huidig, dozenover_huidig = copy.deepcopy(beginoplossing), hoogte_over_begin, dozenover_begin

    if beterdanbeste == True:
        beste_oplossing, hoogte_over_best, dozenover_best = copy.deepcopy(nieuwe_oplossing), hoogte_over_nieuweopl, dozenover_nieuweopl


    return [copy.deepcopy(huidige_oplossing), hoogte_over_huidig, dozenover_huidig], [copy.deepcopy(beste_oplossing), hoogte_over_best, dozenover_best]

def IntensLaag(container, beginverz, aantalverbeter,aantal_laag_verwijderen, verwerpingsgrens):
    #beginopl
    beginverz = copy.deepcopy(beginverz)
    besteverz = copy.deepcopy(beginverz)

    for i in range(aantalverbeter):
        beginverz, besteverz = VerbeterOpl3D(beginverz, besteverz, container,aantal_laag_verwijderen,verwerpingsgrens)
        #GenereerCsv(beginverz[0], naam='beginverz' + str(i))
        beginverz = copy.deepcopy(beginverz)
        besteverz = copy.deepcopy(beginverz)

    #GenereerCsv(besteverz[0], naam='beste_opl' )
    return besteverz

def IntensLaagRij3D(container, beginverz, aantalverbeter, aantalRijenVerwijderen,verwerpingsgrens,draaien=True):

    opvulling_begin3D, hoogte_over_begin, dozenover_begin = copy.deepcopy(beginverz[0]), int(beginverz[1]), list(beginverz[2])
    beginverz = copy.deepcopy(beginverz)
    nieuwe_opvulling3D = []
    for laag in beginverz[0]:
        #dieptelaag = BerekenLengte2D(laag)
        hoogte = laag[0][0][3]
        overige_hoogte = container[0] - hoogte
        dozen = beginverz[2]
        geschiktedozen, overige_dozen = SelecteerDozen(dozen,container[0],container[1],hoogte,draaien=draaien)
        beginverz2D = [laag, overige_hoogte, geschiktedozen]
        nieuweopl = IntensRij(container, beginverz2D, aantalverbeter, aantalRijenVerwijderen)
        nieuwe_laag, overige_hoogte, dozenover_begin = nieuweopl[0], nieuweopl[1], nieuweopl[2]
        nieuwe_opvulling3D.append(nieuwe_laag)
        dozenover_begin += overige_dozen

    nieuwe_oplossing = nieuwe_opvulling3D

    beterdanvorige, beterdanbeste = Acceptatie3D(beginverz[0], beginverz[0], nieuwe_oplossing, container,verwerpingsgrens)
    if beterdanvorige == True:
        nieuweverz = [copy.deepcopy(nieuwe_oplossing), hoogte_over_begin, dozenover_begin]
    else:
        nieuweverz = beginverz

    return nieuweverz

def ControleerOpl3D(opvulling, container):
    diepte = 0
    fouten = []
    for x in range(len(opvulling)):
        diepte_x = opvulling[x][0][0][3]
        diepte += diepte_x
        fouten_laagx = ControleerOpl2D(opvulling[x], container)
        for rij in opvulling[x]:
            for doos in rij:
                if doos[3] > diepte_x:
                    bds = 'Doos met index ' + str(doos[0]) + ' in laag ' + str(x) + 'is te hoog (in diepte) voor rij'
                    fouten.append(bds)
        if len(fouten_laagx) != 0:
            bds = 'Fout in laag ' + str(x) + ': ' + str(fouten_laagx)
            fouten.append(bds)
    if diepte > container[2]:
        bds = 'Container is ' + str(diepte - container[2]) + ' te hoog (in diepte) voor container'
        fouten.append(bds)
    return fouten

#deze functie is handig bij het opvullen van een rij als er geen dozen meer zijn van maximale hoogte. 2 dozen stapelen in een rij
def SamenvoegenDozen2D(rij,dozenover,container):
    max_hoogte_cont,max_breedte_cont = container[0], container[1]
    gebr_dozen_rij = GebruikteDozenRij2D(rij)
    breedte_rij=0
    max_hoogte_rij = 0
    for doos in gebr_dozen_rij:
        breedte_rij += doos[2]
        if doos[1]>max_hoogte_rij:
            max_hoogte_rij=doos[1]
    nieuwerij = []

    for doos in rij:
        # if type(doos[0])==list:
        # #NOG TE DEON
        # else:
            if doos[1]<max_hoogte_rij:

                overige_hoogte = int(max_hoogte_rij-doos[1])
                doosbreedte = doos[2]
                #selecteer dozen volgens toegestane breedte en hoogte

                passende_dozen, overige_dozen = SelecteerDozen2D(dozenover,overige_hoogte,doosbreedte)

                if len(passende_dozen) > 0:
                    #zoek de meest geschikte doos = de doos met breedste breedte
                    #print('passende dozen',passende_dozen)

                    doos = [doos]
                    while len(passende_dozen)>0:

                        bestedoos = 0
                        max_breedte_passendedoos = 0
                        for passendedoos in passende_dozen:
                            if passendedoos[2]>max_breedte_passendedoos:
                                max_breedte_passendedoos=passendedoos[2]
                                bestedoos=passendedoos
                        #print('bestedoos',bestedoos)
                        overige_hoogte -= bestedoos[1]
                        doos.append(bestedoos)
                        passende_dozen.remove(bestedoos)
                        #print(passende_dozen)
                        dozenover= passende_dozen + overige_dozen
                        #print(dozenover)
                        passende_dozen, overige_dozen = SelecteerDozen2D(dozenover, overige_hoogte, doosbreedte)

                    nieuwerij.append(doos)

                else:
                    nieuwerij.append(doos)
            else:
                nieuwerij.append(doos)
    return nieuwerij,dozenover

def SamenvoegenDozen2Dv2(rij,dozenover,container): #niet gebruiken
    max_hoogte_cont,max_breedte_cont = container[0], container[1]
    gebr_dozen_rij = GebruikteDozenRij2D(rij)
    breedte_rij=0
    max_hoogte_rij = 0
    for doos in gebr_dozen_rij:
        breedte_rij += doos[2]
        if doos[1]>max_hoogte_rij:
            max_hoogte_rij=doos[1]
    nieuwerij = []

    for doos in rij:
        if type(doos[0])==list:
            print(NotImplementedError)
        else:
            if doos[1]<max_hoogte_rij:
                overige_hoogte = max_hoogte_rij-doos[1]
                subcontainer = [doos[2],overige_hoogte]

                sublaag,dozenover,hoogte = Laag2D(dozenover,subcontainer)
                if len(sublaag)>0:
                    nieuwedoos = [doos]
                    nieuwedoos += GebruikteDozenLaag2D(sublaag)
                    nieuwerij.append(nieuwedoos)
            else:
                nieuwerij.append(doos)
    return nieuwerij,dozenover

def SamenvoegenDozen3Dz(laag,dozenover,container,draaien):
    huidigelaag = copy.deepcopy(laag)
    maxhoogte = BerekenMaxHoogteLaag3D(laag)
    nieuwelaag = []
    for rij in laag:
        nieuwerij = []
        for doos in rij:
            if type(doos[0])==list and doos[0][4]=='y':
                nieuwedoos = [] #extra in y + extra in z
                for x in doos:
                    if x[3] < maxhoogte:
                        xlengte, xbreedte, xhoogte = x[1], x[2], x[3]
                        subcontainer = [xlengte, xbreedte, xhoogte]

                        geschikte_dozen, overige_dozen = SelecteerDozen(dozenover, xlengte, xbreedte, maxhoogte-xhoogte,draaien=draaien)
                        if len(geschikte_dozen)>0:
                            doosx = [x]
                            while len(geschikte_dozen) > 0:
                                max_opp_passendedoos = 0
                                bestedoos = 0
                                doos1x = list(x)
                                doos1x.append('z')
                                for gesch_doos in geschikte_dozen:
                                    if gesch_doos[2] * gesch_doos[1] > max_opp_passendedoos:
                                        max_opp_passendedoos = gesch_doos[2] * gesch_doos[1]
                                        bestedoos = gesch_doos
                                xhoogte += bestedoos[3]
                                doosx.append(bestedoos)
                                geschikte_dozen.remove(bestedoos)
                                dozenover = geschikte_dozen + overige_dozen
                                geschikte_dozen, overige_dozen = SelecteerDozen(dozenover, xlengte, xbreedte,maxhoogte - xhoogte,draaien=draaien)
                            nieuwedoos.append(doosx)
                        else:
                            nieuwedoos.append(doos)
                    else:
                        nieuwedoos.append(doos)
                nieuwerij.append(nieuwedoos)
            elif type(doos[0])==int:
                if doos[3]<maxhoogte:
                    dooslengte, doosbreedte,dooshoogte = doos[1],doos[2],doos[3]

                    geschikte_dozen, overige_dozen = SelecteerDozen(dozenover,dooslengte,doosbreedte,maxhoogte-dooshoogte,draaien=draaien)
                    if len(geschikte_dozen)>0:
                        doos.append('z')
                        doos=[doos]
                        while len(geschikte_dozen)>0:
                            max_opp_passendedoos = 0
                            bestedoos = 0
                            for gesch_doos in geschikte_dozen:
                                if gesch_doos[2]*gesch_doos[1] > max_opp_passendedoos:
                                    max_opp_passendedoos = gesch_doos[2]*gesch_doos[1]
                                    bestedoos = gesch_doos
                            doos.append(bestedoos)
                            dooslengte += bestedoos[3]
                            geschikte_dozen.remove(bestedoos)
                            dozenover = geschikte_dozen + overige_dozen
                            geschikte_dozen, overige_dozen = SelecteerDozen(dozenover, dooslengte, doosbreedte,maxhoogte - dooslengte,draaien=draaien)
                        nieuwerij.append(doos)

                    else:
                        nieuwerij.append(doos)
                else:
                    nieuwerij.append(doos)
            else:
                print(NotImplementedError)
        nieuwelaag.append(nieuwerij)
    return nieuwelaag, dozenover

def SamenvoegenDozen3Dy(laag,dozenover,container,draaien=True):
    huidigelaag = copy.deepcopy(laag)

    nieuwelaag = []
    for rij in laag:
        maxlengte = BerekenMaxLengteRij(rij)
        #print(maxlengte)
        nieuwerij = []
        for doos in rij:
            if doos[2]<maxlengte:
                dooslengte, doosbreedte,dooshoogte = doos[1],doos[2],doos[3]
                subcontainer = [maxlengte,doosbreedte,dooshoogte]

                geschikte_dozen, overige_dozen = SelecteerDozen(dozenover,maxlengte-doos[1],doosbreedte,dooshoogte,draaien=draaien)
                if len(geschikte_dozen)>0:
                    doos1 = list(doos)
                    doos1.append('y')
                    doos = [doos1]
                    while len(geschikte_dozen)>0:

                        max_opp_passendedoos = 0
                        bestedoos = 0

                        for gesch_doos in geschikte_dozen:
                            if gesch_doos[2]*gesch_doos[1] > max_opp_passendedoos:
                                max_opp_passendedoos = gesch_doos[2]*gesch_doos[1]
                                bestedoos = gesch_doos
                        doos.append(bestedoos)
                        dooslengte+=bestedoos[1]
                        geschikte_dozen.remove(bestedoos)
                        dozenover = geschikte_dozen + overige_dozen
                        geschikte_dozen, overige_dozen = SelecteerDozen(dozenover, maxlengte - dooslengte, doosbreedte,dooshoogte,draaien=draaien)
                    nieuwerij.append(doos)
                else:
                    nieuwerij.append(doos)
            else:
                nieuwerij.append(doos)
        nieuwelaag.append(nieuwerij)
    return nieuwelaag, dozenover

def SelecteerDozen(dozen,maxlengte,maxbreedte,maxhoogte, draaien=True,enkelomzdraaien=True):
    #6 gevallen (3!)
    selectie_dozen = []
    for doos in dozen:
        if doos[1]<= maxlengte and doos[2] <= maxbreedte and doos[3] <= maxhoogte:
            selectie_dozen.append(doos)
        elif doos[2] <= maxlengte and doos[1] <= maxbreedte and doos[3] <= maxhoogte and draaien==True:
            huidige_breedte = int(doos[2])
            huidige_lengte = int(doos[1])
            doos[1] = huidige_breedte
            doos[2] = huidige_lengte
            selectie_dozen.append(doos)
        elif enkelomzdraaien==False and draaien==True:
            if doos[3] <= maxlengte and doos[1] <= maxbreedte and doos[2] <= maxhoogte:
                huidige_breedte = int(doos[2])
                huidige_lengte = int(doos[1])
                huidige_hoogte = int(doos[3])
                doos[1] = huidige_hoogte
                doos[2] = huidige_breedte
                doos[3] = huidige_lengte
                selectie_dozen.append(doos)
            elif doos[1] <= maxlengte and doos[3] <= maxbreedte and doos[2] <= maxhoogte:
                huidige_breedte = int(doos[2])
                huidige_hoogte = int(doos[3])
                doos[2] = huidige_hoogte
                doos[3] = huidige_breedte
                selectie_dozen.append(doos)
            elif doos[3] <= maxlengte and doos[2] <= maxbreedte and doos[1] <= maxhoogte:
                huidige_lengte = int(doos[2])
                huidige_hoogte = int(doos[3])
                doos[1] = huidige_hoogte
                doos[3] = huidige_lengte
                selectie_dozen.append(doos)
            elif doos[2] <= maxlengte and doos[3] <= maxbreedte and doos[1] <= maxhoogte:
                huidige_breedte = int(doos[2])
                huidige_lengte = int(doos[1])
                huidige_hoogte = int(doos[3])
                doos[1] = huidige_breedte
                doos[2] = huidige_hoogte
                doos[3] = huidige_lengte
                selectie_dozen.append(doos)
    overige_dozen = []
    for doos in dozen:
        if doos not in selectie_dozen:
            overige_dozen.append(doos)

    return selectie_dozen, overige_dozen

def SelecteerDozen2D(dozen,maxlengte,maxbreedte):
    selectie_dozen = []
    for doos in dozen:
        if doos[1]<= maxlengte and doos[2] <= maxbreedte:
            selectie_dozen.append(doos)
        elif doos[2] <= maxlengte and doos[1] <= maxbreedte:
            huidige_breedte = int(doos[2])
            huidige_lengte = int(doos[1])
            doos[1] = huidige_breedte
            doos[2] = huidige_lengte
            selectie_dozen.append(doos)


    if len(selectie_dozen)==0:
        overige_dozen=list(dozen)
    else:
        overige_dozen = []
        for doos in dozen:
            if doos not in selectie_dozen:
                overige_dozen.append(doos)
    return selectie_dozen, overige_dozen