include "globals.mzn";
set of int: HORA = 1..60; % numero de tandes en un dia (de 15 minuts (per exemple, des de les 7 del mati fins les 11 de la nit))

                          
int: m = 2;                  % numero de recursos (2, tenim 2 mitges pista o camp)

int: e;                      % nombre de proves
set of int: PROVA=1..e;


array[PROVA] of int: duracio;                  % duracio de la prova
array[PROVA] of 0..1: pistaOcamp;              % pista = 0, camp = 1
array[PROVA] of 1..2: pistaNecessaria;         % 1 si necessita mitja pista, 2 si la necessita completa
array[PROVA,PROVA] of int: descans;            % temps que s'ha d'descansar despres d'una prova determinada
array[PROVA,PROVA] of bool: participantComu; 

array[PROVA] of var HORA: hora;                % hora d'inici de la prova
var HORA: makespan;

% constraint cumulative
constraint forall(pc in 0..1)(
            cumulative(
              [ hora[p]            | p in PROVA where pistaOcamp[p] = pc ],
              [ duracio[p]         | p in PROVA where pistaOcamp[p] = pc ],
              [ pistaNecessaria[p] | p in PROVA where pistaOcamp[p] = pc ],
              m 
              ));

% non-overlap de proves que tenen participants en comu

constraint forall(p1 in PROVA)(forall(p2 in PROVA where p1 < p2 /\ participantComu[p1, p2] = true)
                                        (cumulative( % non-overlap
                                                     [ hora[p1]                     , hora[p2]                      ],
                                                     [ duracio[p1] + descans[p1, p2], duracio[p2] + descans[p2, p1] ],
                                                     [ 1                            , 1                             ],
                                                     1
                                                     )));                                         

% no pots començar una prova i que no doni temps a acabar-la
constraint forall(p in PROVA)((hora[p] + duracio[p] - 1) <= max(HORA));


% variable a minimitzar, minimitzar l'hora maxima en que acaba una prova
constraint forall(p in PROVA)(makespan >= hora[p] + duracio[p]);
solve::restart_luby(10)
    minimize makespan;


output ["hora = "] ++ [show(hora)] ++ [";\n\n"];
output ["obj = "] ++ [show(makespan)] ++ [";\n"];