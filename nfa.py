
class NFA:

    def __init__(self, num_states, states, start_state, final_states, symbols, transitions):
        self.num_states = num_states
        self.final_states = final_states
        self.states = states
        self.symbols = symbols
        self.start_state = start_state
        self.transitions = transitions

    # Redenumeste toate starile adaugand un offset la valoarea lor
    def rename_states(self, offset: int):

        self.start_state += offset
        self.states = list(set(map(lambda x: x + offset, self.states)))
        self.final_states = list(set(map(lambda x: x + offset, self.final_states)))

        new_transitions = {}
        for key in self.transitions.keys():
            transition = []
            for (symbol, next_states) in self.transitions[key]:
                next_states = list(set(map(lambda x: x + offset, next_states)))
                transition.append((symbol, next_states))

            new_transitions[key + offset] = transition
        self.transitions = new_transitions

    # Functie recursiva care construieste in visited inchiderea cu epsilon
    # a fiecarei stari din NFA, pornind de la encodarile directe ale acestora
    def compute_eps_helper(self, direct_enc, state, visited):
        visited.append(state)
        for next_state in direct_enc[state]:
            if next_state not in visited:
                self.compute_eps_helper(direct_enc, next_state, visited)
        return

    # Functie care construieste inchiderea fiecarei stari din NFA
    def compute_eps_closure(self):
        # direct_enc contine starile accesibile printr-o singura tranzitie epsilon
        # complet_enc contine inchiderea cu epsilon a fiecarei stari
        direct_enc = {}
        complet_enc = {}
        for state in range(0, self.num_states):
            direct_enc[state] = []
            complet_enc[state] = []

        # Pentru fiecare stare se calculeaza direct_enc
        for state in self.states:
            direct_enc[state] = []
            transition = self.transitions[state]

            for i in range(0, len(transition)):
                if transition[i][0] == 'eps':
                    direct_enc[state] = transition[i][1]

        # Nu mai este nevoie de tranzitia 'eps' si pentru a ne ajuta mai
        # departe o sterg de acum din symbols
        if 'eps' in self.symbols:
            self.symbols.remove('eps')

        # Se calculeaza inchiderea cu epsilon pentru fiecare stare,
        # folosind vectorul visited si helper-ul
        for state in self.states:
            visited = []
            self.compute_eps_helper(direct_enc, state, visited)
            visited.sort()
            complet_enc[state] = visited

        return complet_enc

    # Construieste NFA-ul, citind informatiile din fisierul de intrare
    def compute_nfa_from_file(self, input_file):
        # Se obtine numarul de stari sin starile finale
        self.num_states = int(input_file.readline())
        self.final_states = [int(x) for x in input_file.readline().split()]
        for state in range(0, self.num_states):
            self.transitions[state] = []
            self.states.append(state)

        # Se citesc, pe rand, toate tranzitiile
        while True:
            line = input_file.readline().strip()
            if line == '':
                break
            line = line.split()

            # Se obtine starea de pornire si simbolul
            start_state = int(line[0])
            symbol = str(line[1])
            if symbol not in self.symbols:
                self.symbols.append(symbol)

            # Se obtin starile rezultat si se adauga toate tranzitiile obtinute
            end_states = [int(x) for x in line[2:]]
            transition = (symbol, end_states)
            self.transitions[start_state].append(transition)

        input_file.close()
        return

    # Se scrie NFA-ul in fisier sub formatul cerut
    def write_nfa_in_file(self, output_file):
        # Se scrie numarul de stari din NFA
        output_file.write(str(self.num_states))
        output_file.write('\n')

        # Se scriu starile finale ale automatului
        final_states = ' '.join([str(el) for el in self.final_states])
        output_file.write(final_states)
        output_file.write('\n')

        # Se scriu tranzitiile sub format (stare_initiala simbol stari_urmatoate)
        for key in self.transitions.keys():
            transitions = self.transitions[key]
            for trans in transitions:
                trans_str = str(key) + " " + trans[0] + " " + ' '.join([str(el) for el in trans[1]])
                output_file.write(trans_str)
                output_file.write('\n')
        output_file.close()
        return

