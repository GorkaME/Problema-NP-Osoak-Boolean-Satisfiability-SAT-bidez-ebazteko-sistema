from __future__ import division
from HamiltonProblema import HamiltonianToSat
import os
import gzip
import shutil
import subprocess
import time
import json

def list2dimacs(my_list):
        return ('\n'.join(' '.join(map(str,sl)) for sl in my_list)) 
    
    
def main(graphh):
    inicio = time.time()
    graph = "{" + graphh + "}"
    graph = json.loads(graph)
    edges, nodes = generate_edges(graph)
    matrize = generate_matrix(len(nodes))
    for edge in edges:
        nork = nodes.index(edge[0])
        nori = nodes.index(edge[1])
        matrize[nork][nori] = 1
    clauses = HamiltonianToSat.reduce_hamiltonian_to_SAT(matrize)
    fin = time.time()
    print("Clausulak sortzeko erabilitako denbora:" + str(fin-inicio))
    
    inicio = time.time()
    filename = str(len(nodes)) + "_nodo_" + str(len(edges)/2) + "_ertz"
    if os.path.exists("HamiltonProblema/grafoak/" + filename + ".gz"):
        os.remove("HamiltonProblema/grafoak/" + filename + ".gz")
    with open("HamiltonProblema/grafoak/" + filename + ".txt", "w+") as f:
        f.write(str(graphh))
    sortuCnf(clauses, "HamiltonProblema/cnf/" + filename)
    lortuErantzuna(filename) 
    emaitza, fitxategia = prozesatuEmaitza(matrize,filename) 
    if (emaitza == -1):
        bidea = -1
    else:
        bidea = generate_bidea(emaitza, nodes)
    fin = time.time()
    print("Erantzuna prozesatzeko eta pantailaratzeko erabilitako denbora:" + str(fin-inicio))
    return fitxategia, emaitza, matrize, bidea, edges, nodes
    
def generate_edges(graph):
    edges = []
    nodes = []
    for node in graph:
        nodes.append(node)
        for neighbour in graph[node]:
            # if edge exists then append
            edges.append((node, neighbour))
    return edges, nodes

def generate_matrix(lenght):
    matrize = []
    for i in range(lenght):
        matrize.append([])
        for j in range(lenght):
            matrize[i].append(0)
    return matrize
    
def generate_bidea(emaitza, nodes):
    bidea = []
    indice1 = -1
    indice2 = -1
    for i in range(len(emaitza)):
        for j in range(len(emaitza[i])):
            if (emaitza[i][j] == 1 and indice1 == -1):
                indice1 = j
            elif (emaitza[i][j] == 1 and indice2 == -1):
                indice2 = j
        if (indice2 != -1 and indice2 != -1):
            bidea.append([nodes[indice1],nodes[indice2]])
            indice1 = indice2
            indice2 = -1
    return bidea
    
def sortuCnf(clauses, filename):
    if os.path.exists(filename + ".gz"):
        os.remove(filename + ".gz")
    listToStr = [' '.join([str(elem) for elem in clause]) for clause in clauses]
    os.makedirs(os.path.dirname(filename + ".cnf"), exist_ok=True)
    with open(filename + ".cnf", "w+") as f:
        for item in listToStr:
            f.write("%s\n" % item)
    with open(filename + ".cnf", "rb") as f_in:
        with gzip.open(filename + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(filename + ".cnf")

def lortuErantzuna(file):
    if not os.path.exists("HamiltonProblema/erantzunak/" + file + ".txt"):
        win_cmd = "kissat " + "HamiltonProblema/cnf/" + file + ".gz >> HamiltonProblema/erantzunak/" + file + ".txt" 
        subprocess.Popen(win_cmd, shell=True)

def prozesatuEmaitza(matrize, file):
    while not os.path.exists("HamiltonProblema/erantzunak/" + file + ".txt"):
        time.sleep(1)
    fitxategia = []
    f = open("HamiltonProblema/erantzunak/" + file + ".txt", "r")
    while(True):
        linea = f.readline()[1:]
        fitxategia.append(str(linea))
        if not linea:
            break
    f.close()
    with open("HamiltonProblema/erantzunak/" + file + ".txt", "r") as f:
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
            emaitza=[emaitza[i:i + len(matrize)] for i in range(0, len(emaitza), len(matrize))]
            for elem in emaitza:
                for zenbaki in elem:
                    if "-" in zenbaki:
                        emaitza[emaitza.index(elem)][elem.index(zenbaki)] = 0
                    else:
                        emaitza[emaitza.index(elem)][elem.index(zenbaki)] = 1
        else:
            emaitza = -1       
        f.close()
        
    return emaitza, fitxategia

