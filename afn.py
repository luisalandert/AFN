def set_state_transitions(transitions_list, state, symbols):
    resulting_states = []
    for symbol in symbols:
        temp = []
        for i in transitions_list:
            if (i[0] == state) and (i[1] == symbol):
                temp.append(str(i[2]))
        if not temp:
            resulting_states.append(('-1',))
        else:
            resulting_states.append(tuple(temp))
    return resulting_states

output = open('output.txt', 'a')

with open('input.txt') as txt:
    num_of_automata = txt.readline()
    for automata in range(int(num_of_automata)):
        print('automata:')
        # LEITURA DADOS
        description = txt.readline().rstrip().split(' ')
        initial_state = description[3]
        states = range(int(description[0]))
        for i in states:
            states[i] = str(states[i])
        symbols = range(int(description[1]))
        for i in symbols:
            symbols[i] = str(symbols[i])
        acception_states = txt.readline().rstrip().split(' ')
        num_of_transitions = description[2]
        transitions = []
        print('description: ')
        print(description)
        print('initial_state: ' + initial_state)
        print('states: ')
        print(states)
        print('symbols: ')
        print(symbols)
        print('acception_state: ')
        print(acception_states)
        print('num_of_transitions: ' + num_of_transitions)
        for transition in range(int(num_of_transitions)):
            transitions.append(txt.readline().rstrip().split(' '))
        print('transitions: ')
        print(transitions)
        # CONSTRUCAO AUTOMATO
        delta = {}
        for state in states:
            delta[state] = set_state_transitions(transitions, state, symbols)
        print('delta:')
        print(delta)
        
        # TESTES
        num_of_test_chains = txt.readline()
        print('num_of_test_chains: ' + num_of_test_chains)
        test_chains = []
        for chain in range(int(num_of_test_chains)):
            test_chains.append(txt.readline().rstrip().split(' '))
        print('test_chains: ')
        print(test_chains)

        # output.write("\n")
txt.close()



