import sys
import re
from dfa import DFA
from nfa import NFA
from regex import *
from pda_parser import *

if __name__ == '__main__':

    # Obtinem string-ul care defineste Regex-ul
    input_file = open(str(sys.argv[1]), "r")
    regex_string = input_file.readline()
    input_file.close()

    # Parsam sirul pentru a obtine o instanta Regex
    parser = PDAParser(regex_string)
    regex = parser.parse(regex_string)

    # Convertim Regex-ul la NFA folosind algoritmul lui Thompson
    nfa = regex.regex_to_nfa()

    # Se scrie NFA-ul in fisier sub formatul cerut
    output_file1 = open(str(sys.argv[2]), "w")
    nfa.write_nfa_in_file(output_file1)
    output_file1.close()

    # Construim DFA-ul pe baza NFA-ului primit
    dfa = DFA()
    dfa.compute_dfa(nfa)

    # Se scrie DFA-ul in fisier sub formatul cerut
    output_file2 = open(str(sys.argv[3]), "w")
    dfa.write_dfa_in_file(output_file2)
    output_file2.close()