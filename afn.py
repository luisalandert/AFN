# coding=UTF-8

# Luísa Dipierri Landert           8010698
# Natália de Ávila Degasperi       11207901

# OBSERVAÇÕES:
# O processamento dos dados do arquivo de texto em estruturas que representam o autômato
# foi feito em funções separadas, explicadas brevemente nos comentários e com exemplo de
# parâmetros e a saída.
# para indicar transições que não existem nos dicionários delta e delta_afd
# (que representam as tabelas de transições) é utilizado '-1'.

# RESET NO ARQUIVO DE SAIDA
open('saida.txt', 'w').close()

# Função que devolve as transições de um estado do AFN
# Exemplo de parâmetros:
# TRANSITION_LIST: [['0', '1', '0'], ['0', '1', '1'], ['0', '2', '1'], ['1', '2', '0']]
# STATE: 0
# SYMBOLS: ['0', '1', '2']
# Exemplo da saída: ['-1', ('0', '1'), '1']
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

# Função que devolve as transições de um estado do AFD equilavente
# Exemplo de parâmetros:
# DELTA: {'1': ['-1', '-1', '0', '1'], '0': ['-1', ('0', '1'), '1', '0']}
# STATE: 0
# SYMBOLS: ['0', '1', '2']
# Exemplo da saída: [('0', '1'), '1']
# OBS: no caso do delta_afd (representação da tabela de transição do afd equilvalente)
# o caso do 0, ou seja, cadeia vazia não entra como 'coluna' nessa estrutura pois já é
# considerado nos estados e as mudanças necessárias são feitas lá.
def set_state_transitions_afd(delta, state, symbols):
    transitions = ['-1']
    if '0' in symbols:
        symbols.remove('0')
    if state == '-1':
        for t in range(len(symbols)-1):
            transitions.append('-1')
        return transitions
    states = []
    for symbol in symbols:
        temp = []
        for s in state:
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
        else:
            states.append('-1')
    transitions.append(states)
    transitions.remove('-1')
    return list(transitions)[0]

# Função que devolve os estados alcançáveis com transições com zero (cadeia vazia)
# a partir do estado.
# Usada para auxiliar na construção do delta_afd (tabela de transição do AFD equivalente)
# Exemplo de parâmetros:
# DELTA: {'1': ['-1', '-1', '0', '1'], '0': ['-1', ('0', '1'), '1', '0']}
# STATE: ('0', '1')
# *esse seria um estado de um autômato que com cadeia vazia acessa os estados '0' e '1'
# Exemplo da saída: ('0', '1')
# *a partir do estado '('0', '1')' e com o delta apresentado é possível acessar os estados '0' e '1'
def get_E(delta, state):
    if state == '-1':
        return '-1'
    states = {'-1'}
    for s in state:
       temp = delta[s][-1]
       for i in temp:
           states.add(i)
    states.remove('-1')
    return tuple(sorted(states, key = int))

# Checa se o estado tem transições com zero e retorna os estados para onde ocorre a bifurcação
# Exemplo de parâmetros:
# TRANSITION_LIST: [['0', '1', '0'], ['0', '1', '1'], ['0', '2', '1'], ['1', '2', '0']]
# STATE: 0
# Exemplo da saída: []
# *o estado '0' não tem transições com cadeia vazia
def state_has_zero(transitions_list, state):
    states = []
    for transition in transitions_list:
        if transition[0] == state and transition[1] == '0':
            states.append(transition[2])
    return states

# Função que calcula os estados alcançáveis para um determinado estado
# usada para obter a coluna 'E' da tabela de transição do AFN (delta) e
# o estado inicial do AFD equivalente quando tem transição com cadeia vazia
# a partir do estado inicial
# Exemplo de parâmetros:
# TRANSITION_LIST: [['0', '1', '0'], ['0', '1', '1'], ['0', '2', '1'], ['1', '2', '0']]
# STATE: 0
# Exemplo da saída: 0
def set_E(transitions_list, state):
    temp = [state]
    for t in temp:
        states = state_has_zero(transitions_list, t)
        for state in states:
            if state not in temp:
                temp.append(state)
    if len(temp) == 1:
        return str(list(temp)[0])
    return tuple(sorted(temp, key = int))

# Testa as cadeias para cada autômato e escreve a saída em saida.txt
# usa os símbolos lidos em cada cadeia e busca o estado após a leitura
# na tabela de transições do AFD equivalente (delta_afd)
def test_automata(delta_afd, initial_state, acception_states, test_chains):
    with open('saida.txt', 'a') as output:
        to_write = ''
        for chain in test_chains:
            states = [initial_state]
            if chain != ['0']:
                for symbol in chain:
                    states.append(delta_afd[states[-1]][int(symbol)-1])
            # checagem do estado final
            final_state = states[-1]
            chain_accepted = False
            for accepted_state in acception_states:
                if type(final_state) == str:
                    if final_state == accepted_state:
                        output.write('1 ')
                        chain_accepted = True
                        break
                else:
                    if accepted_state in final_state:
                        output.write('1 ')
                        chain_accepted = True
                        break
            if not chain_accepted:
                output.write('0 ')
        output.write("\n")
    output.close()

with open('entrada.txt', 'r') as input:
    num_of_automata = input.readline()
    for automata in range(int(num_of_automata)):
        # LEITURA DADOS
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
        # CONSTRUÇÃO AUTÔMATO
        # CONSTRUÇÃO DO DELTA DO AFN
        delta = {}
        for state in states:
            delta[state] = set_state_transitions(transitions, state, symbols)
            delta[state].append(set_E(transitions, state))
        # DEFINIÇÃO DO ESTADO INICIAL NO CASO DE TRANSIÇÃO COM CADEIA VAZIA
        if state_has_zero(transitions, initial_state):
            initial_state = set_E(transitions, initial_state)
        # CONSTRUÇÃO DO DELTA DO AFD EQUIVALENTE
        states_delta_afd = [initial_state]
        delta_afd = {}
        for state in states_delta_afd:
            transitions = set_state_transitions_afd(delta, state, symbols)
            delta_afd[state] = transitions
            for t in transitions:
                if len(t) == 1:
                    new_t = ''.join(t)
                else:
                    new_t = t
                if new_t not in states_delta_afd:
                    states_delta_afd.append(new_t)
        # LEITURA DOS TESTES
        num_of_test_chains = input.readline()
        test_chains = []
        for chain in range(int(num_of_test_chains)):
            test_chains.append(input.readline().rstrip().split(' '))
        # APLICACAO DOS TESTES
        test_automata(delta_afd, initial_state, acception_states, test_chains)
input.close()