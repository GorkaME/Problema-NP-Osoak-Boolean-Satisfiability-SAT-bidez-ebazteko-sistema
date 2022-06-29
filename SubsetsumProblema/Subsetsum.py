import time
import os
import subprocess
import gzip
import shutil
from SubsetsumProblema import SubsetSum_to_SATOptimo3
import csv

def main(lista, suma):
    
    inicio = time.time()
    filename = str(len(lista)) + "_Elementu_" + str(suma) + "_batu"
    sortuCnf(SubsetSum_to_SATOptimo3.reduce_subsetsum_to_SAT(lista, suma), "SubsetsumProblema/cnf/" + filename)
    fin = time.time()
    print("Clausulak sortzeko erabilitako denbora:" + str(fin-inicio))
    
    inicio = time.time()
    win_cmd = "kissat SubsetsumProblema/cnf/" + filename + ".gz >> SubsetsumProblema/erantzunak/" + filename + ".txt" 
    subprocess.Popen(win_cmd, shell=True)
    fin = time.time()
    print("Kissat erabilitako denbora:" + str(fin-inicio))
    while not os.path.exists("SubsetsumProblema/erantzunak/" + filename + ".txt"):
        time.sleep(1)
    fitxategia = []
    f = open("SubsetsumProblema/erantzunak/" + filename + ".txt", "r")
    while(True):
        linea = f.readline()[1:]
        fitxategia.append(str(linea))
        if not linea:
            break
    f.close()
    
    with open("SubsetsumProblema/erantzunak/" + filename + ".txt", "r") as f:
        while(True):
            linea = f.readline()
            if ("s SATISFIABLE" in linea) or ("s UNSATISFIABLE" in linea):
                break
        if not("s UNSATISFIABLE" in linea):
            emaitza = []
            
            while(True):
                linea = f.readline()[2:].split()
                emaitza += linea
                if("0" in linea):
                    break
            emaitza.remove("0")
            emaitza=[emaitza[i:i + len(lista)] for i in range(0, len(emaitza),  len(lista))]
            bat = ""
            indices = []
            zenbakiz = []
            for i in range (0,len(emaitza[0])):
                if not "-" in emaitza[0][i]:
                    bat += str(lista[i]) + " + "
                    zenbakiz.append(lista[i])
                    indices.append(emaitza[0][i])
            bat = bat[:-2] + "= " + str(suma)
            sortuBistaraketa(zenbakiz)
        else:
            indices = -1   
            bat = 0
            zenbakiz=0
        f.close()
    return fitxategia, bat, indices, zenbakiz
        
def sortuCnf(clauses, filename):
    if os.path.exists(filename + ".gz"):
        os.remove(filename + ".gz")
    with open(filename + ".cnf", "w+") as f:
            f.write(clauses)
    with open(filename + ".cnf", "rb") as f_in:
        with gzip.open(filename + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(filename + ".cnf")
      
def sortuBistaraketa(indices):
    if os.path.exists("static/plot.csv"):
        os.remove("static/plot.csv")
    with open("static/plot.csv", 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'parent', 'value'])
        writer.writerow(['Origin',])
        for elem in indices:
            writer.writerow([elem, 'Origin', elem])
    