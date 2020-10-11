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
            resulting_states.append(tuple(sorted(temp, key = int)))
    return resulting_states


# delta_afd: {'1': [('0',)], '0': [('0', '1'), ('1',)], ('0', '1'): [('0', '1'), ('1',)]}
# symbols: ['1', '2']
# delta: {'1': ['-1', '0', '-1', ('1',)], '0': ['1', '2', '-1', ('0', '1')], '2': ['-1', '1', ('1', '2'), ('2',)]}

def set_state_transitions_afd(delta, state, symbols):
    transitions = ['-1']
    if '0' in symbols:
        symbols.remove('0')
    if state == '-1':
        for t in range(len(symbols)-1):
            transitions.append('-1')
        return transitions

    # for s in state: # s = ('0', '1') para cada estado dentro do estado 0 e 1
    #     states = []
    #     for i in symbols: # pra cada simbolo
    #         temp_state = delta[s][int(i)] # ('0', '1')
    #         if temp_state != '-1':
    #             E_states = get_E(delta, temp_state) # ('0', '1')
    #             states.append(E_states)
    states = []
    for symbol in symbols: # para cada simbolo
        temp = []
        for s in state: # para cada estado dentro do estado
            temp_state = delta[s][int(symbol)]
            if temp_state == '-1':
                continue
            E_states = get_E(delta, temp_state)
            for e in E_states:
                temp.append(e)
        if temp:
            if len(temp) == 1:
                states.append(temp[0])
            else:
                temp = list(set(temp))
                states.append(tuple(sorted(temp, key = int)))
        else: # temp vazio
            states.append('-1')
    transitions.append(states)
    transitions.remove('-1')
    return list(transitions)[0]

def get_E(delta, state):
    if state == '-1':
        return '-1'
    states = {'-1'}
    for s in state: # ('0', '1')
       temp = delta[s][-1]
       for i in temp:
           states.add(i)
    states.remove('-1')
    # if len(states) == 1:
    #     states = str(list(states)[0])
    return tuple(sorted(states, key = int))

def state_has_zero(transitions_list, state):
    states = []
    for transition in transitions_list:
        if transition[0] == state and transition[1] == '0':
            states.append(transition[2])
    return states

def set_E(transitions_list, state):
    temp = [state]
    for t in temp:
        states = state_has_zero(transitions_list, t)
        for state in states:
            if state not in temp:
                temp.append(state)
    # if len(states) == 1:
    #     states = str(list(states)[0])
    return tuple(sorted(temp, key = int))

# def test_automata(delta_afd, initial_state, acception_states, chain):
#     states = [initial_state]
#     with open(args.output, 'a') as output:
#         for symbol in chain:
            # print('delta_afd:')
            # print(delta_afd)
            # print('states:')
            # print(states)
            # print('symbol:')
            # print(symbol)
            # states.append(delta_afd[states[-1]][int(symbol)])
        # print(states)


# with open(args.output, 'a') as output:
#     output.write()

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
            delta[state].append(set_E(transitions, state))
        if state_has_zero(transitions, initial_state):
            initial_state = set_E(transitions, initial_state)
        states_delta_afd = [initial_state]
        delta_afd = {}
        for s in states_delta_afd:
            x = set_state_transitions_afd(delta, s, symbols)
            delta_afd[s] = x
            for t in x:
                if len(t) == 1:
                    new_t = ''.join(t)
                else:
                    new_t = t
                if new_t not in states_delta_afd:
                    states_delta_afd.append(new_t)
        # TESTES
        num_of_test_chains = input.readline()
        test_chains = []
        for chain in range(int(num_of_test_chains)):
            test_chains.append(input.readline().rstrip().split(' '))
        # for chain in test_chains:
            # test_automata(delta_afd,initial_state,acception_states,chain)

        # print('description: ')
        # print(description)
        # print('initial_state: ')
        # print(initial_state)
        # print('states: ')
        # print(states)
        # print('symbols: ')
        # print(symbols)
        # print('acception_states: ')
        # print(acception_states)
        # print('num_of_transitions: ' + num_of_transitions)
        # print('transitions: ')
        # print(transitions)
        print('delta:')
        print(delta)
        print('delta_afd:')
        print(delta_afd)
        # print('num_of_test_chains: ' + num_of_test_chains)
        # print('test_chains: ')
        # print(test_chains)
input.close()

# converter tupla em string
# t = ('3',)
# s = ''.join(t)