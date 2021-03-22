# Tema3LFA-REGEXtoDFA
[Tema3 Limbaje Formale si Automate (2020-2021, seria CB)] 


Tema presupune parsarea unei expresii regulate, folosind un PDA. Expresia se converteste intr-un NFA si apoi DFA.

Am creat o clasa Regex care reprezinta o instanta regex, folosind-o pentru
a extinde o ierarhie de clase care sa exprime o expresie regulata (Symbol,
Concat, Union, OpenPar, ClosePar, Star, UnionMark).

Folosindu-ma de un PDA, respectiv de stiva acestuia, am parsat expresia primita
ca string, obtinand instanta Regex. Parcurgand caracter cu caracter string-ul,
se pune pe stiva orice simbolul sub forma de Symbol("a"). Pentru Kleene-Star se
aplica Star peste ce era in varful stivei. Pentru reuniune, se marcheaza prezenta
acesteia prin punerea pe stiva a unui UnionMark. Asemanator se pune pe stiva si
o instanta de OpenPar/ClosedPar pentru paranteze.

Expresia se reduce pe bucati, mai exact se reduc parantezele, de la cele mai
interioare la cele exterioare. Cand se intalneste o paranteza inchisa, se reduce
pana se ajunge la paranteza deschisa corespunzatoare. Se concateneaza ce era intre
paranteze, exceptand cazul in care se gaseste un UnionMark care simbolizeaza o
reuniune. In acest caz se gasesc partea din dreapta si din stanga ale reuniunii
si se pune pe stiva o instanta Union. Cand string-ul se termina se mai face o
reducere finala pentru a obtine o singura expresie regulata.

Pentru a transforma Regex-ul in NFA se foloseste algoritmul lui Thompson care
contruieste NFA-ul prin parcurgerea ierarhiei de clase, adaugand stari si
epsilon-tranzitii. Pentru a evita confuzia de nume ale starilor, acestea se
redenumesc folosind un offset (cu functia rename_states din nfa.py). NFA-ul
rezultat se converteste intr-un DFA, utilizand algoritmul implementat la tema
precedenta.

Detalii despre conversia din NFA in DFA se gasesc aici: https://github.com/stefaniagherasie/Tema2LFA-NFAtoDFA
