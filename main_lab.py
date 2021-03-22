'''
    Vom implementa o parte din laborator in acest "Tutorial"
'''

'''
    0. O sa cream o clasa Stack doar ca sa semene mai bine cu un Automat Push-Down.
Putem folosi si o simpla lista in clasele de mai jos.    
    De asemenea, vom avea si o functie de peek care poate sa ne intoarca si elemente
aflate mai jos de varful stivei. "It's a Surprise Tool That Will Help Us Later "
'''


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, el):
        self.stack.append(el)

    def peek(self, pos):
        if pos < len(self.stack):
            return self.stack[-(pos + 1)]

        return None

    def pop(self):
        el = self.peek(0)
        self.stack.pop()
        return el

    def empty(self):
        return self.stack == []

    def size(self):
        return len(self.stack)


'''
    1. Cream un PDA care sa accepte stringuri generate de gramatica din enunt.
Pentru a fi mai simplu de citit, vom avea si cateva define-uri + type hint-uri.
Vom "hardcoda" PDA-ul in functia sa init. Puteti incerca sa desenati pe hartie
acest PDA.

    Pentru tutorial vom considera doar numere de o cifra si operatorii "+" si "()".
Ramane ca TODO restul gramaticii.

<expr> ::= <expr> + <expr> | (<expr>) | <digit>
<digit> ::= 0-9
'''
from typing import Dict, Tuple, Optional, List

# Transition= word, pop, push
Transition = (str, str, str)
WORD = 0
POP = 1
PUSH = 2
State = int

# TOKENS. Elementele atomice pe care le-am putea gasi intr-o expresie aritmetica
EPS = ""
PLUS = "+"
OPEN = "("
CLOSE = ")"
DIGITS = [chr(digit) for digit in range(ord('0'), ord('9') + 1)]


class PDA:
    def __init__(self):
        self.states: List[State] = [0, 1]
        self.initialState: State = 0
        self.finalStates: List[State] = [1]

        self.transitions: Dict[Tuple[State, Transition], State] = {}

        self.transitions[0, (OPEN, EPS, OPEN)] = 0
        for digit in DIGITS:
            self.transitions[0, (digit, EPS, EPS)] = 1

        self.transitions[1, (CLOSE, OPEN, EPS)] = 1
        self.transitions[1, (PLUS, EPS, EPS)] = 0

        self.stack: Stack = Stack()

    def nextState(self, currentState: State, word: str) -> Optional[State]:
        # Trecem prin toate tranzitiile PDA-ului
        for (state, transition) in self.transitions.keys():
            # Ne asiguram ca tranzitiile sunt pentru starea in care ne aflam
            if state == currentState:
                # Ne asiguram ca tranzitia este pentru litera curenta de consumat
                if word[0] == transition[WORD]:
                    # In cazul in care tranzitia cere un anumit TOKEN in varful stivei caruia
                    # sa ii faca pop, atunci ne asiguram ca acesta se afla in varful stivei
                    if transition[POP] == EPS or self.stack.peek(0) == transition[POP]:
                        # Daca avem ceva de scos de pe stiva, ii dam pop
                        if transition[POP] != EPS:
                            self.stack.pop()
                        # Daca avem ceva de pus pe stiva, facem push
                        if transition[PUSH] != EPS:
                            self.stack.push(transition[PUSH])

                        # Returnam starea urmatoare
                        return self.transitions[(state, transition)]

        # Nu avem o tranzitie valida pentru configuratia curenta
        return None

    # 1. Suntem intr-o stare finala blocati
    # 2. Cuvantul a fost consumat integral
    # 3. Stiva este goala
    def accept(self, word: str) -> bool:
        currentState = self.initialState

        while word != EPS:
            currentState = self.nextState(currentState, word)
            if currentState is None:
                break
            word = word[1:]

        return currentState in self.finalStates and word == EPS and self.stack.size() == 0


input = "(1)"
pda = PDA()
print(pda.accept(input))

'''
    2. Adaugam clase pentru Plus, Number si Par, toate extinzand Expr.
    Fiecare clasa va avea nevoie de functia printTree(tabs) care sa printeze
    sub forma unui arbore.
'''


class Expr:
    def printTree(self, tabs: int):
        return ""

    def eval(self):
        return None


class Plus(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left: Expr = left
        self.right: Expr = right

    def printTree(self, tabs: int):
        print("\t" * tabs + "+")
        self.left.printTree(tabs + 1)
        self.right.printTree(tabs + 1)

    def eval(self):
        return self.left.eval() + self.right.eval()


class Par(Expr):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

    def printTree(self, tabs: int):
        print("\t" * tabs + "(")
        self.expr.printTree(tabs + 1)
        print("\t" * tabs + ")")

    def eval(self):
        return self.expr.eval()


class Number(Expr):
    def __init__(self, num: str):
        self.num = num

    def printTree(self, tabs: int):
        print("\t" * tabs + "Number(" + self.num + ")")

    def eval(self):
        return int(self.num)


'''
    3. Cream pe baza PDA-ului un simplu parser. In cazul parserului, putem sa consideram ca avem doar 2 optiuni.
        a) shift = mergem mai departe prin cuvant
        b) reduce = suntem la finalul unei reguli, putem reduce
        
    Trebuie sa avem grija insa de 2 conflicte de care ne putem lovi:
        a) reduce-reduce -> 2 reguli pot fi aplicate, trebuie sa alegem doar 1. Din fericire, nu avem astfel de
        conflicte in cazul nostru
        b) shift-reduce -> putem reduce regula acum sau sa mergem mai departe.
        Poate fi o problema in cazul E + E * E
        Trebuie sa decidem daca E + E va fi redus in Plus sau adaugam * pe stiva
        
        In cazul gramaticii noastre, vom reduce mereu doar *, iar + va fi redus doar la finalul stringului
        sau la aparitia unei ")".
        
        
        1 + (2 + 3)
        
        E -> E + E | (E) | D
        D -> 0-9
        
        
        1
        _
'''

class Parser:
    def __init__(self):
        self.states: List[State] = [0, 1]
        self.initialState: State = 0
        self.finalStates: List[State] = [1]

        self.transitions: Dict[Tuple[State, Transition], State] = {}

        self.transitions[0, (OPEN, EPS, OPEN)] = 0
        for digit in DIGITS:
            self.transitions[0, (digit, EPS, digit)] = 1

        self.transitions[1, (CLOSE, EPS, CLOSE)] = 1
        self.transitions[1, (PLUS, EPS, PLUS)] = 0

        self.stack: Stack = Stack()

    def nextState(self, currentState: State, word: str) -> Optional[State]:
        # Trecem prin toate tranzitiile PDA-ului
        for (state, transition) in self.transitions.keys():
            # Ne asiguram ca tranzitiile sunt pentru starea in care ne aflam
            if state == currentState:
                # Ne asiguram ca tranzitia este pentru litera curenta de consumat
                if word[0] == transition[WORD]:
                    # Daca avem ceva de pus pe stiva, facem push
                    if transition[PUSH] != EPS:
                        self.stack.push(transition[PUSH])

                    # Returnam starea urmatoare
                    return self.transitions[(state, transition)]

        # Nu avem o tranzitie valida pentru configuratia curenta
        return None

    def reduceNumber(self):
        digit = self.stack.pop()
        self.stack.push(Number(digit))

    def reducePar(self):
        self.stack.pop()
        prevExpr = self.stack.pop()
        self.stack.pop()
        self.stack.push(Par(prevExpr))

    def reducePlus(self):
        prevExpr1 = self.stack.pop()
        self.stack.pop()
        prevExpr2 = self.stack.pop()
        self.stack.push(Plus(prevExpr2, prevExpr1))

    # 1 + 2 + 3 * 4
    #

    def reduce(self) -> bool:
        if self.stack.peek(0) in DIGITS:
            self.reduceNumber()
            return True
        if self.stack.peek(0) == ")":
            self.reducePar()
            return True
        if self.stack.peek(1) == "+" and isinstance(self.stack.peek(0), Expr):
            self.reducePlus()
            return True

        return False

    # 1. Suntem intr-o stare finala blocati
    # 2. Cuvantul a fost consumat integral
    # 3. Stiva este goala
    def parse(self, word: str) -> Optional[Expr]:
        currentState = self.initialState

        while word != EPS:
            currentState = self.nextState(currentState, word)
            if currentState is None:
                break
            word = word[1:]

            while self.reduce():
                continue

        if word != EPS and self.stack.size() != 1:
            return None

        return self.stack.pop()


parser = Parser()
expr = parser.parse("1+(2+3)")
if expr is not None:
    expr.printTree(0)
    print()
    print(expr.eval())

else:
    print("Nu am putut parsa cuvantul")
