include "globals.mzn";

int: se;               % nombre de sessions
set of int: S=1..se;

int: gr;               % nombre de grups de treball
set of int: G=1..gr;

int: cl;               % nombre de slots
set of int: C=1..cl;

int: minPapersPerSlot;     % minim nombre d'articles per sessio i slot
int: maxSesionsPar;        % maxim nombre de sessions paral·leles

array[S] of int: np;      % nombre de papers acceptats a cada sessio
array[C] of int: npMax;   % nombre maxim de papers per slot
array[S] of set of G: WG; % nombre de grups de treball per sessio

array[C,S] of var 0..max(npMax): papersPerSesSlot;     % quants articles per cada sessio i slot es fan
array[C,G] of var 0..se: copsPerSlot;                  % quants cops apareix un grup per a cada slot

var int: nConflicts;                                   % nombre de conflictes

% per cada sessio i slot, el nombre d'articles que es fan, o esta en el rang minMax, o és 0
constraint forall(s in S)(forall(c in C)(
              (minPapersPerSlot <= papersPerSesSlot[c,s] 
              /\ papersPerSesSlot[c,s] <= npMax[c])
              
              \/
              0 = papersPerSesSlot[c,s]));

% s'han de presentar tots els articles
constraint forall(s in S)
            (np[s] = sum([papersPerSesSlot[c,s] | c in C]));

% no es pot superar el maxim de sessions paral·leles per slot
constraint forall(c in C)(
              sum([1 | s in S where papersPerSesSlot[c,s] > 0])
              <= maxSesionsPar
              );

% guardem els cops per slot de cada grup
constraint forall(c in C)(forall(g in G)(
        copsPerSlot[c,g] = 
            sum([1 | s in S where papersPerSesSlot[c,s] > 0 /\ g in WG[s]])
        ));


% els conflictes de cada grup, cada slot, son n*(n-1)/2, on n es els cops que apareix el grup en l'slot
constraint nConflicts = sum([(copsPerSlot[c,g]*(copsPerSlot[c,g]-1)) div 2
                             | c in C, g in G]);
solve::restart_luby(10)
    minimize nConflicts;

output [
  "papersPerSesSlot:\n",
  "  Sessio " ++ concat([ show(s) ++ " " | s in S ]) ++ "\n"
] ++
[
  "Slot " ++ show(c) ++ ": " ++
  concat([ show(papersPerSesSlot[c,s]) ++ " " | s in S ]) ++ "\n"
  | c in C
];

output ["obj = "] ++ [show(nConflicts)] ++ [";\n"];