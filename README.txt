-"NqueensProblema" Nqueens problemaren datu guztiak gordetzeko.

-"HamiltonProblema" Bide Hamiltondarra problemaren datu guztiak gordetzeko.

-"SubsetsumProblema" Subsetsum problemaren datu guztiak gordetzeko.

-"static" karpetaren barruan Javascript dokumentuak daude.

-"templates" karpeta barruan .HTML fitxategiak daude.

-"app.py" aplikazio nagusia.

Dokumentu ".pyc" solteak aplikazioak behar dituen dokumentuak dira (denak Subsetsum problemarentzako, bere karpetaren barruan ezin dira martxan jarri). 
Instalatu behar da ubuntu terminalean "Kissat" komandoa aplikazioa ondo ibiltzeko (Ikusi Github-en pausuak: https://github.com/arminbiere/kissat.git).

Flask martxan jartzeko hurrengo bertzioak erabili:
     Python 3.8.10
     Flask 1.1.1
     Werkzeug 0.16.1

Ubuntu terminala behar da aplikazioa martxan jartzeko. Exekutatu behar diren komandoak:
     -Aplikazioa dagoen lekuan kokatu: cd /**/**...
     -export FLASK_APP=app
     -export FLASK_ENV=development
     -flask run
