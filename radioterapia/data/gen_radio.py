import random

def num2str(num):
    if num >= 10:
        return str(int(num))
    return ' '+str(int(num))


def writeSolicitud(f, numPacients):
    f.write('solicitud = [ ')
    for j in range(numPacients):
        diaSolicitud = random.randint(1, 5)
        f.write(str(diaSolicitud))
        if j != numPacients-1:
            f.write(',')
        f.write(' ')
    f.write(f"]; % dia (laborable) en que s'ha fet la solicitud\n\n")


def ordenaMatriuDisponible(matriu, numDies, numLinacs):
    for i in range(numDies): # ordenem la matriu
        disponibleDia = []
        for j in range(numLinacs):
            disponibleDia.append(matriu[j][i])

        disponibleDia.sort()
        for j in range(numLinacs):
            matriu[j][i] = disponibleDia[j]

    return matriu


def generaMatriuDisponible(numLinacs, numDies):
    matriu = []
    for _ in range(numLinacs):
        vector = []
        for j in range(numDies):
            sigma = 5    # desviacio standard
            num = -1
            if j < 5:
                mu = 5
                num = abs(random.gauss(mu, sigma))
            elif j < 10:
                mu = 20
                num = abs(random.gauss(mu, sigma))
            elif j < 15:
                mu = 35
                num = abs(random.gauss(mu, sigma))
            else:
                num = 49
            
            num = max(3, min(49, num)) # 3 <= num <= 49
            vector.append(num)
        matriu.append(vector)
    
    return ordenaMatriuDisponible(matriu, numDies, numLinacs)


def writeDispobible(f, numLinacs, numDies):
    f.write('disponible = [')
    total = 0
    matriu = generaMatriuDisponible(numLinacs, numDies)
    for k in range(numLinacs):
        if k > 0:
            f.write('              ')
        f.write('| ')
        for j in range(numDies):
            num = matriu[k][j]

            total += int(num)
            num = num2str(num)
            f.write(num)
            if j != numDies-1:
                f.write(', ')
            elif k != numLinacs-1:
                f.write('\n')
            else:
                f.write(f' |]; % capacitat de cada linac\n\n')
    return total

# retorna el nombre que tocaria a cada iteracio del patro
# pre: 1 <= nPatro <= 4
def patro(i, numSesions, nPatro):
    if nPatro == 1:
        return 2
    if nPatro == 2:
        return 3
    if nPatro == 3:
        if i <= numSesions / 2:
            return 2
        return 3
    # else
    if i <= numSesions / 2:
        return 3
    return 2


def writeDuracion(f, numPacients, numSesions):
    totsPacients = []
    total = 0
    pacientsPerPatro = {1: 0, 2: 0, 3: 0, 4: 0} # quants pacients hi ha per a cada patro
    for _ in range(numPacients):
        pacient = []
        patroPacient = random.randint(1,4) # 4 possibilitats de patro de duracions
        pacientsPerPatro[patroPacient] += 1
        for n in range(numSesions):
            dur = patro(n, numSesions, patroPacient)
            pacient.append(dur)
            total += dur
        totsPacients.append(pacient)

    totsPacients.sort()
    f.write('duracio = [')
    for j in range(numPacients):
        f.write('| ')
        for k in range(numSesions):
            f.write(str(totsPacients[j][k]))
            if k != numSesions-1:
                f.write(', ')
            elif j != numPacients-1:
                f.write('\n            ')
            else:
                f.write(f' |]; % duracion de la sesion (2 o 3 instants de temps)(30 o 45 mins)\n\n')
    return total, pacientsPerPatro


def generaPatroSeparacio(numSesions):
    p1 = [1, 2, 2, 1]
    p2 = [1, 2, 1, 2]
    p3 = [3, 1, 3, 1]
    m = [p1, p2, p3]

    patrons = []
    for _ in range(3):
        iterFinsFinal = 0
        patro = []
        while iterFinsFinal < numSesions - 1:
            rand = random.randint(0, 2)
            patro.extend(m[rand])
            iterFinsFinal += len(m[rand])
        patrons.append(patro[:numSesions-1])
    
    return patrons


def writeSeparacion(f, numPacients, numSesions, pacientsPerPatro):
    #choices = [1, 2]
    #probabilities = [0.9, 0.1]
    #random_choice = random.choices(choices, probabilities, k=numPacients)
    #llistaString = ', '.join(map(str, random_choice))
    #f.write('separacion = [' + llistaString + ']; % numero de dias que tienen que pasar entre sesion y sesion')
    llistaPacientsPerPatro = list(pacientsPerPatro.values())
    llista = []
    for i in range(len(llistaPacientsPerPatro)):
        llista.extend([i+1]*llistaPacientsPerPatro[i])

    patrons = generaPatroSeparacio(numSesions)
    f.write('separacio = [')
    patronsFinalsPacients = []
    choices = [0, 1]
    probabilities = [0.75, 0.25]
    rand = 0
    for j in range(numPacients):
        if j > 0 and llista[j-1] != llista[j]:
            rand = 0
        f.write('| ')
        random_choice = random.choices(choices, probabilities)[0]
        rand = min(2, rand+random_choice)
        patro = patrons[rand]
        patronsFinalsPacients.append(rand)
        for k in range(numSesions-1):
            f.write(str(patro[k]))
            if k != numSesions-1-1:
                f.write(', ')
            elif j != numPacients-1:
                f.write('\n              ')
            else:
                f.write(f' |]; % separacio ideal entre sesions \n\n')
            
    return patronsFinalsPacients


def writeGrup(f, pacientsPerPatro, patronsSeparacio):
    # 4 patrons de pacients, 3 patrons de separacio: 12 grups possibles diferents
    llistaPacientsPerPatro = list(pacientsPerPatro.values())
    llista = []
    for i in range(len(llistaPacientsPerPatro)):
        llista.extend([i+1]*llistaPacientsPerPatro[i])
    
    llistaGrups = []
    grup = []
    for i in range(len(patronsSeparacio)):
        patroUnit = (patronsSeparacio[i], llista[i])
        if patroUnit not in llistaGrups:
            llistaGrups.append(patroUnit)
        grup.append(llistaGrups.index(patroUnit)+1)
    
    llistaString = ', '.join(map(str, grup))
    f.write('grup = [' + llistaString + ']; % pacients amb mateix grup son identics')


def generaHospital(idHospital, numLinacs, numSesions, numPacients, numDies, tol, sol):
    for i in range(25):
        idExp = idHospital * 25 + i
        with open(f'radio_{idExp}.dzn', 'w') as f:
            f.write(f'\nnumDies = {numDies}; % numero de dies\nm = {numLinacs}; % num linacs\ns = {numSesions}; % num sessions per pacient\np = {numPacients}; % num pacients\n')
            f.write(f'tolerancia = {tol}; % diferencia maxima diaSesio i separacio\nsolicitud = {sol}; % dies maxims fins primera visita\n\n')

            #writeSolicitud(f, numPacients)

            disponibleTotal = writeDispobible(f, numLinacs, numDies)
            
            duracioTotal, pacientsPerPatro = writeDuracion(f, numPacients, numSesions)
            
            patronsSeparacio = writeSeparacion(f, numPacients, numSesions, pacientsPerPatro)

            writeGrup(f, pacientsPerPatro, patronsSeparacio)

            print(f'Disponible - duracio: {disponibleTotal - duracioTotal}')




if __name__ == "__main__":
    generaHospital(idHospital=0, numLinacs=1, numSesions=8, numPacients=15, numDies=20, tol=2, sol=9)
    generaHospital(idHospital=1, numLinacs=3, numSesions=8, numPacients=45, numDies=20, tol=3, sol=14)