from flask import Flask, request, render_template
#from flask_caching import Cache
from NqueensProblema import Nqueens 
from HamiltonProblema import Hamilton
from SubsetsumProblema import Subsetsum

#cache = Cache(config={'CACHE_TYPE': 'null'})
app = Flask(__name__)
#cache.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nqueens')
def nqueens():
    return render_template('nqueens.html')

@app.route('/nqueens', methods=['POST'])
def nqueens_post():
    text = request.form['text'] 
    if text == "" or int(text) == 0:
        return "Zenbaki bat 0 baino handiagoa aukeratu behar da."
    matrize, fitxategia, dimentsio = Nqueens.main(text)   
    return render_template('emaitzaNqueens.html', mtrx=matrize, fitx=fitxategia, dim=dimentsio)

@app.route('/hamiltondarra')
def hamiltondarra():
    return render_template('hamiltondarra.html')

@app.route('/hamiltondarra', methods=['POST'])
def hamiltondarra_post():
    graph = request.form['graph'] 
    if graph == "":
        return "Ezin da grafo huts bat prozesatu"
    fitxategia, emaitza, matrize, bidea, edges, nodes = Hamilton.main(graph)
    return render_template('emaitzaHamilton.html', fitx=fitxategia, mtrx=matrize, result=emaitza, bidea=bidea, edges=edges, nodes=nodes)

@app.route('/subsetsum')
def subsetsum():
    return render_template('subsetsum.html')

@app.route('/subsetsum', methods=['POST'])
def subsetsum_post():
    text = request.form['text'].split(",")
    suma = int(request.form['sum'])
    lista = []
    amalista = []
    for elem in text:
        lista.append(int(elem))
        amalista.append(int(elem))
    if len(lista) == 0:
        return "Zenbaki segidak zenbaki bat edo gehiago izan behar ditu"
    if not isinstance(suma, int):
        return "Batura bilatzeko zenbaki bat idatzi behar duzu"    
    fitxategia, batuketa, indices, zenbakiz = Subsetsum.main(lista, suma)
    return render_template('emaitzaSubsetsum.html', fitx=fitxategia, bat=batuketa, ind=indices, seg=amalista, bilatu=suma, lista=zenbakiz)
