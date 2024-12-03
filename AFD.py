from graphviz import Digraph; 

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states  # Conjunto de estados
        self.alphabet = alphabet  # Alfabeto
        self.transitions = transitions  # Diccionario de transiciones
        self.start_state = start_state  # Estado inicial
        self.accept_states = accept_states  # Estados de aceptación

def dfa_to_regular_grammar(dfa):
    grammar = {"non_terminals": set(), "terminals": set(), "productions": {}, "start_symbol": None}

    # Los no terminales son los estados del DFA
    grammar["non_terminals"] = dfa.states

    # Los terminales son los símbolos del alfabeto del DFA
    grammar["terminals"] = dfa.alphabet

    # El símbolo inicial es el estado inicial del DFA
    grammar["start_symbol"] = dfa.start_state

    # Construir las producciones
    for state in dfa.states:
        grammar["productions"][state] = []

        # Para cada símbolo en el alfabeto, agregar las transiciones
        for symbol in dfa.alphabet:
            if state in dfa.transitions and symbol in dfa.transitions[state]:
                destination = dfa.transitions[state][symbol]
                grammar["productions"][state].append((symbol, destination))

        # Si el estado actual es de aceptación, agregar una producción con ε
        if state in dfa.accept_states:
            grammar["productions"][state].append(("ε", None))  # None representa la cadena vacía

    return grammar


def print_grammar(grammar):
    print("Non-terminals:", grammar["non_terminals"])
    print("Terminals:", grammar["terminals"])
    print("Start Symbol:", grammar["start_symbol"])
    print("Productions:")
    for non_terminal, rules in grammar["productions"].items():
        rules_str = " | ".join(
            f"{symbol}{destination if destination else ''}" for symbol, destination in rules
        )
        print(f"  {non_terminal} -> {rules_str}")



def plot_dfa(dfa, output_file="dfa", file_format="png"):
    """
    Genera un diagrama del AFD usando Graphviz.
    :param dfa: Objeto DFA que contiene todos los elementos del autómata.
    :param output_file: Nombre del archivo de salida.
    :param file_format: Formato de imagen de salida (por defecto 'png').
    """
    dot = Digraph(format=file_format)

    # Agregar estados
    for state in dfa.states:
        if state in dfa.accept_states:
            dot.node(state, shape="doublecircle")  # Estados de aceptación
        else:
            dot.node(state, shape="circle")  # Estados normales

    # Agregar marcador de estado inicial
    if dfa.start_state:
        dot.node("start", shape="point")  # Nodo invisible para la entrada inicial
        dot.edge("start", dfa.start_state)

    # Agregar transiciones
    for state, symbol_dict in dfa.transitions.items():
        for symbol, next_state in symbol_dict.items():
            dot.edge(state, next_state, label=symbol)

    # Generar el diagrama
    dot.render(output_file, cleanup=True)
    print(f"DFA diagram generated: {output_file}.{file_format}")

