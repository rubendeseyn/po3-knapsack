from IteratedLocalSearch import *
import os

def DataAnalyse2D(map='data2D'):
    file_list = os.listdir(map)

    opp_container = ['Opp_container']
    aantal_dozen = ['Aantal dozen']
    verschil_gr_kl = ['verschil grootste-kleinste']
    gemiddeld_percentage = ['resultaat ILS']
    vierkant_rechthoek = ['vierkant_rechthoek']


    for file in file_list:
        container,dozen = LeesBestand2D(map+'/'+file)
        opp_container.append(container[0]*container[1])
        aantal_dozen.append(len(dozen))

        opp_dozen = []
        for doos in dozen:
            opp_dozen.append(doos[1]*doos[2])

        opp_dozen.sort()
        verschil_opp = opp_dozen[-1]-opp_dozen[0]
        verschil_gr_kl.append(verschil_opp)
        gemiddeld_percentage.append(ILS2D(map+'/'+file)[2])

    file_list.insert(0, 'bestandsnaam')
    tabel = [file_list, opp_container, aantal_dozen, verschil_gr_kl, gemiddeld_percentage,gemiddeld_percentage]
    GenereerCsv(tabel,'DataAnalyse2D')


def DataAnalyse3D(map='selectie3D'):
    file_list = os.listdir(map)
    vol_container = ['Volume_container']
    aantal_dozen = ['Aantal dozen']
    verschil_gr_kl = ['verschil grootste-kleinste']
    begin_percentage_draaien = ['beginresultaat ILS met draaien']
    max_percentage_draaien = ['resultaat ILS met draaien']
    #max_percentage_zonder_draaien = ['resultaat ILS zonder draaien']
    vierkant_rechthoek = ['vierkant_rechthoek']
    stappen_met_draaien = ['aantal stappen met draaien']
    beste_opln = ['beste opln']
    #stappen_zonder_draaien = ['aantal stappen zonder draaien']
    print(file_list)
    for file in file_list:
        #vierkant_rechthoek.append(file[10])

        container, dozen = LeesBestand3D(map+'/' + file)
        vol_container.append(container[0] * container[1]*container[2])

        aantal_dozen.append(len(dozen))

        vol_dozen = []
        for doos in dozen:
            vol_dozen.append(doos[1]*doos[2]*doos[3])

        vol_dozen.sort()
        verschil_opp = vol_dozen[-1] - vol_dozen[0]
        verschil_gr_kl.append(verschil_opp)
        begin_percentage, beste_percentage, begin_opl, beste_opl, stap = ILS3D(map+'/' + file)
        print(beste_percentage)
        stappen_met_draaien.append(stap)
        max_percentage_draaien.append(beste_percentage)
        begin_percentage_draaien.append(begin_percentage)
        beste_opln.append(beste_opl)
        #begin_percentage, beste_percentage, begin_opl, beste_opl,stap = ILS3D(map + '/' + file,draaien=False)
        #stappen_zonder_draaien.append(stap)
        #max_percentage_zonder_draaien.append(beste_percentage)
        #plot3D(beste_opl,container)

        #plot3D(beste_opl,container)

    file_list.insert(0,'bestandsnaam')

    tabel = [file_list, vol_container, aantal_dozen, verschil_gr_kl,stappen_met_draaien,max_percentage_draaien, begin_percentage_draaien,beste_opln]
    GenereerCsv(tabel, 'DataAnalyse3D')
    #print(GenereerLatexCode(tabel))
    return tabel

def Parameterstesten(map='selectie3D'):

    file_list = os.listdir(map)
    print(file_list)
    aantalDozenDivers = [x for x in range(1,10)]
    aantalkeer_intens = [x for x in range(2,11)]
    aantalLagenVerwijderen = [x for x in range(1,4)]
    aantalRijenInLaagVerwijderen = [x for x in range(1,9)]
    maxNietAccepteren = [2,3,4,5,6,7,8,9,10]
    verhoogkans = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15]
    verwerpingsgrens = [0,0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15]

    draaien = [True,False]

    parameters = [aantalDozenDivers, aantalkeer_intens, aantalLagenVerwijderen, aantalRijenInLaagVerwijderen, maxNietAccepteren,draaien,verhoogkans,verwerpingsgrens]
    paraNaam = ['aantalDozenDivers', 'aantalkeer_intens', 'aantalLagenVerwijderen', 'aantalRijenInLaagVerwijderen','maxNietAccepteren',  'draaien','verhoogkans','verwerpingsgrens']


    #default waarden zijn = [data, 80, 5, 8, 3, 8, 0.075, 0.05]

    # als test hoef je gewoon de lijst te kopiëren die je wil testen, verder moet je hieronder nog juiste waarde als 'x' instellen
    index= 7
    test = parameters[index]
    parameterwaarden = ['parameterwaarden']
    percentages = ['gemiddelde percentages']
    stappen = ['gemiddeld aantal stappen']

    for x in test:
        som_percentages = 0
        som_stappen = 0
        print(x)
        parameterwaarden.append(x)
        for bestand in file_list:
            begin_percentage, beste_percentage,begin_opl,beste_opl,stap = ILS3D(str(map)+'/'+bestand, rekentijd=3, aantalDozenDivers=3, aantalkeer_intens=4, aantalLagenVerwijderen=1,aantalRijenInLaagVerwijderen=1, maxNietAccepteren=5,verwerpingsgrens=0.03,verhoogkans=0.05,draaien=True)
            som_percentages += beste_percentage
            som_stappen += stap
        som_stappen /= len(file_list)
        som_percentages /= len(file_list)
        percentages.append(som_percentages)
        stappen.append(som_stappen)

    gegevens = [parameterwaarden,percentages,stappen]
    GenereerCsv(gegevens,str(paraNaam[index]))
    return test, percentages,stappen

DataAnalyse3D()