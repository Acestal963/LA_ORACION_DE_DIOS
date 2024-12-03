import json
from AFD import DFA

class DFAUtils:
    @staticmethod
    def import_from_json(filename):
        with open(filename, "r") as file:
            data = json.load(file)

        # Verificar que las transiciones estén en el formato correcto
        print("Transitions loaded from JSON:", data["transitions"])

        # Construir las transiciones
        transitions = {}
        for state, symbol_dict in data["transitions"].items():
            if state not in transitions:
                transitions[state] = {}  # Iniciar un diccionario para este estado
            for symbol, next_state in symbol_dict.items():
                # Añadir transiciones, evitando duplicados
                transitions[state][symbol] = next_state

        # Crear el DFA a partir de los datos leídos del JSON
        return DFA(
            set(data["states"]),
            set(data["alphabet"]),
            transitions,
            data["start_state"],
            set(data["accept_states"]),
        )

    @staticmethod
    def export_to_json(dfa, filename):
        data = {
            "states": list(dfa.states),
            "alphabet": list(dfa.alphabet),
            "transitions": dfa.transitions,
            "start_state": dfa.start_state,
            "accept_states": list(dfa.accept_states),
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"DFA saved to {filename}")
