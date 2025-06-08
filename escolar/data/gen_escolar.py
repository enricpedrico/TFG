import random


def generaTipusAula(f, nAssig):
    f.write(f"tipusAula = [")
    for i in range(nAssig):
        if i % 30 < 2: # educacio fisica
            f.write('3')
        elif i % 30 == 2:
            f.write('2')
        else:
            f.write('1')

        if i != nAssig-1:
            f.write(', ')

    f.write(f"]; % 1 = aula normal, 2 = laboratori, 3 = pavello\n\n")


#def generaProf(f, nAssig, promocionsPerCurs):
#    f.write(f"prof =      [")
#    curs = []
#    act = 0
#    for i in promocionsPerCurs:
#        for _ in range(i):
#            curs.append(act)
#        act += 1
#
#    newProf = 2
#    profs = []
#    for i in range(nAssig):
#        #numAssig = i % 30
#        
#        if i < 2:
#            f.write('1')
#            profs.append(1)
#        else:
#            if i % 2 == 0:
#                if i < 30:
#                    f.write(f'{newProf}')
#                    profs.append(newProf)
#                    newProf += 1
#                else:
#                    r = random.randint(1, 10)
#                    cursAct = i // 30
#                    cota = 3
#                    if curs[cursAct] == curs[cursAct-1]:
#                        cota = 1
#
#                    if r > cota and profs.count(profs[i-30]) <= 22:
#                        f.write(f'{profs[i-30]}')
#                        profs.append(profs[i-30])
#                    else:
#                        f.write(f'{newProf}')
#                        profs.append(newProf)
#                        newProf += 1
#                    
#            else:
#                f.write(f'{profs[i-1]}')
#                profs.append(profs[i-1])
#                
#        
#        if i != nAssig-1:
#            f.write(', ')
#    #copsProf = []
#    #for j in range(max(profs)+1):
#    #   copsProf.append(profs.count(j))
#    
#    #print(copsProf)
#    print((max(profs),sum(promocionsPerCurs)))
#    f.write(f"];\n\n")

def generaProf(f, nAssig, promocionsPerCurs):
    f.write(f"prof =      [")
    professors = [0] * nAssig
    
    asig_per_curs = 30
    total_cursos = sum(promocionsPerCurs)
    
    num_profesors = 2 * total_cursos
    profesors_disponibles = list(range(1, num_profesors + 1))
    
    asig_actual = 0
    
    for nivell_curs, num_promocions in enumerate(promocionsPerCurs):
        for promocio in range(num_promocions):
            professors_curs_actual = set()
            
            for asig_en_curs in range(0, asig_per_curs, 2):
                profesor_disponible = None
                intents = 0
                max_intents = 100
                
                while profesor_disponible is None and intents < max_intents:
                    profesor_candidat = random.choice(profesors_disponibles)
                    if profesor_candidat not in professors_curs_actual:
                        profesor_disponible = profesor_candidat
                        professors_curs_actual.add(profesor_candidat)
                    intents += 1
                
                if profesor_disponible is None:
                    profesor_disponible = random.choice(profesors_disponibles)
                
                if asig_actual < nAssig:
                    professors[asig_actual] = profesor_disponible
                if asig_actual + 1 < nAssig:
                    professors[asig_actual + 1] = profesor_disponible
                
                asig_actual += 2
    
    for i in range(nAssig):
        prof = professors[i]
        f.write(str(prof))

        if i != nAssig-1:
            f.write(', ')

    print(comptaAssignacions(professors, num_profesors))
    f.write(f"];\n\n")
    return

def comptaAssignacions(profes, nProfesors):
    cops = [0] * nProfesors

    for profe in profes:
        if profe != -1:
            cops[profe-1] += 1

    return cops

def generaCurs(f, nAssig):
    f.write(f"curs =      [")
    for i in range(nAssig):
        curs = i // 30
        f.write(str(curs))

        if i != nAssig-1:
            f.write(', ')

    f.write(f"];\n\n")

def generaAssigIgual(f, nAssig):
    f.write(f"assigIgual =[")
    for i in range(nAssig):
        assig = i // 2
        f.write(str(assig))

        if i != nAssig-1:
            f.write(', ')

    f.write(f"];\n\n")

def generaEscolar(id, promocionsPerCurs, nombreAules):

    for i in range(25):
        idExp = id * 25 + i
        with open(f'escolar_{idExp}.dzn', 'w') as f:

            classesPerSetmana = 30 # 5 dies x 6 h/dia
            nAssig = classesPerSetmana * sum(promocionsPerCurs)
            f.write(f"\nas = {nAssig}; % nombre d'assignatures total\n")
            f.write(f"\nt = {len(nombreAules)}; % nombre d'aules diferents\n")
            f.write(f"nombreAules = {nombreAules}; % nombre d'aules per tipus\n\n")

            generaTipusAula(f, nAssig)

            generaProf(f, nAssig, promocionsPerCurs)

            generaCurs(f, nAssig)

            generaAssigIgual(f, nAssig)



if __name__ == "__main__":
    generaEscolar(id=0, promocionsPerCurs=[2,2,2,2],     nombreAules = [8,1,1] ) # 1rA, 1rB, 2nA, ...
    generaEscolar(id=1, promocionsPerCurs=[4,4,4,4,2,2], nombreAules = [20,2,2]) # 1rA, 1rB, 1rC, ...