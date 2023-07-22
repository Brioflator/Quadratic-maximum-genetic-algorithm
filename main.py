import copy
import random
import math



#functia de maximizat, coeficientii fiind cititi la input
def functionResult(x, c): #calc polinomul de grad 2
    return c[0]*(x**2) + c[1]*x + c[2]

def binarySearchIntervals(u, vctr, st, dr): #cautarea binara pentru a gasi intervalul potrivit pentru un u dat
    global last #last este ultimul interval in care se afla u
    while st <= dr:
        mij = (st + dr) // 2
        if vctr[mij] <= u:
            last = mij
            st = mij+1
        elif vctr[mij] > u:
            dr = mij-1
    return last+1

f = open("Evolutie.txt", "w")


n = int(input("Dim populatiei = "))
print("Domeniul de def al functiei:")
a = int(input("a = "))
b = int(input("b = "))
print("Parametrii pentru functia de maximizat: ", end=" ")

coeficients = [int(x) for x in input().split()]
precision = int(input("Precizia = "))
pc = float(input("Probabilitatea de recombinare = "))
pm = float(input("Probabilitatea de mutatie = "))
stages = int(input("Numarul de etape = "))



#formula din curs pentru discretizarea intervalului si calculul lungimii cromozomului
dimC = math.ceil(math.log2((b-a)*(10**precision))) #dimensiunea cromozomului (numarul de biti)
chromosomes = [[random.randint(0, 1) for j in range(dimC)] for i in range(n)] #initial generam fiecare gena aleator

# conditia de terminare, in acest caz numarul de etape
for stage in range(1, stages+1):

    if stage == 1:
        f.write("Populatia initiala\n")
        f.write("reprezentarea pe biti a cromozomilor, valoarea reala a lui x, val fct de maximizat\n")

    sumF = 0 # suma val fct de maximizat pentru toti cromozomii
    X = [] # lista de val reale a lui x pentru toti cromozomii
    maxfittest = float('-inf') # cel mai fittest cromozom
    fittest = 0
    for i in range(n):
        b2str = ''.join([str(x) for x in chromosomes[i]]) #transform cromozomul intr-un sir de biti
        x = int(b2str, 2) #transform sirul de biti in baza 10

        interpolate_x = ((b - a) / (2 ** dimC - 1)) * x + a #formula din curs pentru valoarea codificata a unui cromozom (interpolarea sa pe D)
        X.append(interpolate_x) #salvez toti x's corespunzatori cromozomilor

        if stage == 1:
            f.write(str(i + 1) + ": " + b2str + " x= " + str(round(interpolate_x, precision)) + " f= " + str(functionResult(round(interpolate_x, precision), coeficients)) + "\n")

        sumF += functionResult(interpolate_x, coeficients)

        # calculez cel mai fit cromozom sa l trec direct in etapa urmatoare
        if functionResult(round(interpolate_x, precision), coeficients) > maxfittest:
            maxfittest = functionResult(round(interpolate_x, precision), coeficients)
            fittest = i

    fittest_chromosome = chromosomes[fittest].copy()

    if stage == 1:
        f.write("\nProbabilitati selectie\n")
    probability_selection = []
    for i in range(n):
        probability_selection.append(functionResult(X[i], coeficients) / sumF) #probabilitatile de selectie prin metoda ruletei
        if stage == 1:
            f.write("cromozom " + str(i + 1) + " probabilitate " + str(functionResult(X[i], coeficients) / sumF) + "\n")

    if stage == 1:
        f.write("\nIntervale probabilitate selectie\n")
    intervals_probability_selection = [0]
    sumI = probability_selection[0]
    intervals_probability_selection.append(sumI)
    if stage == 1:
        f.write("0 " + str(sumI) + " ")
    for i in range(1, n):
        sumI += probability_selection[i]
        intervals_probability_selection.append(sumI) # calculam intervalele ca fiind suma a probabilitatilor anterioare
        if stage == 1:
            f.write(str(sumI) + " ")


    if stage == 1:
        f.write("\n")
    selected = [0 for _ in range(n)]
    for i in range(n):
        u = random.random() #generez un u random pe care il caut binar in lista de probabilitati de selectie
        crmz = binarySearchIntervals(u, intervals_probability_selection, 0, n) - 1 # cromozomul care participa la recombinare
        if stage == 1:
            f.write("u= " + str(u) + " selectam cromozomul " + str(crmz + 1) + "\n")
        selected[i] = crmz #ma folosesc de selected pentru a vedea ce cromozomi trec de selectie

    if stage == 1:
        f.write("\nDupa selectie: \n")
    cc = [] #lista de cromozomi care trec de selectie
    for i in range(n):
        if stage == 1:
            f.write(str(i + 1) + ": " + ''.join([str(x) for x in chromosomes[selected[i]]]) + " x= " + str(round(X[selected[i]], precision)) + " f= " + str(functionResult(X[selected[i]], coeficients)) + "\n")
        cc.append(chromosomes[selected[i]])
    chromosomes = copy.deepcopy(cc) #copiez toti cromozomii care au trecut de selectie in lista initiala chromosomes si trec mai departe

    if stage == 1:
        f.write("\nProbabilitatea de recombinare " + str(pc) + "\n")
    recombined = []
    for i in range(n):
        u = random.random() #generez un u random
        if u < pc: #daca acest u este mai mic decat probabilitatea de incrucisare trec indicele cromozomului intr-un vector
            if stage == 1:
                f.write(str(i + 1) + ": " + ''.join([str(x) for x in chromosomes[i]]) + " u= " + str(u) + "<" + str(pc) + " participa\n")
            recombined.append(i)
        else:
            if stage == 1:
                f.write(str(i + 1) + ": " + ''.join([str(x) for x in chromosomes[i]]) + " u= " + str(u) + "\n")

    if stage == 1:
        f.write('\n')
    while len(recombined) > 1: #recombined = lista de indici!
        i = random.randrange(len(recombined)) #iau un i random si un j tot la fel de radom si incrucisez cromozomii recombined[i] recombined[j]
        j = len(recombined) - i - 1
        if i == j:
            continue
        if stage == 1:
            f.write("Recombinare dintre cromozomul " + str(recombined[i] + 1) + " cu cromozomul " + str(recombined[j] + 1) + ": \n")

        pct = random.randrange(dimC) #punctul de la care se realizeaza incrucisarea
        if stage == 1:
            f.write(''.join([str(x) for x in chromosomes[recombined[i]]]) + " " + ''.join([str(x) for x in chromosomes[recombined[j]]]) + " punct " + str(pct) + "\n")
        # incrucisarea se face prin interschimbarea cromozomilor de la pct incolo
        crmz_copy = chromosomes[recombined[i]][:pct + 1].copy() #incrucisarea
        chromosomes[recombined[i]][:pct + 1] = chromosomes[recombined[j]][:pct + 1].copy()
        chromosomes[recombined[j]][:pct + 1] = crmz_copy.copy()
        if stage == 1:
            f.write("Rezultat " + ''.join([str(x) for x in chromosomes[recombined[i]]]) + " " + ''.join([str(x) for x in chromosomes[recombined[j]]]) + "\n")

        aux = [recombined[k] for k in range(len(recombined)) if k != i and k != j] #elimin indicii i si j din recomb
        recombined = aux.copy()

    if stage == 1:
        f.write("\nDupa recombinare: \n")
    for i in range(n):
        b2str = ''.join([str(x) for x in chromosomes[i]])
        x = int(b2str, 2)
        interpolate_x = ((b - a) / (2 ** dimC - 1)) * x + a #caluclez din nou valorile x pentru noii cromozomi
        X[i] = interpolate_x
        if stage == 1:
            f.write(str(i + 1) + " : " + b2str + " x= " + str(round(interpolate_x, precision)) + " f= " + str(functionResult(round(interpolate_x, precision), coeficients)))
            f.write('\n')

    if stage == 1:
        f.write("\nProbabilitate de mutatie pentru fiecare gena " + str(pm) + "\n")
        f.write("Au fost modificati cromozomii:\n")
    for i in range(n):
        u = random.random() #generez un u random si pentru cromozomii cu u<probabilitatea de mutatie, schimb un bit de pe pozitia poz care e si ea generata random
        if u < pm:
            poz = random.randrange(dimC)
            chromosomes[i][poz] = 1-chromosomes[i][poz]
            if stage == 1:
                f.write(str(i + 1) + "\n")

    if stage == 1:
        f.write("\nDupa mutatie:\n")
    Max = float('-inf') #valoarea cea mai buna
    worstVal = float('inf') #valoarea cea mai proasta
    worst = 0 #cel mai prost cromozom
    medValSum = 0 #suma valorilor medii
    for i in range(n):
        b2str = ''.join([str(x) for x in chromosomes[i]])
        x = int(b2str, 2)
        interpolate_x = ((b - a) / (2 ** dimC - 1)) * x + a #la final recalculez din nou valorile x dupa mutatii
        X[i] = interpolate_x
        if stage == 1:
            f.write(str(i + 1) + " : " + b2str + " x= " + str(round(interpolate_x, precision)) + " f= " + str(functionResult(round(interpolate_x, precision), coeficients))+"\n")
        Max = max(Max, functionResult(round(interpolate_x, precision), coeficients)) #valoarea maximizata a functiei
        medValSum += functionResult(round(interpolate_x, precision), coeficients) #ajuta la calculul valorii medii a performantei
        if functionResult(round(interpolate_x, precision), coeficients) < worstVal: #totodata vreau sa vad cromozomul cu worst performance pentru a-l inlocui cu cel mai fittest pe care l-am ales la inceput
            worstVal = functionResult(round(interpolate_x, precision), coeficients) #deoarece folosim selectia de tip elitist, cel mai fittest trece automat mai departe
            worst = i

    chromosomes[worst] = fittest_chromosome.copy() #inlocuiesc cel mai prost cromozom cu cel mai fittest
    Max = max(Max, maxfittest)  #maximul dintre cel mai fittest si cel mai bun cromozom din populatie dupa mutatii
    medValSum = medValSum - worstVal + maxfittest #calculez noua valoare medie a performantei

    if stage == 1:
        f.write("\n\nEvolutia maximului\n")
    f.write("MaxValue = " + str(Max) + "       Medium Performance: " + str(medValSum / n) + "\n")

f.close()