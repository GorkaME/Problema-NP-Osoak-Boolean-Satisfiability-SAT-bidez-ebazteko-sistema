Proiektuaren edukiera:

-"NqueensProblema" Nqueens problemaren datu guztiak gordetzeko.

-"HamiltonProblema" Bide Hamiltondarra problemaren datu guztiak gordetzeko.

-"SubsetsumProblema" Subsetsum problemaren datu guztiak gordetzeko.

-"static" karpetaren barruan Javascript eta CSS dokumentuak daude.

-"templates" karpeta barruan .HTML fitxategiak daude.

-"app.py" aplikazio nagusia.

-".pyc" fitxategiak aplikazioa ondo funtzionatzeko behar diren gehigarriak dira.

Behin fitxategi guztiak deskargatuta daudenean, aplikazioa bai Linux sistema eragilean bai windows-eko
sistema eragilean martxan jarri ahal da. Desberdintasun bakarra, windows erabiltzea erabakitzen baduzu,
Ubuntu sistemako terminala instalatu behar duzu proiektua ondo funtzionatzeko (nire kasuan windows-en 
lan egin dut aipatutako Ubuntu terminal honekin). Hau egiteko jarraitu behar diren pausuak: 
	https://ubunlog.com/como-habilitar-la-bash-de-ubuntu-en-windows-10/

Hurrengo urratsa ingurune birtuala prestatzea da:
	$conda create -n tfg_martinez python=3.8.10
	$source activate tfg_martinez
	$pip install flask
	$pip install Werkzeug

Gainera, ingurunearen barruan hainbat liburutegi instalatu behar dira (proiektuak erabiltzen dituenak):
	$pip install psutil
	$pip install matplotlib
	$pip install tabulate
	$pip install mpmath
	$pip install pandas
	$pip install os
	$pip install gzip
	$pip install shutil
	$pip install subprocess
	$pip install time
	$pip install json
	$pip install csv

Behin instalazioak eginda eta ingurune birtuala prestatuta, Kissat SAT-Solver-a instalatu 
behar da Ubuntu terminalean "Kissat" komandoa erabili ahal izateko. Horretarako, 
Kissat Solver-aren Github orrialdean adierazten diren pausuak jarraitu behar dira:
	https://github.com/arminbiere/kissat.git

Azkenik, dena ondo instalatuta dagoenean, web aplikazioa martxan jarri behar da. Horretarako, 
Ubuntu terminalean lehenik aktibatu dugun ingurunean, Github-etik deskargatutako TFG-a gorde 
dugun karpetaren erroan jarri behar gara (nire kasuan "/mnt/c/TFG/") eta hurrengo komandoak 
exekutatu (Proiektuaren garapenean azaldutako komandoak dira):
	$export FLASK_APP=app
	$export FLASK_ENV=development
	$export FLASK_DEBUG=1
	$flask run

Honekin, web aplikazioa instalatuta eta martxan egongo lirateke. Erabiltzeko "flask run" komandoa 
exekutatu eta gero, Ubuntu terminalean agertzen den "http:" helbidea web nabigatzailean jarri behar da.

