from nfa import NFA
'''
   <regex> ::= <regex> . <regex> |
               <regex> | <regex> |
               <regex> * |
               (<regex>) |
               <symbol>
'''


class Regex:
    def regex_to_nfa(self) -> NFA:
        pass

    def print_tree(self, tabs: int) -> str:
        return ""


class Symbol(Regex):       # a
    def __init__(self, ch):
        self.symbol = ch

    def regex_to_nfa(self) -> NFA:
        # Un simbol "a" din alfabetul de intrare este convertit
        # la un NFA cu 2 stari si o tranzitie pe "a" intre ele
        alphabet = [self.symbol]
        num_states = 2
        start_state = 0
        final_states = [1]
        states = [0, 1]

        transitions = {}
        transitions[0] = [(self.symbol, [1])]
        transitions[1] = []

        return NFA(num_states, states, start_state, final_states, alphabet, transitions)

    def print_tree(self, tabs: int):
        print("\t" * tabs + "Symbol(" + self.symbol + ")")


class Concat(Regex):        # a.b
    def __init__(self, lhs: Regex, rhs: Regex):
        self.lhs: Regex = lhs
        self.rhs: Regex = rhs

    def regex_to_nfa(self) -> NFA:
        # Se obtin cele 2 NFA-uri care vor fi concatenate
        lhs_nfa = self.lhs.regex_to_nfa()
        rhs_nfa = self.rhs.regex_to_nfa()

        # Pentru NFA-ul din dreapta se vor redenumi starile pentru a evita conflicte de nume
        rhs_nfa.rename_states(max(lhs_nfa.states) + 1)

        # Se stabileste care este alfabetul NFA-ului, adaugand si 'eps' pt ε-tranzitii
        alphabet = lhs_nfa.symbols + rhs_nfa.symbols
        alphabet += ['eps']
        alphabet = list(set(alphabet))

        num_states = lhs_nfa.num_states + rhs_nfa.num_states
        # Starea initiala a lui lhs_nfa este starea initiala a intregului NFA
        # Starea finala a lui rhs_nfa este starea finala a intregului NFA
        start_state = lhs_nfa.start_state
        final_states = rhs_nfa.final_states
        states = lhs_nfa.states + rhs_nfa.states
        states = list(set(states))

        # Se adauga toate tranzitiile din NFA-uri si noile ε-tranzitii
        transitions = {}
        transitions.update(lhs_nfa.transitions)
        transitions.update(rhs_nfa.transitions)

        for final_state in lhs_nfa.final_states:
            if final_state not in transitions.keys():
                transitions[final_state] = [('eps', [rhs_nfa.start_state])]
            else:
                transitions[final_state].append(('eps', [rhs_nfa.start_state]))

        # Daca vreo stare nu apare in dictionar, o adaugam
        for state in states:
            if state not in transitions.keys():
                transitions[state] = []

        return NFA(num_states, states, start_state, final_states, alphabet, transitions)

    def print_tree(self, tabs: int):
        print("\t" * tabs + ".")
        self.lhs.print_tree(tabs + 1)
        self.rhs.print_tree(tabs + 1)


class Star(Regex):             # a*
    def __init__(self, expr: Regex):
        self.expr: Regex = expr

    def regex_to_nfa(self) -> NFA:
        # Se obtine NFA-ul subexpresiei pe care se aplica Star
        sub_nfa = self.expr.regex_to_nfa()
        # Se redenumesc starile deoarece vom adauga 2 stari si 'eps' tranzitii
        sub_nfa.rename_states(1)

        # Se stabileste care este alfabetul NFA-ului, adaugand si 'eps' pt ε-tranzitii
        alphabet = sub_nfa.symbols + ['eps']
        alphabet = list(set(alphabet))

        # adaugam 2 stari si le codificam cu 0 si max(sub_nfa.states) + 1
        num_states = sub_nfa.num_states + 2
        start_state = 0
        final_states = [max(sub_nfa.states) + 1]
        states = sub_nfa.states + [start_state, final_states[0]]
        states = list(set(states))

        # Se adauga toate tranzitiile din NFA-ul subexpresiei si noile ε-tranzitii
        transitions = sub_nfa.transitions

        transitions[start_state] = [('eps', [sub_nfa.start_state, final_states[0]])]

        for final_state in sub_nfa.final_states:
            if final_state not in transitions.keys():
                transitions[final_state] = [('eps', [sub_nfa.start_state, final_states[0]])]
            else:
                transitions[final_state].append(('eps', [sub_nfa.start_state, final_states[0]]))

        # Daca vreo stare nu apare in dictionar, o adaugam
        for state in states:
            if state not in transitions.keys():
                transitions[state] = []

        return NFA(num_states, states, start_state, final_states, alphabet, transitions)

    def print_tree(self, tabs: int):
        print("\t" * tabs + "*")
        self.expr.print_tree(tabs + 1)


class Union(Regex):         # a|b
    def __init__(self, lhs: Regex, rhs: Regex):
        self.lhs: Regex = lhs
        self.rhs: Regex = rhs

    def regex_to_nfa(self) -> NFA:
        # Se obtin cele 2 NFA-uri peste care se va aplica Union
        up_nfa = self.lhs.regex_to_nfa()
        down_nfa = self.rhs.regex_to_nfa()

        # Se redenumesc starile deoarece vom adauga 2 stari si 'eps' tranzitii
        up_nfa.rename_states(1)
        down_nfa.rename_states(1 + up_nfa.num_states)

        # Se stabileste care este alfabetul NFA-ului, adaugand si 'eps' pt ε-tranzitii
        alphabet = up_nfa.symbols + down_nfa.symbols + ['eps']
        alphabet = list(set(alphabet))

        # adaugam 2 stari si le codificam cu 0 si max(down_nfa.states) + 1
        num_states = up_nfa.num_states + down_nfa.num_states + 2
        start_state = 0
        final_states = [max(down_nfa.states) + 1]
        states = up_nfa.states + down_nfa.states + [start_state, final_states[0]]
        states = list(set(states))

        # Se adauga toate tranzitiile din NFA-uri si noile ε-tranzitii
        transitions = {}
        transitions.update(up_nfa.transitions)
        transitions.update(down_nfa.transitions)

        transitions[0] = [('eps', [up_nfa.start_state, down_nfa.start_state])]
        for final_state in up_nfa.final_states:
            if final_state not in transitions.keys():
                transitions[final_state] = [('eps', [final_states[0]])]
            else:
                transitions[final_state].append(('eps', [final_states[0]]))

        for final_state in down_nfa.final_states:
            if final_state not in transitions.keys():
                transitions[final_state] = [('eps', [final_states[0]])]
            else:
                transitions[final_state].append(('eps', [final_states[0]]))

        # Daca vreo stare nu apare in dictionar, o adaugam
        for state in states:
            if state not in transitions.keys():
                transitions[state] = []

        return NFA(num_states, states, start_state, final_states, alphabet, transitions)

    def print_tree(self, tabs: int):
        print("\t" * tabs + "|")
        self.lhs.print_tree(tabs + 1)
        self.rhs.print_tree(tabs + 1)


# Marcheaza ca trebuie facuta o uniune
class UnionMark(Regex):
    def print_tree(self, tabs: int):
        print("\t" * tabs + "UnionMark")


# Marcheaza ca avem o paranteza deschisa
class OpenPar(Regex):       # "("
    def print_tree(self, tabs: int):
        print("\t" * tabs + "(")


# Marcheaza ca avem o paranteza deschisa
class ClosePar(Regex):      # ")"
    def print_tree(self, tabs: int):
        print("\t" * tabs + ")")

