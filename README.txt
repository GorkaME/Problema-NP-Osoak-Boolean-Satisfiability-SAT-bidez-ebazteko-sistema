-"__pycache__" flask cachearako erabiltzen duen karpeta da.

-"kissat" karpetan, Ubuntu terminalean "Kissat" komandoa erabiltzeko exekutablea eta honen informazio guztia gordeta daukat (Github-etik deskargatzen dena). 
Instalatu behar da ubuntu terminalean "Kissat" komandoa erabiltzeko (Ikusi Github-en pausuak: https://github.com/arminbiere/kissat.git)

-"NqueensProblema" Nqueens problemaren datu guztiak gordetzeko.

-"HamiltonProblema" Bide Hamiltondarra problemaren datu guztiak gordetzeko.

-"SubsetsumProblema" Subsetsum problemaren datu guztiak gordetzeko.

-"static" karpetaren barruan Javascript dokumentuak daude.

-"templates" karpeta barruan .HTML fitxategiak daude.

Dokumentu ".pyc" solte horiek aplikazioak behar dituen dokumentuak dira (denak Subsetsum problemarentzako, bere karpetaren barruan ezin dira martxan jarri)

-"app.py"

Flask martxan jartzeko hurrengo bertzioak erabili:
     Python 3.8.10
     Flask 1.1.1
     Werkzeug 0.16.1

Ubuntu terminala behar da aplikazioa martxan jartzeko. Exekutatu behar diren komandoak:
     -Aplikazioa dagoen lekuan kokatu: cd /**/**...
     -export FLASK_APP=app
     -export FLASK_ENV=development
     -flask run
