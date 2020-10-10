import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='input',
                    help="input file", metavar='INPUT_FILE')
parser.add_argument('-o', dest='output',
                    help='output file', metavar='OUTPUT_FILE')
args = parser.parse_args()

def set_state_transitions(transitions_list, state, symbols):
    resulting_states = []
    for symbol in symbols:
        temp = []
        for i in transitions_list:
            if (i[0] == state) and (i[1] == symbol):
                temp.append(str(i[2]))
        if not temp:
            resulting_states.append('-1')
        elif len(temp) == 1:
            resulting_states.append(temp[0])
        else:
            resulting_states.append(tuple(temp))
    return resulting_states

def state_has_zero(transitions_list, state):
    states = []
    for transition in transitions_list:
        if transition[0] == state and transition[1] == '0':
            states.append(transition[2])
    return states

def get_E(transtitions_list, state):
    temp = [state]
    for t in temp:
        states = state_has_zero(transtitions_list, t)
        for state in states:
            if state not in temp:
                temp.append(state)
    return tuple(sorted(temp))


# with open(args.output, 'a') as output:
#     output.write("foi o teste\n")

with open(args.input, 'r') as input:
    num_of_automata = input.readline()
    for automata in range(int(num_of_automata)):
        print('automata:')

        # LEITURA DADOS obs: todos os estados devem ser tuplas
        description = input.readline().rstrip().split(' ')
        initial_state = description[3]
        states = range(int(description[0]))
        for i in states:
            states[i] = str(states[i])
        symbols = range(int(description[1]))
        for i in symbols:
            symbols[i] = str(symbols[i])
        acception_states = input.readline().rstrip().split(' ')
        num_of_transitions = description[2]
        transitions = []
        for transition in range(int(num_of_transitions)):
            transitions.append(input.readline().rstrip().split(' '))
        # CONSTRUCAO AUTOMATO
        delta = {}
        for state in states:
            delta[state] = set_state_transitions(transitions, state, symbols)
        if state_has_zero(transitions, initial_state):
            initial_state = get_E(transitions, initial_state)

        # TESTES
        num_of_test_chains = input.readline()
        test_chains = []
        for chain in range(int(num_of_test_chains)):
            test_chains.append(input.readline().rstrip().split(' '))

        print('description: ')
        print(description)
        print('initial_state: ')
        print(initial_state)
        print('states: ')
        print(states)
        print('symbols: ')
        print(symbols)
        print('acception_states: ')
        print(acception_states)
        print('num_of_transitions: ' + num_of_transitions)
        print('transitions: ')
        print(transitions)
        print('delta:')
        print(delta)
        print('num_of_test_chains: ' + num_of_test_chains)
        print('test_chains: ')
        print(test_chains)
input.close()

# converter tupla em string
# t = ('3',)
# s = ''.join(t)