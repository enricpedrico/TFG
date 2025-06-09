import os
import matplotlib.pyplot as plt
import numpy as np
import statistics
import seaborn as sns
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

def extractSolver(s):
    return s[7:7+s[7:].find('_')]

def extractNumExp(s):
    return int(s[len(s)-s[::-1].find('_'):s.find('.')])

def extractObjValue(s):
    return int(s[2+s.find('='):s.find(';')])

def extractTime(s):
    return float(s[2+s.find(':'):-2])

def rearrengeExps(d):
    solvers = ['chuffed','cp-sat','highs','coin','gecode']
    for solver in solvers:
        secPart = d[solver][25:50]
        thirdPart = d[solver][50:]
        d[solver] = d[solver][:25] + thirdPart + secPart

    return d


def extractData(nExps, carpeta):
    dTimes = {'chuffed': [-1]*nExps, 'cp-sat': [-1]*nExps, 'highs': [-1]*nExps, 'coin': [-1]*nExps, 'gecode': [-1]*nExps}
    dObj   = {'chuffed': [-1]*nExps, 'cp-sat': [-1]*nExps, 'highs': [-1]*nExps, 'coin': [-1]*nExps, 'gecode': [-1]*nExps}

    for nombre_archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
                
                nExp = extractNumExp(nombre_archivo)
                solver = extractSolver(nombre_archivo)
                for linia in archivo:
                    linia = linia.strip()

                    if len(linia) >= 3 and linia[:3] == 'obj':
                        dObj[solver][nExp] = extractObjValue(linia)
                    
                    if len(linia) >= 14 and linia[:14] == '% time elapsed':
                        dTimes[solver][nExp] = min(7200, extractTime(linia))
    
    return (dTimes, dObj)

def printTimesObjs(dTimes, dObj):
    solvers = ['chuffed','cp-sat','highs','coin','gecode']
    

    max_width = 0
    for solver in solvers:
        for i in range(len(dTimes[solver])):
            entry = f"{dTimes[solver][i]}s, obj = {dObj[solver][i]}"
            max_width = max(max_width, len(entry))
    

    print(f"{'Solver':<10}", end="")
    if len(dTimes[solvers[0]]) > 0:
        for i in range(len(dTimes[solvers[0]])):
            print(f"{'Instance ' + str(i+1):>{max_width + 2}}", end="")
    print()
    

    print("-" * (10 + (max_width + 2) * len(dTimes[solvers[0]])))
    
    for solver in solvers:
        print(f"{solver:<10}", end="")
        for i in range(len(dTimes[solver])):
            entry = f"{dTimes[solver][i]}s, obj = {dObj[solver][i]}"
            print(f"{entry:>{max_width + 2}}", end="")
        print()


def timesLines(nExps, dTimes, log):
    nBlocs = nExps // 25
    for i in range(nBlocs):
        x = np.arange(25)
        y_times_chuffed = dTimes['chuffed'][i*25:i*25+25]
        y_times_cp_sat = dTimes['cp-sat'][i*25:i*25+25]
        y_times_highs = dTimes['highs'][i*25:i*25+25]
        y_times_coin = dTimes['coin'][i*25:i*25+25]
        y_times_gecode = dTimes['gecode'][i*25:i*25+25]

        fig, ax1 = plt.subplots()
        
        exp = '1r Bloc'
        if i == 1:
            exp = '2n Bloc'
        elif i > 1:
            exp = '3r Bloc'

        ax1.plot(x, y_times_chuffed, label='chuffed (temps)', color='b')
        ax1.plot(x, y_times_cp_sat, label='cp-sat (temps)', color='g')
        ax1.plot(x, y_times_highs, label='highs (temps)', color='r')
        ax1.plot(x, y_times_coin, label='coin (temps)', color='y')
        ax1.plot(x, y_times_gecode, label='gecode (temps)', color='c')
        ax1.set_xlabel('Número experiment')
        st = 'Temps (s)'
        if log:
            ax1.set_yscale('log')
            st = st + ' (log)'
        ax1.set_ylabel(st)
        ax1.tick_params(axis='y')

        fig.tight_layout()
        fig.legend(loc='upper right')
        plt.title('Temps per experiment, '+exp)
        plt.show()

def generateLatexTimeoutTable(dTimes, dObj):
    solvers = ['chuffed','cp-sat','highs','coin','gecode']
    
    stats = {}
    for solver in solvers:
        timeout_count = 0
        timeout_with_solution = 0
        obj_values = []
        
        for i in range(len(dTimes[solver])):
            if dTimes[solver][i] > 7100:
                timeout_count += 1
                if dObj[solver][i] != -1:
                    timeout_with_solution += 1
                    obj_values.append(dObj[solver][i])
        

        if obj_values:
            avg_obj = sum(obj_values) / len(obj_values)
            avg_obj_str = f"{avg_obj:.2f}"
        else:
            avg_obj_str = "-"
        
        stats[solver] = (timeout_count, timeout_with_solution, avg_obj_str)

    latex_code = []
    latex_code.append("\\begin{table}[H]")
    latex_code.append("\\centering")
    latex_code.append("\\begin{tabular}{|l|c|c|c|}")
    latex_code.append("\\hline")
    latex_code.append("\\textbf{Solver} & \\textbf{Cops límit (2h)} & \\textbf{Amb solució} & \\textbf{Mitjana Obj} \\\\")
    latex_code.append("\\hline")
    
    for solver in solvers:
        timeout_count, timeout_with_solution, avg_obj_str = stats[solver]
        latex_code.append(f"{solver} & {timeout_count} & {timeout_with_solution} & {avg_obj_str} \\\\")
    
    latex_code.append("\\hline")
    latex_code.append("\\end{tabular}")
    latex_code.append("\\caption{Anàlisi valors objectiu per solver.}")
    latex_code.append("\\label{tab:timeout_analysis}")
    latex_code.append("\\end{table}")
    
    print("\n".join(latex_code))
    return "\n".join(latex_code)

def objLines(nExps, dObj, notFound):
    nBlocs = nExps // 25
    for i in range(nBlocs):
        x = np.arange(25)
        
        y_obj_chuffed = [o if o != -1 else notFound for o in dObj['chuffed'][i*25:i*25+25]]
        y_obj_cp_sat = [o if o != -1 else notFound for o in dObj['cp-sat'][i*25:i*25+25]]
        y_obj_highs = [o if o != -1 else notFound for o in dObj['highs'][i*25:i*25+25]]
        y_obj_coin = [o if o != -1 else notFound for o in dObj['coin'][i*25:i*25+25]]
        y_obj_gecode = [o if o != -1 else notFound for o in dObj['gecode'][i*25:i*25+25]]
        
        fig, ax1 = plt.subplots()
        
        exp = '1r Bloc'
        if i == 1:
            exp = '2n Bloc'
        elif i > 1:
            exp = '3r Bloc'

        ax1.plot(x, y_obj_chuffed, label='chuffed (obj)', linestyle='--', color='b')
        ax1.plot(x, y_obj_cp_sat, label='cp-sat (obj)', linestyle='--', color='g')
        ax1.plot(x, y_obj_highs, label='highs (obj)', linestyle='--', color='r')
        ax1.plot(x, y_obj_coin, label='coin (obj)', linestyle='--', color='y')
        ax1.plot(x, y_obj_gecode, label='gecode (obj)', linestyle='--', color='c')

        ax1.set_ylabel('obj')
        ax1.tick_params(axis='y')

        fig.tight_layout()
        fig.legend(loc='upper right')
        plt.title('Valor objectiu per experiment, '+exp)
        plt.show()


def boxplotTimes(dTimes, log, nExps):
    nBlocs = nExps // 25
    for i in range(nBlocs):
        #x = np.arange(nExps)
        clean_times = {
            solver: [t for t in times[i*25:i*25+25] if t != -1]
            for solver, times in dTimes.items()
        }

        # Crear boxplot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.boxplot(clean_times.values(), labels=clean_times.keys(), showfliers=True)

        st = 'Temps (s)'
        if log:
            ax.set_yscale('log')
            st = st + ' (log)'

        exp = '1r Bloc'
        if i == 1:
            exp = '2n Bloc'
        elif i > 1:
            exp = '3r Bloc'

        ax.set_ylabel(st)
        ax.set_title('Boxplot temps per solver, '+exp)
        
        plt.tight_layout()
        plt.show()


def histBinsTimes(nExps, dTimes, dObj, utilitzarDobj):
    if not utilitzarDobj:
        dObj = [0]*nExps
    nBlocs = nExps // 25
    
    # Recopilar datos de todos los bloques
    all_times_bins = []
    block_labels = []
    
    for i in range(nBlocs):
        names = ['chuffed','cp-sat','highs','coin','gecode']
        nomsReals = ['Chuffed','OR Tools','HiGHS','COIN-BC','Gecode']
        
        timesBins = []
        for solver in names:
            solverTimesBins = [0]*3
            for j, time in enumerate(dTimes[solver][i*25:i*25+25]):
                if time < 900 and time != -1 and dObj[solver][i*25+j] != -1:
                    solverTimesBins[0] += 1
                elif time < 7100 and time != -1 and dObj[solver][i*25+j] != -1:
                    solverTimesBins[1] += 1
                else:
                    solverTimesBins[2] += 1
            timesBins.append(solverTimesBins)
        
        all_times_bins.append(timesBins)
        
        # Etiquetas para los bloques
        if i == 0:
            block_labels.append('1r Bloc')
        elif i == 1:
            block_labels.append('2n Bloc')
        else:
            block_labels.append(f'{i+1}º Bloc')
    
    # Crear el gráfico comparativo
    fig, axs = plt.subplots(1, len(names), figsize=(18,6), sharey=True)
    
    bin_labels = ['< 15 min', '15 – 120 min', ' > 120 min']
    colors = ['skyblue', 'lightcoral', 'lightgreen', 'gold', 'plum']  # Colores para cada bloque
    
    # Ancho de las barras
    bar_width = 0.8 / len(all_times_bins)
    
     
    for j, solver in enumerate(names):
        # Posiciones para las barras de cada bin
        x_pos = np.arange(len(bin_labels))
        
        for block_idx, times_bins in enumerate(all_times_bins):
            # Desplazamiento para cada bloque
            offset = (block_idx - len(all_times_bins)/2 + 0.5) * bar_width
            
            axs[j].bar(x_pos + offset, 
                      times_bins[j], 
                      bar_width, 
                      label=block_labels[block_idx],
                      color=colors[block_idx % len(colors)],
                      edgecolor='black',
                      alpha=0.8)
        
        axs[j].set_title(nomsReals[j], fontsize=25)
        axs[j].set_xticks(x_pos)
        axs[j].set_xticklabels(bin_labels, fontsize=12)
        
        if j == 0:
            axs[j].set_ylabel("Nombre d'experiments", fontsize=25)
            axs[j].legend(fontsize=20)
    
    #plt.suptitle('Comparació de Temps per solver, 3 bins (2 conjunts d\'experiments)', fontsize=25)
    plt.tight_layout()
    plt.show()

def printMitjanaVariancia(dTimes, solver):
    llista = dTimes[solver]
    print((round(statistics.mean(llista), 2), round(statistics.stdev(llista), 2)))


def boxplotTimeSolver(dTimes, solvers):
    plt.figure(figsize=(8, 5))
    
    data = [dTimes[solver] for solver in solvers]
    
    plt.boxplot(data, vert=True, patch_artist=True)
    
    plt.xticks(range(1, len(solvers)+1), solvers)
    
    plt.ylabel("Temps (s)")
    plt.grid(True, axis='y')
    #plt.title("Temps per solver")
    plt.show()

def quantsTenenSolucio(dTimes, nExps):
    solvers = ['chuffed','cp-sat','highs','coin','gecode']
    #print(dTimes['chuffed'])
    res = [[] for _ in range(nExps)]
    for i in range(len(dTimes[solvers[0]])):
        for solver in solvers:
            if dTimes[solver][i] <= 7100:
                res[i].append(solver)
    
    print(res[25:])
    return res

def solverPerProblema(dTimes,nExps):
    data = quantsTenenSolucio(dTimes, nExps)[25:]

    all_solvers = ['chuffed','cp-sat','highs','coin','gecode']
    
    matrix = []
    for solver in all_solvers:
        row = [1 if solver in problem_solvers else 0 for problem_solvers in data]
        matrix.append(row)
    
    df_heatmap = pd.DataFrame(matrix, 
                             index=[s.upper() for s in all_solvers], 
                             columns=[f'E{i+25:02d}' for i in range(len(data))])  
    
    plt.style.use('default')
    
    fig, ax = plt.subplots(figsize=(12, 4))
    
    colors = ['#f8f9ff', '#4CAF50'] 
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)
    
    
    hm = sns.heatmap(df_heatmap, 
                     annot=False, 
                     cmap=custom_cmap,
                     cbar_kws={
                         'label': 'Estado del Problema',
                         'shrink': 0.6,
                         'aspect': 20,
                         'ticks': [0, 1],
                         'format': '%.0f'
                     },
                     linewidths=1,
                     linecolor='white',
                     square=False,
                     ax=ax)
    

    cbar = hm.collections[0].colorbar
    cbar.set_ticklabels(['No Resolt', 'Resolt'])
    cbar.ax.tick_params(labelsize=8)
    
    for i, solver in enumerate(all_solvers):
        for j in range(len(data)): 
            if solver in data[j]:
       
                ax.text(j + 0.5, i + 0.5, '✓', 
                       ha='center', va='center', 
                       fontsize=12, fontweight='bold', 
                       color='white')
            else:
              
                ax.text(j + 0.5, i + 0.5, '•', 
                       ha='center', va='center', 
                       fontsize=6, 
                       color='#bbb', alpha=0.5)
    

    ax.set_title('rendiment dels solvers', 
                fontsize=12, fontweight='bold', pad=15, color='#2c3e50')
    
    ax.set_xlabel('Número d\'experiment', fontsize=10, fontweight='bold', color='#34495e')
    ax.set_ylabel('Solvers', fontsize=10, fontweight='bold', color='#34495e')
    
    ax.tick_params(axis='x', labelsize=7, colors='#2c3e50', rotation=45)
    ax.tick_params(axis='y', labelsize=9, colors='#2c3e50')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('#34495e')
    
    plt.tight_layout()
    plt.show()
    
    return df_heatmap

def div2congres(dObjChuffed):
    return [int(obj//2) for obj in dObjChuffed]

if __name__ == "__main__":
    carpeta = 'output_radio'

    nExps = 50
    
    dTimes, dObj = extractData(nExps=nExps, carpeta=carpeta)

    if carpeta == 'output_congres':
        dObj['chuffed'] = div2congres(dObj['chuffed'])

    utilitzarDobj = True
    if carpeta == 'output_escolar':
        utilitzarDobj = False
    else:
        solvers = ['chuffed','cp-sat','highs','coin','gecode']
        for solver in solvers:
            for i in range(nExps):
                if dObj[solver][i] == -1:
                    dTimes[solver][i] = 7200.0

    #######################################################
    # FUNCIONS DISPONIBLES

    generateLatexTimeoutTable(dTimes=dTimes, dObj=dObj)

    #timesLines(nExps=nExps, dTimes=dTimes, log=True)
    
    #objLines(nExps=nExps, dObj=dObj, notFound=30)
    
    #boxplotTimes(dTimes=dTimes, log=True, nExps=nExps)

    #printTimesObjs(dTimes, dObj)

    histBinsTimes(nExps=nExps, dTimes=dTimes, dObj=dObj, utilitzarDobj=utilitzarDobj)

    #printMitjanaVariancia(dTimes, 'chuffed')

    #boxplotTimeSolver(dTimes, ['highs','coin'])

    #quantsTenenSolucio(dTimes, nExps)

    #solverPerProblema(dTimes,nExps)