from typing import Dict, Tuple, Optional, List
from regex import *
from stack import Stack

EPS = ""
CONCAT = "."
UNION = "|"
STAR = "*"
OPEN = "("
CLOSE = ")"

Transition = (str, str, str)
WORD = 0
POP = 1
PUSH = 2
State = int


class PDAParser:
    def __init__(self, regex_string):
        # Construim alfabetul pe baza string-ului primit
        self.alphabet = []
        for symbol in regex_string:
            if symbol.isalpha() and symbol not in self.alphabet:
                self.alphabet.append(symbol)

        self.states: List[State] = [0, 1]
        self.start_state: State = 0
        self.final_states: List[State] = [1]

        self.transitions: Dict[Tuple[State, Transition], State] = {}

        self.transitions[0, (OPEN, EPS, OPEN)] = 0
        for symbol in self.alphabet:
            self.transitions[0, (symbol, EPS, symbol)] = 1

        self.transitions[1, (CLOSE, EPS, CLOSE)] = 1
        self.transitions[1, (STAR, EPS, STAR)] = 1
        self.transitions[1, (UNION, EPS, UNION)] = 0
        self.transitions[1, (CONCAT, EPS, CONCAT)] = 0

        self.stack: Stack = Stack()

    def next_state(self, currentState: State, word: str) -> Optional[State]:
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

    # Reduce o expresie aflata intre paranteze
    def reduce(self):
        # Daca in varful stivei se afla o paranteza inchisa, aceasta se elimina
        peek = self.stack.peek(0)
        if isinstance(peek, ClosePar):
            self.stack.pop()

        # In rhs_union salvam partea din dreapta al unui Union, daca e cazul
        rhs_union = Regex()
        isInUnion = False

        while True:
            # Cand dam de o paranteza deschisa am terminat de redus expresia dintre paranteze
            if isinstance(self.stack.peek(1), OpenPar):
                # Salvam in peek ce era inainte de paranteza
                peek = self.stack.pop()
                # Se scoate OpenPar de pe stiva
                self.stack.pop()

                # Se pune inapoi pe stiva expresia redusa
                if isInUnion is False:
                    self.stack.push(peek)
                else:
                    # Daca eram in Union, ce era in varful stivei reprezinta partea
                    # din stanga al unui Union
                    union_regex = Union(peek, rhs_union)
                    self.stack.push(union_regex)
                    isInUnion = False
                return

            # Cand avem 2 regex-uri care nu sunt Union in varful stivei, le concatenam
            elif (not isinstance(self.stack.peek(0), UnionMark)) \
                    and (not isinstance(self.stack.peek(1), UnionMark)):
                peek0 = self.stack.pop()
                peek1 = self.stack.pop()
                self.stack.push(Concat(peek1, peek0))

            # Cand pe pozitia 1 in stiva este un UnionMark, suntem intr-un Union si ce era
            # in varful stivei reprezinta rhs al uniunii
            elif (not isinstance(self.stack.peek(0), UnionMark)) \
                    and (isinstance(self.stack.peek(1), UnionMark)) and (isInUnion is False):
                #  Se scoate rhs pentru Union si se salveaza in rhs_union
                peek = self.stack.pop()
                rhs_union = peek
                isInUnion = True
                # Se scoate si UnionMark de pe stiva
                self.stack.pop()

            # Cand pe pozitia 1 in stiva este un UnionMark, dar suntem deja intr-o uniune,
            # in varful stivei se afla lhs pentru Union anterior.
            elif (not isinstance(self.stack.peek(0), UnionMark)) \
                    and (isinstance(self.stack.peek(1), UnionMark)) and (isInUnion is True):
                #  Se scoate lhs pentru Union de pe stiva
                peek = self.stack.pop()
                isInUnion = False

                # Se pune pe stiva Union care s-a format si se lasa UnionMark pentru
                # a continua procesul de uniune
                union_regex = Union(peek, rhs_union)
                self.stack.push(union_regex)

    # Parseaza string-ul pana cand pe stiva se afla o singura instanta Regex()
    def parse(self, regex_str):

        for i in range(len(regex_str)):
            symbol = regex_str[i]

            if symbol in self.alphabet:
                self.stack.push(Symbol(symbol))

            elif symbol == OPEN:
                self.stack.push(OpenPar())

            # Cand s-a inchis o paranteza se reduce tot ce era in
            # in interiorul ei si se pune in varful stivei
            elif symbol == CLOSE:
                self.stack.push(ClosePar())
                self.reduce()

            # Pentru STAR, se aplica Star pe ce era in varful stivei
            elif symbol == STAR:
                peek = self.stack.pop()
                # Daca deja avem un Star pe stiva, nu se mai aplica din nou Star
                # pentru a evita star-uri redundante
                if isinstance(peek, Star):
                    self.stack.push(peek)
                else:
                    self.stack.push(Star(peek))

            # Pentru UNION, se pune pe stiva UnionMark ca sa marcheze ca trebuie facuta
            # uniunea atunci cand se reduce expresia
            elif symbol == UNION:
                self.stack.push(UnionMark())

        # Facem o reducere finala, concatenand ce era pe stiva, daca este cazul
        if self.stack.size() != 1:
            self.stack.add(OpenPar())
            self.reduce()

        # In varful stivei se afla Regex-ul final
        return self.stack.peek(0)
