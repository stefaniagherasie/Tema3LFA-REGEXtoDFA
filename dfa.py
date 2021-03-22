class DFA:

    def __init__(self):
        self.num_states = 0
        self.final_states = []
        self.dfa_transitions = []
        self.dfa_states = []

    # Obtine starile urmatoare corespunzatoare unei liste de stari,
    # folosind trazitiile de pe un anumit simbol
    def get_next_dfa_states(self, symbol, states, transitions):
        # Am folosit set() pentru a evita dublicatele
        next_dfa_states = set()

        for state in states:
            for transition in transitions[state]:
                if transition[0] == symbol:
                    next_states = transition[1]
                    next_dfa_states.update(next_states)
        next_dfa_states = list(next_dfa_states)
        return next_dfa_states

    # Obtine tranzitiile din DFA, in acelasi timp construind starile DFA-ului
    def compute_dfa_transitions(self, nfa):
        # Se obtin valorile inchiderilor cu epsilon din NFA
        epsilon = nfa.compute_eps_closure()

        # Pentru fiecare stare din DFA se considera epsilon(stare) ca stari succesor
        # Consideram 0 starea initiala, epsilon(0) fiind prima stare din DFA
        self.dfa_states.append(epsilon[0])

        # Se parcurg toate starile din DFA
        for dfa_state in self.dfa_states:
            # Pentru fiecare simbol se afla starea urmatoare
            for symbol in nfa.symbols:
                # Se obtin ca lista starile urmatoare
                next_states = self.get_next_dfa_states(symbol, dfa_state, nfa.transitions)

                # Se concateneaza si epsilon de fiecare stare
                for next_st in next_states:
                    next_states = next_states + epsilon[next_st]
                # Pentru a evita dublicatele
                next_states = list(set(next_states))

                # Se adauga tranzitia sub forma de tuplu (stare1, simbol, stare2)
                new_transition = (dfa_state, symbol, next_states)
                self.dfa_transitions.append(new_transition)

                # Se adauga starea obtinuta in lista de stari din DFA
                # daca nu a fost intalnita deja
                if next_states not in self.dfa_states:
                    self.dfa_states.append(next_states)
        return

    # Obtine starile finale din DFA, adica starile care contin o stare finala a NFA-ului
    def compute_dfa_final_states(self, nfa):
        for dfa_state in self.dfa_states:
            for final_state in nfa.final_states:
                if final_state in dfa_state:
                    self.final_states.append(dfa_state)
        return

    # Se scrie DFA-ul in fisier sub formatul cerut
    def write_dfa_in_file(self, output_file):
        # Se scrie numarul de stari din DFA
        output_file.write(str(self.num_states))
        output_file.write('\n')

        # Se scriu starile finale cu noua notatie
        # Starile primesc ca nou nume indexul lor din self.dfa_states
        code = self.dfa_states.index(self.final_states[0])
        output_file.write(str(code))
        for final_state in self.final_states[1:]:
            code = self.dfa_states.index(final_state)
            output_file.write(" " + str(code))
        output_file.write('\n')

        # Se scriu tranzitiile in fisier
        for trans in self.dfa_transitions:
            code1 = self.dfa_states.index(trans[0])
            code2 = self.dfa_states.index(trans[2])
            transition = str(code1) + " " + trans[1] + " " + str(code2) + '\n'
            output_file.write(transition)
        return

    # Obtine specificatiile DFA-ului
    def compute_dfa(self, nfa):
        self.compute_dfa_transitions(nfa)
        self.compute_dfa_final_states(nfa)
        self.num_states = len(self.dfa_states)

