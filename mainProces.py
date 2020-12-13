from alles3D import *
import time


def Diversificatie(dozen0, aantal):
    dozen = list(dozen0)
    if aantal*2 > len(dozen):
        dozen = dozen[aantal:] + dozen[:aantal]
    else:
        indices = []
        for x in range(aantal):
            index = randint(aantal, len(dozen)-1)
            stap = 0
            while index in indices and stap <10:
                index = randint(aantal, len(dozen) - 1)
                stap += 1
            indices.append(index)
            a, b = dozen[x], dozen[indices[x]]
            dozen[x], dozen[indices[x]] = b, a
    return dozen


def ILS2D(bestandsnaamData='Data1.2kp',rekentijd=2, aantalDozenDivers=1, aantalkeer_intens=5,aantalRijenVerwijderen=2, acceptatie_intens=0,maxNietAccepteren=15,verwerpingsgrens=0.05,verhoogkans=0.05):
    plotx, ploty = [], []
    begintijd = time.time()

    container, dozenover_begin, opvulling_begin, hoogte_over_begin = BeginOplossing(bestandsnaamData)
    beste_opl = copy.deepcopy(opvulling_begin)
    huidigeverz = [opvulling_begin, hoogte_over_begin, dozenover_begin]
    beginverz = [opvulling_begin, hoogte_over_begin, dozenover_begin]

    begin_percentage = EvalueerContainer(beginverz[0], container)
    plotx.append(time.time())
    ploty.append(begin_percentage)

    aantalKeerNietGeaccepteerd = 0
    while (time.time() - begintijd) < rekentijd : #or (plotx[-1]- plotx[-2] >0.5)
        if aantalKeerNietGeaccepteerd > maxNietAccepteren:
            verwerpingsgrens += verhoogkans
            aantalDozenDivers +=5

        verzameling_dozen = GebruikteDozen(opvulling_begin) + dozenover_begin
        verzameling_dozen = Diversificatie(verzameling_dozen, aantalDozenDivers)
        opvulling, ongebruiktedozen, hoogte_over=Laag2D(verzameling_dozen, container)
        opvulling=copy.deepcopy(opvulling)
        nieuweverz=[opvulling, hoogte_over, ongebruiktedozen]

        nieuwe_opl, hoogte_over_nieuweopl, dozenover_nieuweopl = IntensRij(container, nieuweverz,aantalkeer_intens , aantalRijenVerwijderen)
        nieuwe_opl=copy.deepcopy(nieuwe_opl)
        nieuweverz = [nieuwe_opl, hoogte_over_nieuweopl, dozenover_nieuweopl]

        huidige_opl=huidigeverz[0]
        beterdanvorige, beterdanbeste=Acceptatie(beste_opl, huidige_opl, nieuwe_opl, container, verwerpingsgrens)

        if beterdanvorige == True:
            huidigeverz=[copy.deepcopy(nieuwe_opl), hoogte_over_nieuweopl, dozenover_nieuweopl]
            vorige_perc = EvalueerContainer(huidigeverz[0], container)
            plotx.append(time.time())
            ploty.append(vorige_perc)
            aantalKeerNietGeaccepteerd = 0
            verwerpingsgrens = 0
        else:
            aantalKeerNietGeaccepteerd += 1

        if beterdanbeste == True:
            #besteVerz= copy.deepcopy(nieuwe_oplossing), int(hoogte_over_nieuweopl), list(dozenover_nieuweopl)
            beste_opl= copy.deepcopy(nieuwe_opl)

    beste_percentage = EvalueerContainer(beste_opl, container)
    #VisualiseerMatrix(beste_opl,container)
    plt.plot(plotx, ploty, 'o-')
    plt.xlim(plotx[0], plotx[-1])
    plt.ylim(0, 1)
    plt.ylabel('vullingspercentage')
    plt.xlabel('tijd')
    #plt.show()
    #plt.savefig('EVO2D.pdf')
    return begin_percentage, beste_opl, beste_percentage,container


'''
begin_percentage, beste_opl, beste_percentage,container=ILS2D('Data3.2kp',2,20,5,2)
print(begin_percentage)
print(beste_percentage)
print(beste_opl)
print(container)
VisualiseerMatrix(beste_opl,container)
'''


def ILS3D(bestandsnaamData,rekentijd=3, aantalDozenDivers=3, aantalkeer_intens=4, aantalLagenVerwijderen=1,aantalRijenInLaagVerwijderen=1, maxNietAccepteren=5,verwerpingsgrens=0.03,verhoogkans=0.05,draaien=True):
    verwerpingsgrensbegin = int(verwerpingsgrens)
    plotx,ploty,plotxverwerp,plotverwerp = [],[],[],[]

    begintijd = time.time()

    #maak beginoplossing
    container, dozenover_begin, opvulling_begin, hoogte_over_begin = BeginOplossing3D(bestandsnaamData,aantalDozenDivers)


    verzameling_dozen = copy.deepcopy(GebruikteDozen3D(opvulling_begin) + dozenover_begin)

    huidigeverz = [copy.deepcopy(opvulling_begin), int(hoogte_over_begin),list(dozenover_begin)]

    besteverz = [copy.deepcopy(opvulling_begin), int(hoogte_over_begin),list(dozenover_begin)]

    beginverz = [copy.deepcopy(opvulling_begin), int(hoogte_over_begin),list(dozenover_begin)]


    begin_percentage = EvalueerContainer3D(beginverz[0], container)
    plotx.append(time.time())
    ploty.append(begin_percentage)

    plotxverwerp.append(time.time())
    plotverwerp.append(verwerpingsgrens)


    aantalKeerNietGeaccepteerd=0
    stap = 0
    while (time.time() - begintijd) < rekentijd:
        stap += 1
        if aantalKeerNietGeaccepteerd>maxNietAccepteren:
            verwerpingsgrens += verhoogkans
        plotxverwerp.append(time.time())
        plotverwerp.append(verwerpingsgrens)
        #opvulling maken met diversificatie dozen
        verzameling_dozen = Diversificatie(verzameling_dozen, aantalDozenDivers)

        opvulling, ongebruiktedozen, hoogte_over = MaakOpvulling3D(list(verzameling_dozen), container,draaien=draaien)
        nieuweverz = [copy.deepcopy(opvulling), int(hoogte_over), list(ongebruiktedozen)]

        #intensificatie met de gemaakte oplossing
        nieuweverz =IntensLaag(container, nieuweverz, aantalkeer_intens, aantalLagenVerwijderen,verwerpingsgrens)
        nieuwe_opl, hoogte_over_nieuweopl, dozenover_nieuweopl = nieuweverz[0],nieuweverz[1],nieuweverz[2]

        nieuweverz = IntensLaagRij3D(container, nieuweverz, aantalkeer_intens, aantalRijenInLaagVerwijderen, verwerpingsgrens,draaien=draaien)
        nieuwe_opl, hoogte_over_nieuweopl, dozenover_nieuweopl = nieuweverz[0], nieuweverz[1], nieuweverz[2]

        nieuwe_opl2 = []
        for laag in nieuweverz[0]:
            nieuwelaag, dozenover_nieuweopl = SamenvoegenDozen3Dy(laag,dozenover_nieuweopl,container,draaien=draaien)
            nieuwe_opl2.append(nieuwelaag)


        nieuwe_opl3 = []
        for laag in nieuwe_opl2:
            nieuwelaag, dozenover_nieuweopl = SamenvoegenDozen3Dz(laag, dozenover_nieuweopl, container,draaien=draaien)
            nieuwe_opl3.append(nieuwelaag)

        nieuwe_opl = nieuwe_opl3
        #acceptatie bekijken
        beterdanvorige, beterdanbeste = Acceptatie3D(besteverz[0], huidigeverz[0], nieuweverz[0], container, verwerpingsgrens)

        if beterdanvorige == True:
            huidigeverz = [copy.deepcopy(nieuwe_opl), hoogte_over_nieuweopl, dozenover_nieuweopl]
            vorige_perc = EvalueerContainer3D(huidigeverz[0],container)

            plotx.append(time.time())
            ploty.append(vorige_perc)
            aantalKeerNietGeaccepteerd = 0
            verwerpingsgrens=verwerpingsgrensbegin

            #print('geaccepteerd')
        else:
            aantalKeerNietGeaccepteerd += 1
            #print('niet geaccepteerd')
        if beterdanbeste == True:
            besteverz= copy.deepcopy(nieuwe_opl), int(hoogte_over_nieuweopl), list(dozenover_nieuweopl)

        #plot3D(beste_opl,container)

        #vorigeper = EvalueerContainer3D(vorige_opl[0],container)
        #print(temp_acceptatie)




    beste_percentage = EvalueerContainer3D(besteverz[0], container)


        #print(beste_percentage)
    plt.figure()
    plt.plot(plotx, ploty,'o-')
    plt.xlim(plotx[0], plotx[-1])
    plt.ylim(0, 1)
    plt.ylabel('vullingspercentage')
    plt.xlabel('tijd')
    plt.savefig('/Users/rubendeseyn/Desktop/po3/program/percentage_evo/'+str(bestandsnaamData)+'_evo.pdf',)

    plt.figure()
    plt.plot(plotxverwerp, plotverwerp, 'o-')
    plt.xlim(plotx[0], plotx[-1])
    plt.ylim(0, 0.5)
    plt.ylabel('verwerpingsgrens')
    plt.xlabel('tijd')
    plt.savefig('/Users/rubendeseyn/Desktop/po3/program/verwerpingsgrens_evo/' + str(bestandsnaamData) + '_verwerp_evo.pdf', )


    #plot3D(besteverz[0],container)
    beste_opl = besteverz[0]
    begin_opl = beginverz[0]
    return begin_percentage, beste_percentage,begin_opl,beste_opl,stap


#besteverz, begin_percentage, beste_percentage, beste_opl, begin_opl, container= ILS3D('data3D/ep3-60-U-C-90.3kp',rekentijd=3,aantalDozenDivers=5,aantalkeer_intens=10,aantalLagenVerwijderen=3,aantalRijenInLaagVerwijderen=1, maxNietAccepteren=10,verwerpingsgrens=0,verhoogkans=0.15)
# print(ControleerOpl3D(begin_opl,container))
# plot3D(begin_opl,container)
#
# print(begin_percentage)
#print(beste_percentage)
# print(beste_opl)
# print(besteverz[2])
# print(container)
# print(beste_opl)
# print(begin_opl)
#data3D/ep3-20-F-R-50.3kp !!!! geeft fout
#ILS2D()
#ILS2D(bestandsnaamData='Data1.2kp', rekentijd=2, aantalDozenDivers=1, aantalkeer_intens=5, aantalRijenVerwijderen=2, acceptatie_intens=0, maxNietAccepteren=10, verwerpingsgrens=0.0, verhoogkans=0.05)

'''
begin_percentage, beste_opl, beste_percentage,container=ILS3D('ep3-60-U-C-90.3kp',3,4,6,1)
print(begin_percentage)
print(beste_percentage)
print(container)
print(beste_opl)
#print(begin_opl)
'''
