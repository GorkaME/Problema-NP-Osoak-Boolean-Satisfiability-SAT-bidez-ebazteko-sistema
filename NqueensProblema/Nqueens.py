import os
import gzip
import shutil
import subprocess
import time

def main(text):
    
    inicio = time.time()
    filename = str(text) + '_queens' 
    sortuCnf(clausulakSortu(int(text)), "NqueensProblema/cnf/" + filename)     #klausulak sortzeko
    fin = time.time()
    print("Clausulak sortzeko erabilitako denbora:" + str(fin-inicio))
        
    inicio = time.time()
    lortuErantzuna(filename)                                   #Kissat komandoa terminalean exekutatzeko, eta honek jasotzen duen emaitza gordetzeko
    matrize, fitxategia = prozesatuEmaitza(int(text), filename)              #Emaitza prozesatu zerokoz eta batekoz matrizea lortzeko.
    dimentsio = int(text)
    fin = time.time()
    print("Erantzuna prozesatzeko eta pantailaratzeko erabilitako denbora:" + str(fin-inicio))
    return matrize, fitxategia, dimentsio
    
def clausulakSortu(n):
    clauses=[]
    clauses.append(["p","cnf",n*n]) #Lehenengo clausula berezia sortzen dugu, baina azken balioa gero gehitzen diogu
    filak=[] #Filen klausulak gordeko dituen aldagaia
    k=1
    for i in range(n):      #filak sortzeko gure klausuletan
        filak.append([])
        for j in range(n):
            filak[i].append(k)
            k+=1
        clauses.append(filak[i]) #sortutako fila bakoitza Clasuletan gordetzen dugu
        
    indizea=0
    kombFilak=[] #Filen konbinazio klausulak gordeko dituen aldagaia
    for i in range(len(filak)):        #Combinations erabili beharrean, eskuz sortu ditut filen konbinazioak
        for j in range(len(filak[i])): #ez dut lortu egitea itertools combinations erabiliz
            k=j+1                      #fila bakoitzerako, uneko eta hurrengo balioak gordetzen ditut(j eta k)
            while k<len(filak[i]):     #while baten bidez, konbinaketa guztiak lortzen ditut hau eginez: 
                kombFilak.append([])   #Uneko balioa hurrengo guztiekin konbinatuz, horrela clausuleko balio guztiekin
                kombFilak[indizea].append(-filak[i][j]) 
                kombFilak[indizea].append(-filak[i][k])
                clauses.append(kombFilak[indizea]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                k+=1 #hurrengo balioa hartzeko
                indizea+=1 #beste clausula desberdin bat sortzeko
                
    #----------------- Zutabeak eta bere konbinazioak -------------------
        
    zutabeak=[]  #Zutabeen klausulak gordeko dituen aldagaia
    for i in range(n):      #zutabeak sortzeko gure klausuletan
        zutabeak.append([])
        k=i+1
        for j in range(n):
            zutabeak[i].append(k)
            k+=n            #kasu honetan, k=k+n rekin lortzen dugu zutabeen balioak.
        clauses.append(zutabeak[i]) #sortutako zutabe bakoitza Clasuletan gordetzen dugu
         
    indizea=0
    kombZutabeak=[] #Zutabeen konbinazio klausulak gordeko dituen aldagaia
    for i in range(len(zutabeak)):        #Combinations erabili beharrean, eskuz sortu ditut filen konbinazioak
        for j in range(len(zutabeak[i])): 
            k=j+1                      #fila bakoitzerako, uneko eta hurrengo balioak gordetzen ditut(j eta k)
            while k<len(filak[i]):        #while baten bidez, konbinaketa guztiak lortzen ditut hau eginez: 
                kombZutabeak.append([])   #Uneko balioa hurrengo guztiekin konbinatuz, horrela clausuleko balio guztiekin
                kombZutabeak[indizea].append(-zutabeak[i][j]) 
                kombZutabeak[indizea].append(-zutabeak[i][k])
                clauses.append(kombZutabeak[indizea]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                k+=1 #hurrengo balioa hartzeko
                indizea+=1 #beste clausula desberdin bat sortzeko
    
    #----------------- Behe diagonalen konbinazioak -------------------
    
    indizea=0
    beheDiagonal=[]
    for i in range(len(filak)): #Filak gordetak ditugunez, erabiliko ditugu
        for j in range(len(filak[i])):
            posI=i                      #uneko i posizioa gordetzen dugu
            posJ=j                      #uneko j posizioa gordetzen dugu
            while posI+1<len(filak[i]) and posJ+1<len(filak[j]): #posI eta posJ hurrengo posizioa duten bitartean
                beheDiagonal.append([])   #clausula bat sortzen dugu
                beheDiagonal[indizea].append(-filak[i][j])              #lehenengo posizioa sartzen dugu
                beheDiagonal[indizea].append(-filak[posI+1][posJ+1])    #Eta hurrengoa ere (gero hurrengoaren hurrengoa etab.. ahal den bitartean)
                clauses.append(beheDiagonal[indizea]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                posI+=1
                posJ+=1 #hurrengo balioak hartzen ditugu, n baino txikiagoak badira klausula berri bat sortzeko
                indizea+=1 #beste clausula desberdin bat sortzeko
                
    #----------------- Goi diagonalen konbinazioak -------------------
    
    indizea=0
    goiDiagonal=[]
    for i in range(len(filak)): #Filak gordetak ditugunez, erabiliko ditugu
        for j in range(len(filak[i])):
            posI=i                      #uneko i posizioa gordetzen dugu
            posJ=j                      #uneko j posizioa gordetzen dugu
            while posI+1<len(filak[i]) and posJ-1>=0: #posI  hurrengo posizioa duen, eta posJ aurreko posizioa
                goiDiagonal.append([])   #clausula bat sortzen dugu
                goiDiagonal[indizea].append(-filak[i][j])              #lehenengo posizioa sartzen dugu
                goiDiagonal[indizea].append(-filak[posI+1][posJ-1])    #Eta diagonaleko hurrengoa ere (gero hurrengoaren hurrengoa etab.. ahal den bitartean)
                clauses.append(goiDiagonal[indizea]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                posI+=1 #uneko posI-ren hurrengo balioa aztertuko dugu
                posJ-=1 #uneko posJ-ren aurkako balioa aztertuko dugu
                indizea+=1 #beste clausula desberdin bat sortzeko            
        
    #----------------- Klausula bakoitzean 0 esleitu, eta lehenengo klausula bukatu -------------------
    
    kont=0 #kontagailu bat sortzen dugu klausulak zenbatzeko
    for i in range(1,len(clauses)): #lehenengo klausuletik aurrera 0 bat esleitzen diegu bakoitzari bukaeran
        clauses[i].append(0)
        kont+=1
    clauses[0].append(kont) #klausula kopurua batzen diogu lehenengo klausulari
    
    return clauses

def sortuCnf(clauses, filename):
       
    if not os.path.exists(filename + ".gz"):
        #List to Str
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
    if not os.path.exists("NqueensProblema/erantzunak/" + file + ".txt"):
        win_cmd = "kissat " + "NqueensProblema/cnf/" + file + ".gz >> NqueensProblema/erantzunak/" + file + ".txt" 
        subprocess.Popen(win_cmd, shell=True)
    
def prozesatuEmaitza(num, file):
    while not os.path.exists("NqueensProblema/erantzunak/" + file + ".txt"):
        time.sleep(1)
    fitxategia = []
    f = open("NqueensProblema/erantzunak/" + file + ".txt", "r")
    while(True):
        linea = f.readline()[1:]
        fitxategia.append(str(linea))
        if not linea:
            break
    f.close()
    with open("NqueensProblema/erantzunak/" + file + ".txt", "r") as f:
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
            emaitza=[emaitza[i:i + num] for i in range(0, len(emaitza), num)]
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
 