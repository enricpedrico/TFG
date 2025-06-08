import random


def generaNpMax(f, numSlots, minPapersXSlot, maxParSessions):
    f.write(f"npMax = [")
    obligatoris = [minPapersXSlot]
    while max(obligatoris) < 6:
        obligatoris.append(obligatoris[-1]+1)

    restants = [random.randint(minPapersXSlot, 6) for _ in range(numSlots - len(obligatoris))]

    randoms = obligatoris + restants
    random.shuffle(randoms)

    for i in range(numSlots):
        r = randoms[i]

        f.write(f"{r}")
        if i != numSlots-1:
            f.write(', ')

    
    f.write(f"]; % nombre maxim de papers per slot\n\n")
    return sum(randoms)*maxParSessions

def generaNp(f, numSessions, totalDuracio):
    f.write(f"np = [")
    np = []
    for i in range(numSessions):
        r = random.randint(3,20)
        np.append(r)

    suma = sum(np)
    while totalDuracio*0.7 < suma:
        r = random.randint(0, len(np)-1)
        if np[r] > 3:
            np[r] -= 1
            suma -= 1
    
    for i in range(numSessions):
        f.write(f"{np[i]}")
        if i != numSessions-1:
            f.write(', ')

    print(np)
    f.write(f"]; % nombre de papers acceptats a cada sessio\n\n")


def generaWG(f, numWG, numSessions):
    f.write(f"WG = [ ")
    wg = 1
    for i in range(numSessions):
        teWG = random.randint(1,10)
        s = '{'
        if teWG > 3:
            r = wg
            wg = 1 + wg % numWG
            s = s + str(r)
            if teWG > 8:
                r = wg
                wg = 1 + wg % numWG
                s = s + ',' + str(r)
                if teWG > 9:
                    r = wg
                    wg = 1 + wg % numWG
                    s = s + ',' + str(r)


        s = s + '}'
        f.write(s)
        if i != numSessions-1:
            f.write(', ')

    
    f.write(f" ]; % grups per sessio\n\n")


def generaCongres(id, numSessions, numWG, numSlots, minPapersXSlot, maxParSessions):

    for i in range(25):
        idExp = id * 25 + i
        with open(f'congres_{idExp}.dzn', 'w') as f:

            f.write(f"\nse = {numSessions}; % nombre de sessions\n")
            f.write(f"gr = {numWG}; % nombre de grups de treball\n")
            f.write(f"cl = {numSlots}; % nombre de slots\n")
            f.write(f"minPapersPerSlot = {minPapersXSlot}; % minim nombre d'articles per sessio i slot\n")
            f.write(f"maxSesionsPar = {maxParSessions}; % maxim nombre de sessions paraleles\n\n")

            totalDuracio = generaNpMax(f, numSlots, minPapersXSlot, maxParSessions)

            generaNp(f, numSessions, totalDuracio)

            generaWG(f, numWG, numSessions)



if __name__ == "__main__":
    generaCongres(id=0, numSessions=40, numWG=20, numSlots=7, minPapersXSlot=3, maxParSessions=14) # roadef2024
    generaCongres(id=1, numSessions=80, numWG=40, numSlots=12, minPapersXSlot=3, maxParSessions=20)