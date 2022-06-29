import os
import gzip
import shutil
import subprocess
import time
import psutil
import pandas as pd

def main(text):
    gertuena = text
    filename = str(text) + '_queens' 
    i = 0
    if not os.path.exists("cnf/" + filename + ".gz"):
        inicio = time.time()
        while(i<100):                                 #100 diferentzia maximoarekin gertuen duen fitxategia bilatu
            if os.path.exists("cnf/" + str(gertuena+i) + "_queens.gz"):
                gertuena += i
                break
            if os.path.exists("cnf/" + str(gertuena-i) + "_queens.gz"):
                gertuena -= i
                break
            i +=1
        if gertuena>text:
            clausulakKendu(int(text), "cnf/" + filename, gertuena)
        if gertuena<text:
            clausulakSortu(int(text), "cnf/" + filename)
        documentos = clausulakSortu(int(text), "cnf/" + filename)
        #sortuCnf("cnf/" + filename, documentos)     #klausulak sortzeko
        fin = time.time()
        print("Clausulak sortzeko erabilitako denbora:" + str(fin-inicio))
    else:
        print(filename + " fitxategia existitzen da!")
    '''
    inicio = time.time()
    lortuErantzuna(filename)                                   #Kissat komandoa terminalean exekutatzeko, eta honek jasotzen duen emaitza gordetzeko
    fin = time.time()
    print("Kissat erabilitako denbora:" + str(fin-inicio))
    matrize, fitxategia = prozesatuEmaitza(int(text), filename)              #Emaitza prozesatu zerokoz eta batekoz matrizea lortzeko.
    dimentsio = int(text)
    
    return matrize, fitxategia, dimentsio
    '''
def clausulakKendu(n, filename, gertuena):
    soberan = []
    for x in range(n+1, gertuena+1):
        soberan.append(str(x))
    print(soberan[0])
    clauses=[]
    clause0=[]
    clause0.append(["p","cnf",n*n]) #Lehenengo clausula berezia sortzen dugu, baina azken balioa gero gehitzen diogu
    filak=[] #Filen klausulak gordeko dituen aldagaia
    kont = 0
    documentos = 1
    k=1
    for i in range(n):      #filak sortzeko gure klausuletan
        filak.append([])
        for j in range(n):
            filak[i].append(k)
            k+=1
        clauses.append(filak[i].copy()) #sortutako fila bakoitza Clasuletan gordetzen dugu
    kont, clauses, documentos = clausulakGorde(clauses, kont, filename, documentos)
    with open(filename + ".cnf", "w") as ffff:
        with gzip.open("cnf/" + str(gertuena) + '_queens' + ".gz",'rt') as f:
            for line in f:
                if "-1" in line:
                    break
            ffff.write(line)
            dago = False
            for line in f:
                for item in soberan:
                    if not item in line:
                        dago = True
                    if dago:
                        ffff.write(line)
                        dago = False
                        
                        
def clausulakSortu(n, filename):
    print("Klausulak sortzen hasi...") 
    clauses=[]
    clause0=[]
    clause0.append(["p","cnf",n*n]) #Lehenengo clausula berezia sortzen dugu, baina azken balioa gero gehitzen diogu
    filak=[] #Filen klausulak gordeko dituen aldagaia
    kont = 0
    documentos = 1
    k=1
    for i in range(n):      #filak sortzeko gure klausuletan
        filak.append([])
        for j in range(n):
            filak[i].append(k)
            k+=1
        clauses.append(filak[i].copy()) #sortutako fila bakoitza Clasuletan gordetzen dugu
            
    for i in range(len(filak)):        #Combinations erabili beharrean, eskuz sortu ditut filen konbinazioak
        for j in range(len(filak[i])): #ez dut lortu egitea itertools combinations erabiliz
            k=j+1                      #fila bakoitzerako, uneko eta hurrengo balioak gordetzen ditut(j eta k)
            while k<len(filak[i]):     #while baten bidez, konbinaketa guztiak lortzen ditut hau eginez: 
                kombFilak=[] #Filen konbinazio klausulak gordeko dituen aldagaia
                kombFilak.append([])   #Uneko balioa hurrengo guztiekin konbinatuz, horrela clausuleko balio guztiekin
                kombFilak[0].append(-filak[i][j]) 
                kombFilak[0].append(-filak[i][k])
                clauses.append(kombFilak[0]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                k+=1 #hurrengo balioa hartzeko
                if psutil.virtual_memory().percent>95:
                    print("Memoriaren 95% erabilita, orain arteko klausulak gordeko dira jarraitu ahal izateko")
                    kont, clauses, documentos = clausulakGorde(clauses, kont, filename, documentos)
                    print("Geratu den memoria: " + str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))
                
    print("Filak Sortuta!!") 
    #----------------- Zutabeak eta bere konbinazioak -------------------
        
    zutabeak=[]  #Zutabeen klausulak gordeko dituen aldagaia
    for i in range(n):      #zutabeak sortzeko gure klausuletan
        zutabeak.append([])
        k=i+1
        for j in range(n):
            zutabeak[i].append(k)
            k+=n            #kasu honetan, k=k+n rekin lortzen dugu zutabeen balioak.
        clauses.append(zutabeak[i]) #sortutako zutabe bakoitza Clasuletan gordetzen dugu
         
     #Zutabeen konbinazio klausulak gordeko dituen aldagaia
    for i in range(len(zutabeak)):        #Combinations erabili beharrean, eskuz sortu ditut filen konbinazioak
        for j in range(len(zutabeak[i])): 
            k=j+1                      #fila bakoitzerako, uneko eta hurrengo balioak gordetzen ditut(j eta k)
            while k<len(filak[i]):        #while baten bidez, konbinaketa guztiak lortzen ditut hau eginez: 
                kombZutabeak=[]
                kombZutabeak.append([])   #Uneko balioa hurrengo guztiekin konbinatuz, horrela clausuleko balio guztiekin
                kombZutabeak[0].append(-zutabeak[i][j]) 
                kombZutabeak[0].append(-zutabeak[i][k])
                clauses.append(kombZutabeak[0]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                k+=1 #hurrengo balioa hartzeko
                if psutil.virtual_memory().percent>95:
                    print("Memoriaren 95% erabilita, orain arteko klausulak gordeko dira jarraitu ahal izateko")
                    kont, clauses, documentos = clausulakGorde(clauses, kont, filename, documentos)
                    print("Geratu den memoria: " + str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))
    
    #----------------- Behe diagonalen konbinazioak -------------------
    print("Zutabeak Sortuta!!") 
       
    for i in range(len(filak)): #Filak gordetak ditugunez, erabiliko ditugu
        for j in range(len(filak[i])):
            posI=i                      #uneko i posizioa gordetzen dugu
            posJ=j                      #uneko j posizioa gordetzen dugu
            while posI+1<len(filak[i]) and posJ+1<len(filak[j]): #posI eta posJ hurrengo posizioa duten bitartean
                beheDiagonal=[]   #clausula bat sortzen dugu
                beheDiagonal.append([])
                beheDiagonal[0].append(-filak[i][j])              #lehenengo posizioa sartzen dugu
                beheDiagonal[0].append(-filak[posI+1][posJ+1])    #Eta hurrengoa ere (gero hurrengoaren hurrengoa etab.. ahal den bitartean)
                clauses.append(beheDiagonal[0]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                posI+=1
                posJ+=1 #hurrengo balioak hartzen ditugu, n baino txikiagoak badira klausula berri bat sortzeko
                if psutil.virtual_memory().percent>95:
                    print("Memoriaren 95% erabilita, orain arteko klausulak gordeko dira jarraitu ahal izateko")
                    kont, clauses, documentos = clausulakGorde(clauses, kont, filename, documentos)
                    print("Geratu den memoria: " + str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))
        
    print("Behe Diagonala Sortuta!!")   
    #----------------- Goi diagonalen konbinazioak -------------------
    
    for i in range(len(filak)): #Filak gordetak ditugunez, erabiliko ditugu
        for j in range(len(filak[i])):
            posI=i                      #uneko i posizioa gordetzen dugu
            posJ=j                      #uneko j posizioa gordetzen dugu
            while posI+1<len(filak[i]) and posJ-1>=0: #posI  hurrengo posizioa duen, eta posJ aurreko posizioa
                goiDiagonal=[]  #clausula bat sortzen dugu
                goiDiagonal.append([])
                goiDiagonal[0].append(-filak[i][j])              #lehenengo posizioa sartzen dugu
                goiDiagonal[0].append(-filak[posI+1][posJ-1])    #Eta diagonaleko hurrengoa ere (gero hurrengoaren hurrengoa etab.. ahal den bitartean)
                clauses.append(goiDiagonal[0]) #sortutako klausula bakoitza Clauses-en gordetzen dut
                posI+=1 #uneko posI-ren hurrengo balioa aztertuko dugu
                posJ-=1 #uneko posJ-ren aurkako balioa aztertuko dugu 
                if psutil.virtual_memory().percent>95:
                    print("Memoriaren 95% erabilita, orain arteko klausulak gordeko dira jarraitu ahal izateko")
                    kont, clauses, documentos = clausulakGorde(clauses, kont, filename, documentos)
                    print("Geratu den memoria: " + str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))
        
    #----------------- Klausula bakoitzean 0 esleitu, eta lehenengo klausula bukatu -------------------
    print("Goi Diagonala Sortuta!!") 
    
    kont, clauses, documentos = clausulakGorde(clauses, kont, filename, documentos)
    print("Geratu den memoria: " + str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))
    
    clause0[0].append(kont)    
    listToStr = [' '.join([str(elem) for elem in clause]) for clause in clause0]
    with open(filename + "0.cnf", "w+") as f:
        for item in listToStr:
            f.write("%s\n" % item)
                        
    print("Klausulak Gordeta!!") 
    return documentos

def clausulakGorde(clauses, kont, filename, documentos):
    for k in range(0,len(clauses)): 
        clauses[k].append(0)
        kont+=1 
    listToStr = [' '.join([str(elem) for elem in clause]) for clause in clauses]
    with open(filename + str(documentos) + ".cnf", "w+") as f:
        for item in listToStr:
            f.write("%s\n" % item)
    print("Klausulen " + str(documentos) + ". cnf fitxategia sortuta")  
    clauses=[]
    documentos += 1
    return kont, clauses, documentos

def sortuCnf(filename, documentos):
       
    with gzip.open(filename + ".gz", "wb") as f_out:
        i=0
        while(i<documentos):
            with open(filename + str(i) +".cnf", "rb") as f_in:
                shutil.copyfileobj(f_in, f_out)
            os.remove(filename + str(i) +".cnf")
            i += 1
    print("Klausulak Konprimatutak!!") 
        
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

main(50)
 