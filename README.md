# Descripció dels directoris

Cada carpeta, excepte `results`, conté el fitxer MiniZinc `.mzn`, que és el model corresponent, i una subcarpeta amb els arxius de dades per executar el model. A més, aquesta subcarpeta també conté un arxiu Python amb el qual s'han generat els jocs de prova de cada problema.

## Resultats

A la carpeta `results` hi ha l'arxiu Python que crea gràfiques i resultats (cal obrir-lo i baixar fins a la funció `main` per veure totes les funcions disponibles). Per analitzar els diferents resultats, cal canviar el valor de la variable `carpeta`.

A més, dins la carpeta `results` hi ha quatre subcarpetes, corresponents als outputs de cadascun dels subproblemes. Aquestes carpetes estan identificades pel número d'experiment i el solver utilitzat per a l'execució.
