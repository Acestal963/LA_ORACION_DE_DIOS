import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QScrollArea,
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from DFAUtils import DFAUtils
from AFD import dfa_to_regular_grammar, DFA, plot_dfa


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DFA to Regular Grammar")
        self.setGeometry(100, 100, 800, 800)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # DFA Input
        self.states_label = QLabel("States (comma-separated):")
        self.states_input = QLineEdit()

        self.alphabet_label = QLabel("Alphabet (comma-separated):")
        self.alphabet_input = QLineEdit()

        self.start_state_label = QLabel("Start State:")
        self.start_state_input = QLineEdit()

        self.accept_states_label = QLabel("Accept States (comma-separated):")
        self.accept_states_input = QLineEdit()

        self.transitions_label = QLabel("Transitions (format: state,symbol->state):")
        self.transitions_input = QTextEdit()

        # Buttons
        self.convert_button = QPushButton("Convert to Regular Grammar")
        self.convert_button.clicked.connect(self.convert_dfa_to_grammar)

        self.plot_button = QPushButton("Generate and Show DFA Diagram")
        self.plot_button.clicked.connect(self.plot_and_display_dfa)

        self.export_button = QPushButton("Export DFA to JSON")
        self.export_button.clicked.connect(self.export_dfa)

        self.import_button = QPushButton("Import DFA from JSON")
        self.import_button.clicked.connect(self.import_dfa)

        # Output
        self.grammar_output_label = QLabel("Regular Grammar:")
        self.grammar_output = QTextEdit()
        self.grammar_output.setReadOnly(True)

        self.dfa_image_label = QLabel("DFA Diagram:")

        # Add a scrollable area for the DFA image
        self.dfa_image = QLabel()
        self.dfa_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.dfa_image)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(600, 400)  # Adjust as needed

        # Layout setup
        for widget in [
            self.states_label,
            self.states_input,
            self.alphabet_label,
            self.alphabet_input,
            self.start_state_label,
            self.start_state_input,
            self.accept_states_label,
            self.accept_states_input,
            self.transitions_label,
            self.transitions_input,
            self.convert_button,
            self.plot_button,
            self.export_button,
            self.import_button,
            self.grammar_output_label,
            self.grammar_output,
            self.dfa_image_label,
            self.scroll_area,  # Replace self.dfa_image with self.scroll_area
        ]:
            layout.addWidget(widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def read_dfa_inputs(self):
        try:
            states = set(self.states_input.text().split(","))
            alphabet = set(self.alphabet_input.text().split(","))
            start_state = self.start_state_input.text()
            accept_states = set(self.accept_states_input.text().split(","))
            transitions_raw = self.transitions_input.toPlainText().split("\n")
            transitions = {}
            for line in transitions_raw:
                if "->" in line:
                    part1, part2 = line.split("->")
                    state, symbol = part1.split(",")
                    if state.strip() not in transitions:
                        transitions[state.strip()] = {}
                    transitions[state.strip()][symbol.strip()] = part2.strip()
            return DFA(states, alphabet, transitions, start_state, accept_states)
        except Exception as e:
            raise ValueError(f"Invalid DFA input: {e}")

    def convert_dfa_to_grammar(self):
        try:
            dfa = self.read_dfa_inputs()
            grammar = dfa_to_regular_grammar(dfa)
            output = []
            for non_terminal, rules in grammar["productions"].items():
                rules_str = " | ".join(
                    f"{symbol}{destination if destination else ''}" for symbol, destination in rules
                )
                output.append(f"{non_terminal} -> {rules_str}")
            self.grammar_output.setText("\n".join(output))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert DFA: {str(e)}")

    def plot_and_display_dfa(self):
        try:
            dfa = self.read_dfa_inputs()  # Get the DFA object
            output_file = "dfa_diagram"
            plot_dfa(dfa, output_file, "png")

            # Load the image without scaling
            self.dfa_image.setPixmap(QPixmap(f"{output_file}.png"))

            # Adjust the scroll area size to fit the image dimensions dynamically
            self.dfa_image.adjustSize()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate DFA diagram: {str(e)}")

    def export_dfa(self):
        try:
            dfa = self.read_dfa_inputs()
            filename, _ = QFileDialog.getSaveFileName(self, "Save DFA", "", "JSON Files (*.json)")
            if filename:
                DFAUtils.export_to_json(dfa, filename)
                QMessageBox.information(self, "Success", "DFA exported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export DFA: {str(e)}")

    def import_dfa(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open DFA", "", "JSON Files (*.json)")
            if filename:
                dfa = DFAUtils.import_from_json(filename)
                self.states_input.setText(",".join(dfa.states))
                self.alphabet_input.setText(",".join(dfa.alphabet))
                self.start_state_input.setText(dfa.start_state)
                self.accept_states_input.setText(",".join(dfa.accept_states))
                transitions_str = "\n".join(
                    f"{state},{symbol}->{next_state}"
                    for state, trans in dfa.transitions.items()
                    for symbol, next_state in trans.items()
                )
                self.transitions_input.setText(transitions_str)
                QMessageBox.information(self, "Success", "DFA imported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import DFA: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
