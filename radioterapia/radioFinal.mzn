include "globals.mzn";
int: numDies;
set of int: DIA=1..numDies; % dies totals
int: m;    % nombre de recursos (LINACS)
set of int: SALA = 1..m;    % conjunt de LINACs
int: p;    % nombre de nous pacients
set of int: PACIENT=1..p;   % conjunt de pacients
int: s;    % sessions per tanda
set of int: SESSIO=1..s;    % conjunt de sessions
int: solicitud;             % maxim de dies que poden passar fins la 1ra visita
int: tolerancia;            % limit màxim que ens podem allunyar de la separació ideal
set of int: MAXSEP = 0..tolerancia*s;

% duracio de la sessió
%les files de duracio estan ordenades lexicograficament per a que els pacients identics estiguin seguits
array[PACIENT,SESSIO] of int: duracio; 
% nombre de dies que idealment han de passar entre la sessió anterior i l'actual
array[PACIENT,1..s-1] of int: separacio; 
% si grup[p]=grup[p+1] els pacients p i p+1 son identics
array[PACIENT] of int: grup; 
% disponibilitat de cada linac, cada dia.
%les files estan ordenades decrexientment per a que puguem identificar linacs que un dia determinat son identics
array[SALA, DIA] of int: disponible;

array[PACIENT,SESSIO] of var DIA: dia;
array[PACIENT,SESSIO] of var SALA: sala;

%identificador del pacient més petit que fa servir el linac aquest dia
array[SALA,DIA] of var PACIENT: minPac; 
array[PACIENT,SESSIO] of var DIA: limitInf;
array[PACIENT,SESSIO] of var DIA: limitSup;
array[PACIENT] of var MAXSEP: separacioTotal;
var int: obj;                                 % valor objectiu a minimitzar


%ens guardem el mínim i màxim bounds per a cada sessió
constraint forall(pac in PACIENT)(forall(ses in SESSIO)
      (if ses = 1 then
          limitInf[pac,ses] = 1 /\ limitSup[pac,ses] = solicitud
       else
          limitInf[pac,ses] = 
            max(1,
                limitInf[pac,ses-1] + separacio[pac,ses-1] - tolerancia)
          /\
          limitSup[pac,ses] = 
            min(numDies,
                limitSup[pac,ses-1] + separacio[pac,ses-1] + tolerancia)
       endif));
                                                         
%restringim els dies en els que es poden fer les sessions amb els bounds
constraint forall(pac in PACIENT)(forall(ses in SESSIO)
      (dia[pac,ses] >= limitInf[pac,ses] /\
       dia[pac,ses] <= limitSup[pac,ses]
      ));

%les sessions es fan en dies creixents
constraint forall(pac in PACIENT)(increasing([dia[pac,ses] | ses in SESSIO]));

%dia primera visita maxim 'solicitud' dies despres
%constraint forall(pac in PACIENT)(dia[pac, 1] <= solicitud);

%les sessions no es poden allunyar massa de la separació ideal
constraint forall (pac in PACIENT, ses in 1..s-1)
    (abs(dia[pac,ses+1]-dia[pac,ses]-separacio[pac,ses]) <= tolerancia);
    
% els linacs tenen prou capacitat
constraint forall(l in SALA, d in DIA)
     (sum(pac in PACIENT, ses in SESSIO where dia[pac,ses]=d /\ sala[pac,ses] = l)
         (duracio[pac,ses])
          <= 
          disponible[l,d]);
    
% simetria de pacients identics
constraint forall(pac in 1..p-1 where grup[pac]=grup[pac+1])
  (lex_greatereq([dia[pac,ses]| ses in SESSIO],[dia[pac+1,ses]| ses in SESSIO]));
  
     
% minPac pren el valor que li correspont
% assumeix que no hi ha linacs buits
constraint forall(l in SALA, d in DIA)
  (minPac[l,d]= min(pac in PACIENT, ses in SESSIO 
                    where sala[pac,ses]=l /\ dia[pac,ses]=d)(pac));

% simetria de linacs que son identics en dies determinats
constraint forall(l in 1..m-1, d in DIA)
  (disponible[l,d] = disponible[l+1,d] -> minPac[l,d] < minPac[l+1,d]);

% separació total
constraint forall(pac in PACIENT)
 (separacioTotal[pac] = 
  sum([ abs(dia[pac, ses+1]-(dia[pac, ses]+separacio[pac, ses])) | ses in 1..s-1]));

constraint obj = max([separacioTotal[pac] | pac in PACIENT]);
solve :: restart_luby(10)                                              %:: int_search(dia, smallest, indomain_min)
      minimize obj;

output [
  "diaSesion = \n"] ++ 
  [ show(dia[pac, ses]) ++ if ses == max(SESSIO) then "\n" else " " endif
    | pac in PACIENT, ses in SESSIO ] 
  ++ [";\n"];

output ["SalaDia = "] ++ [show(sala)] ++ [";\n"];
output ["obj = "] ++ [show(obj)] ++ [";\n"];