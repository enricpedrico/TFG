include "globals.mzn";
set of int: HORA = 1..6;                           % assignatures en un dia
set of int: DIA = 1..5;                            % dies de la setmana escolars
set of int: HORAGENERAL = 1..max(HORA)*max(DIA);   % hora de la setmana

int: as;                     % nombre d'assignatures total (multiple de 30)
set of int: ASSIG=1..as;     % totes les assignatures, 1r i 2na hora incloses
int: t;
set of int: TIPUSAULA=1..t;  % aula normal, laboratori, pavello

array[TIPUSAULA] of int: nombreAules; % [nombre d'aules normals, nombre de labs, nombre de pavellons]
array[ASSIG] of TIPUSAULA: tipusAula; % 1 = aula normal, 2 = pavello, 3 = laboratori
array[ASSIG] of int: prof;            % professor que dona una assignatura en una assignatura
array[ASSIG] of int: curs;            % quin curs fa cada assignatura
array[ASSIG] of int: assigIgual;      % quina assignatura es (sense separar per hores)

array[ASSIG] of var HORA: hora;
array[ASSIG] of var DIA: dia;
array[ASSIG] of var HORAGENERAL: horaGeneral;

% lligar horaGeneral
constraint forall(a in ASSIG)
              (horaGeneral[a] = hora[a] + max(HORA)*(dia[a]-1));

% no es supera el nombre d'aules, laboratoris i pavellons cada hora  
constraint forall(aula in TIPUSAULA)(
            cumulative([horaGeneral[a] | a in ASSIG where tipusAula[a] = aula],
                       [1              | a in ASSIG where tipusAula[a] = aula],
                       [1              | a in ASSIG where tipusAula[a] = aula],
                       nombreAules[aula]
                       ));

% no es pot fer la mateixa assignatura 2 cops el mateix dia
constraint forall(i,j in ASSIG where i != j /\ assigIgual[i] = assigIgual[j])
                 (dia[i] != dia[j]);
                  
% els professors no poden estas a dos llocs alhora
constraint forall(i,j in ASSIG where i != j /\ prof[i] = prof[j])(
                 cumulative( % non-overlap
                             [ horaGeneral[i], horaGeneral[j] ],
                             [ 1             , 1              ],
                             [ 1             , 1              ],
                             1
                             ));
                                                                        % una classe no pot fer dos assignatures alhora
constraint forall(i,j in ASSIG where i != j /\ curs[i] = curs[j])(
                 cumulative( % non-overlap
                             [ horaGeneral[i], horaGeneral[j] ],
                             [ 1             , 1              ],
                             [ 1             , 1              ],
                             1
                             ));
     
                                      
solve::restart_luby(10)
    satisfy;


output ["hora = "] ++ [show(hora)] ++ [";\n"];
output ["dia = "] ++ [show(dia)] ++ [";\n"];