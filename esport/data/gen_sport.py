import random


def generaDuracio(f, numEvents):
    f.write(f"duracio =         [")

    vectDuracio = []
    for i in range(numEvents):
        r = random.randint(0, 6) % 6 + 1 # random amb el doble de possibilitats per a duracio d'1 (rang (1-6))
        vectDuracio.append(r)
        f.write(f"{r}")
        if i != numEvents-1:
            f.write(', ')

    
    f.write(f"]; % duracio de la prova, en periodes de 15 min\n\n")
    return vectDuracio


def generaPistaOCamp(f, numEvents):
    f.write(f"pistaOcamp =      [")

    for i in range(numEvents):
        r = random.randint(0, 1)
        f.write(f"{r}")
        if i != numEvents-1:
            f.write(', ')

    f.write(f"];  % pista = 0, camp = 1\n\n")

def generaPistaNecessaria(f, numEvents, vectDuracio):
    f.write(f"pistaNecessaria = [")

    for i in range(numEvents):
        r = random.randint(1, 2)
        if vectDuracio[i] >= 4: # si la duracio es de més d'1h (o 1h), es un event que sol necessita mitja pista (o camp)
            r = 1
        f.write(f"{r}")
        if i != numEvents-1:
            f.write(', ')

    f.write(f"]; % 1 si necessiten mitja pista, 2 si la necessiten completa\n\n")


def generaDescans(f, numEvents):
    f.write(f"% descansos despres de fer la prova 1, la fila 1\n")
    f.write(f"descans = [")
    for i in range(numEvents):
        for j in range(numEvents):
            if j == 0:
                f.write(f"| ")

            r = random.randint(0, 5) % 4 + 1 # random amb doble de possibilitats per al 1 i 2 (rang (1-4))
            if i == j:
                r = 0
            f.write(f"{r}")
            if j == numEvents - 1 and i != numEvents - 1:
                f.write(f"\n           ")
            elif j != numEvents - 1:
                f.write(', ')
    
    f.write(" |];\n\n")


def generaParticipantComu(f, numEvents):
    f.write(f"% participant comu a proves 1 i 3 (per tot i, j, sempre i < j per indicar si tenen participant comu)\n")
    f.write(f"participantComu = [")
    for i in range(numEvents):
        for j in range(numEvents):
            if j == 0:
                f.write(f"| ")

            r = random.randint(1, 4) # 25% de possibilitats de tenir participant en comu
            s = ''
            if i >= j:
                s = "false"
            else:
                if r == 1:
                    s = "true "
                else:
                    s = "false"

            f.write(s)
            if j == numEvents - 1 and i != numEvents - 1:
                f.write(f"\n                   ")
            elif j != numEvents - 1:
                f.write(', ')

    f.write(" |];")


def generaSport(id, numEvents):

    for i in range(25):
        idExp = id * 25 + i
        with open(f'sport_{idExp}.dzn', 'w') as f:

            f.write(f"e = {numEvents}; % nombre d'events\n\n")

            vectDuracio = generaDuracio(f, numEvents)

            generaPistaOCamp(f, numEvents)

            generaPistaNecessaria(f, numEvents, vectDuracio)

            generaDescans(f, numEvents)

            generaParticipantComu(f, numEvents)


if __name__ == "__main__":
    #generaSport(id=0, numEvents=20)
    generaSport(id=1, numEvents=40)