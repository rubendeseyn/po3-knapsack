import csv
import matplotlib
import matplotlib.pyplot as plt
import random
import math
import numpy as np
from matplotlib import colors as mcolors
def EvalueerContainer(gevulde_cont,container):
    gebruiktedozen = GebruikteDozenLaag2D(gevulde_cont)
    opp_cont = container[0] * container[1]
    opp_dozen = 0
    for doos in gebruiktedozen:
        opp_dozen += doos[1] * doos[2]
    return opp_dozen / opp_cont

def GebruikteDozenLaag2D(opvulling2D):
    gebr_dozen = []
    for rij in opvulling2D:
        gebr_dozen += GebruikteDozenRij2D(rij)
    return gebr_dozen
def GebruikteDozenRij2D(rij):
    gebr_dozen = []
    for doos in rij:
        if type(doos[0]) == list:
            for x in doos:
                if type(x[0]) == list:
                    for y in x:
                        gebr_dozen.append(y)
                else:
                    gebr_dozen.append(x)
        else:
            gebr_dozen.append(doos)
    return gebr_dozen
def GebruikteDozen3D(opvulling3D):
    gebr_dozen = []
    for laag in opvulling3D:
        gebr_dozen_laag = GebruikteDozenLaag2D(laag)
        gebr_dozen+=gebr_dozen_laag
    return gebr_dozen

def GenereerLatexCode(matrix):
    code=str('\\begin{table}[]'+'\n'+'\\begin{tabular}{|l|l|l|l|l|l|}'+'\n'+'\hline'+'\n')
    for rij in matrix:
        lijn=''
        for element in rij[0:-1]:
            lijn += str(element)+ str('   &    ')
        lijn+= str(rij[-1])+str(' \\\ '+'\hline'+'\n')
        code+=lijn
    code += str('\end{tabular} \n \caption{Kenmerken beginoplossingen} \n\label{tab:waardenbeginopl} \n\end{table}')
    return code
def GenereerCsv(matrix,naam=0):
    with open(str(naam)+".csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(matrix)

def VisualiseerMatrix(lagen,container,naam=1,show=False,procent=False):
    plt.close()
    matrix = VulMatrix(lagen,container)
    fig, ax = plt.subplots()
    maximum = len(matrix)
    if len(matrix[0])>maximum:
        maximum=len(matrix[0])

    min_val, max_val = 0, maximum
    intersection_matrix = matrix
    cmaps = ['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']

    ax.matshow(intersection_matrix, cmap=plt.cm.Blues)
    plt.xlim((0, container[1]))
    plt.ylim((0, container[0]))

    plt.ylabel('lengte')
    plt.xlabel('breedte')
    if procent==True:
        plt.text(5, -7, 'opvullingspercentage '+str(round(EvalueerContainer(lagen,container)*100,2))+'%', bbox=dict(facecolor='white', alpha=0.1))
    plt.savefig('plot' + str(naam) + '.pdf')
    plt.show()
    # for i in range(65):
    #     for j in range(33):
    #         c = intersection_matrix[j][i]
    #         ax.text(i, j, str(c))

def VisualiseerMatrix2(lagen,container,naam=1):
    plt.close()
    matrix = VulMatrix(lagen,container)
    colors = 'white lime red blue magenta yellow black red cadetblue orchid peru olive darkviolet teal firebrick khaki cyan plum violet sienna orangered lawngreen crimson'.split()
    cmap = matplotlib.colors.ListedColormap(colors, name='colors', N=None)
    plt.xlim((0, container[1]))
    plt.ylim((0, container[0]))

    plt.ylabel('lengte')
    plt.xlabel('breedte')

    plt.imshow(matrix, cmap=cmap)
    if naam!='0':
        plt.savefig('plot' + str(naam) + '.pdf')
    plt.show()
    return None

def VulMatrix(lagen, container):
    cont_breedte = container[1]
    cont_hoogte = container[0]
    matrix = []
    totgebr_hoogte = 0  # hou de totaal gebruikte hoogte bij
    for laag in lagen:
        allehoogtesperlaag = []  # kijk wat de hoogste hoogte is per laag
        for doos in laag:
            if type(doos[0])==list:
                pass
                #allehoogtesperlaag.append(sum(hoogtes_samengest))
            else:
                allehoogtesperlaag.append(doos[1])
        hoogte = max(allehoogtesperlaag)
        totgebr_hoogte += hoogte
        huidige_hoogte = 0
        for h in range(hoogte):
            rij = []
            for doos in laag:
                #print('elke rij',huidige_hoogte)
                if type(doos[0]) == list:
                    breedtes_samengest = []
                    hoogtes_samengest = []
                    for x in doos:
                        hoogtes_samengest.append(x[1])
                        breedtes_samengest.append(x[2])
                    #print(hoogtes_samengest)
                    #print(huidige_hoogte)
                    for breedte in range(max(breedtes_samengest)):
                            i=0 #doos van samengest doos

                            while huidige_hoogte+1 > sum(hoogtes_samengest[0:i+1]) and i <len(hoogtes_samengest)+1:
                                i+=1


                            if sum(hoogtes_samengest[0:i+1])- huidige_hoogte > 0:
                                if breedte < breedtes_samengest[i]:
                                    rij.append(doos[i][0])
                                else:
                                    rij.append(0)
                            else:
                                rij.append(0)
                else:
                    for breedte in range(doos[2]):

                        if doos[1] - huidige_hoogte > 0:  # controleer hoogte vd doos tov maximale hoogte vd laag
                            rij.append(doos[0])

                        else:
                            rij.append(0)  # lege ruimte naast doos rechts
            huidige_hoogte += 1
            while len(rij) < cont_breedte:
                rij.append(0)
            matrix.append(rij)

    # voeg lege ruimte toe als nog niet alles gebruikt is in de hoogte
    while totgebr_hoogte < cont_hoogte:
        matrix.append([0] * cont_breedte)
        totgebr_hoogte += 1

    return matrix

def BerekenMaxHoogteLaag3D(laag):
    dozen = GebruikteDozenLaag2D(laag)
    hoogte = 0
    for doos in dozen:
        if type(doos[0])!=int:
           break
        else:
            if doos[3]>hoogte:
                hoogte=doos[3]
    return hoogte

def BerekenMaxLengteRij(rij):
    maxlengte = 0
    for doos in rij:
        if doos[1]>maxlengte:
            maxlengte=doos[1]
    return maxlengte

def plot2D(opvulling3D,container,naam='opl',show=False):
    plt.close()
    i = 1
    for laag in opvulling3D:
        VisualiseerMatrix(laag,container,str(naam)+' laag '+str(i),show=show)
        i+=1

def plot3D(opvulling3D,container,bestandsnaam='',show=True):
    plt.close()
    #positions =
    #sizes =
    #colors = ['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']
    x_pos = []
    y_pos = []
    huidige_hoogte = 0
    z_pos=[0] #y-co eerste laag
    sizes=[]
    for laag in opvulling3D:

        #z_pos+= [z_pos[-1]]*(len(GebruikteDozenLaag2D(laag))-1)
        y_pos2 = [0] #y-co eerste rij
        huidige_rijlengte = 0
        for rij in laag:
            x_pos2 = [0]
            #y_pos2 += [y_pos2[-1]] * (len(rij)-1)
            for doos in rij:
                if type(doos[0]) == list and type(doos[0][0]) == list and type(doos[0][0][0])==int :

                    eindx, eindy, eindz = int(x_pos2[-1] + doos[0][0][2]), int(y_pos2[-1]), int(z_pos[-1])

                    x_pos2 += [x_pos2[-1]] * (len(GebruikteDozen3D([[[doos]]])) - 1)
                    z_pos3 = []
                    z_pos.pop()
                    huidigey = huidige_rijlengte
                    y_pos3 = []
                    for doosy in doos:
                        #print('doosy',doosy)
                        y_pos3 += [huidigey] * (len(doosy))
                        huidigez = int(huidige_hoogte)
                        z_pos4 = []
                        for doosz in doosy:
                            z_pos4 += [huidigez]
                            huidigez += doosz[3]
                            #print('doosz',doosz)

                            afmet = (doosz[2], doosz[1], doosz[3])
                            sizes.append(afmet)
                       # print('z_pos4',z_pos4)
                        z_pos3 += z_pos4
                        huidigey += doosy[0][1]

                    #print('y_pos3', y_pos3
                    y_pos2.pop()
                    y_pos2 += y_pos3
                    #print('z_pos3',z_pos3)
                    z_pos += z_pos3
                    x_pos2.append(x_pos2[-1] + doos[0][0][2])  ##x-co volgende doos
                    y_pos2 += [eindy]
                    z_pos += [eindz]

                elif type(doos[0])==list and doos[0][4]=='z':
                    eindx, eindy, eindz = int(x_pos2[-1] + doos[0][2]), int(y_pos2[-1]), int(z_pos[-1])
                    x_pos2 += [x_pos2[-1]] * (len(doos)-1)
                    y_pos += [y_pos2[-1]] * (len(doos))  # incl laatste teveel

                    huidigez = z_pos[-1] + doos[0][3]
                    for doosz in doos:
                        z_pos += [huidigez]
                        huidigez += doosz[3]
                        afmet = (doosz[2], doosz[1], doosz[3])
                        sizes.append(afmet)
                    z_pos.pop()
                    z_pos += [eindz]  # juist voor volgende doos
                    x_pos2 += [eindx]  # juist voor volgende doos

                elif type(doos[0])==list and doos[0][4]=='y':

                    eindx,eindy,eindz = int(x_pos2[-1]+doos[0][2]),int(y_pos2[-1]),int(z_pos[-1])
                    x_pos2 += [x_pos2[-1]] * (len(doos)-1)
                    z_pos += [z_pos[-1]] * (len(doos)) #incl laatste teveel

                    huidigey = y_pos2[-1]+doos[0][1]
                    for doosx in doos:
                        y_pos2 += [huidigey]
                        huidigey += doosx[1]
                        afmet = (doosx[2], doosx[1], doosx[3])
                        sizes.append(afmet)
                    y_pos2.pop()
                    y_pos2 += [eindy] #juist voor volgende doos
                    x_pos2 += [eindx] #juist voor volgende doos


                elif type(doos[0])==int:
                    z_pos += [z_pos[-1]] #z-co volgende doos
                    x_pos2.append(x_pos2[-1]+doos[2]) #x-co volgende doos
                    y_pos2 += [y_pos2[-1]] #nieuw y-co volgende doos
                    afmet = (doos[2],doos[1],doos[3])
                    sizes.append(afmet)
                else:
                    print(NotImplementedError)
            x_pos2.pop() #laatste x-coordinaat wordt niet gebruikt want geen volgende doos
            y_pos2.pop() #laatste y-co wordt niet gebruikt
            x_pos += x_pos2

            rijplus = rij[0][1]
            y_pos2 += [huidige_rijlengte+ rij[0][1]]  # y-co volgende rij
            huidige_rijlengte += rijplus

        y_pos2.pop() #laatste y-coordinaat wordt niet gebruikt want geen volgende rij
        y_pos += y_pos2
        z_pos.pop()

        hoogteplus =int(BerekenMaxHoogteLaag3D(laag))
        z_pos += [huidige_hoogte + hoogteplus] #z-co-volgende laag !!!!pasop
        huidige_hoogte +=hoogteplus
    z_pos.pop() #laatste z-coordinaat wordt niet gebruikt want geen nieuwe laag
    positions = []
    # print(sizes)
    # print('x_pos',x_pos)
    # print('y_pos',y_pos)
    # print('z-pos',z_pos)
    for i in range(len(x_pos)):
        positions.append((x_pos[i],y_pos[i],z_pos[i]))

    #print(positions)
    #positions = [(-3, 5, -2), (1, 7, 1)]
    #sizes = [(4, 5, 3), (3, 3, 7)]
    #colors = ["crimson", "limegreen"]


    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    #colors = 'white lime red blue magenta yellow black red cadetblue orchid peru olive darkviolet teal firebrick khaki cyan plum violet sienna orangered lawngreen crimson'.split()


    fig = plt.figure()
    ax = fig.gca(projection='3d')
   # ax.set_aspect('equal')


    for p, s, c in zip(positions, sizes, colors):
        plotCubeAt(pos=p, size=s, ax=ax, color=c)
    ax.set_xlim3d(0, container[1])
    ax.set_ylim3d(0, container[0])
    ax.set_zlim3d(0, container[2])
    ax.set_xlabel('lengte')
    ax.set_ylabel('breedte')
    ax.set_zlabel('hoogte')
    # yint = range(min(y_pos), math.ceil(max(y_pos)) + 1)
    # matplotlib.pyplot.yticks(yint)
    # xint = range(min(x_pos), math.ceil(max(x_pos)) + 1)
    # matplotlib.pyplot.yticks(xint)
    # zint = range(min(z_pos), math.ceil(max(z_pos)) + 1)
    # matplotlib.pyplot.yticks(zint)
    if show==True:
        plt.show()
    plt.close()

def cuboid_data(o, size=(1,1,1)):
    # code taken from
    # https://stackoverflow.com/a/35978146/4124317
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1], o[1], o[1]],
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]
    z = [[o[2], o[2], o[2], o[2], o[2]],
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]
    return np.array(x), np.array(y), np.array(z)

def plotCubeAt(pos=(0,0,0), size=(1,1,1), ax=None,**kwargs):
    # Plotting a cube element at position pos
    if ax !=None:
        X, Y, Z = cuboid_data( pos, size )
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)

