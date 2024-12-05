# requirements pyside6, rdkit, padelpy, pyinstaller
# for making single executable "pyinstaller -F -n Descalculator_1.1 --add-data /home/administrator/piyush/projects/Descalculator/essentials:. test.py"

import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QRadioButton, QProgressBar, QFileDialog, QTextEdit, QMessageBox, QButtonGroup
)
from PySide6.QtCore import Qt, QThread, Signal
from rdkit import Chem
from rdkit.ML.Descriptors import MoleculeDescriptors
from rdkit.Chem import Descriptors
from padelpy import padeldescriptor
import os

# Worker thread for performing calculations to keep the GUI responsive
class CalculationThread(QThread):
    progress_signal = Signal(str)
    progress_bar_signal = Signal(int)
    finished_signal = Signal(str)

    def __init__(self, file_path, calc_descriptors, calc_fingerprints):
        super().__init__()
        self.file_path = file_path
        self.calc_descriptors = calc_descriptors
        self.calc_fingerprints = calc_fingerprints

    def run(self):
        try:
            # Load CSV file
            df = pd.read_csv(self.file_path)
            if "SMILES" not in df.columns:
                raise ValueError("The CSV file must contain a 'SMILES' column.")

            self.progress_signal.emit("File loaded successfully.")
            
            # Perform calculations based on selected options
            if self.calc_descriptors:
                self.progress_signal.emit("Calculating RDKit descriptors...")
                df = calculate_rdkit_descriptors(df)
            
            if self.calc_fingerprints:
                self.progress_signal.emit("Calculating PaDEL fingerprints...")
                df = calculate_padel_fingerprints(df)
            
            # Save the result
            output_file = "descriptors_and_fingerprints.csv"
            df.to_csv(output_file, index=False)
            self.progress_signal.emit(f"Calculation complete. Results saved to '{output_file}'")
            self.finished_signal.emit(output_file)
        except Exception as e:
            self.progress_signal.emit(f"Error: {str(e)}")

# Helper functions for RDKit descriptors and PaDEL fingerprints
def calculate_rdkit_descriptors(df, smiles_column="SMILES"):
    descriptor_names = [desc[0] for desc in Descriptors._descList]
    calc = MoleculeDescriptors.MolecularDescriptorCalculator(descriptor_names)
    
    rdkit_data = []
    for smiles in df[smiles_column]:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            descriptor_values = calc.CalcDescriptors(mol)
            rdkit_data.append(descriptor_values)
        else:
            rdkit_data.append([float('nan')] * len(descriptor_names))

    rdkit_df = pd.DataFrame(rdkit_data, columns=descriptor_names)
    return pd.concat([df.reset_index(drop=True), rdkit_df], axis=1)

def calculate_padel_fingerprints(df, smiles_column="SMILES", output_csv="fingerprints.csv"):
    smiles_file = "temp_smiles.smi"
    df[[smiles_column]].to_csv(smiles_file, index=False, header=False)

    padeldescriptor(
        mol_dir=smiles_file,
        d_file=output_csv,
        fingerprints=True,
        d_2d=False,
        d_3d=False,
        retainorder=True,
    )

    padel_df = pd.read_csv(output_csv)
    os.remove(smiles_file)
    os.remove(output_csv)

    return pd.concat([df.reset_index(drop=True), padel_df.drop(["Name"], axis=1)], axis=1)

# Main Window
class DescriptorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Descriptor & Fingerprint Calculator")
        self.setGeometry(200, 200, 600, 400)

        # Layouts
        layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Select CSV file:")
        self.file_path_label = QLabel("")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(browse_button)
        
        # Options
        options_layout = QHBoxLayout()
        self.descriptor_radio = QRadioButton("Calculate RDKit Descriptors")
        self.fingerprint_radio = QRadioButton("Calculate PaDEL Fingerprints")
        self.both_radio = QRadioButton("Calculate Both")
        self.descriptor_radio.setChecked(True)

        # Group radio buttons to enforce single selection
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.descriptor_radio)
        self.button_group.addButton(self.fingerprint_radio)
        self.button_group.addButton(self.both_radio)

        options_layout.addWidget(self.descriptor_radio)
        options_layout.addWidget(self.fingerprint_radio)
        options_layout.addWidget(self.both_radio)
        
        # Run button and progress display
        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run_calculation)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        
        # Add components to main layout
        layout.addLayout(file_layout)
        layout.addLayout(options_layout)
        layout.addWidget(run_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_text)
        
        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path_label.setText(file_path)
            self.file_path = file_path

    def run_calculation(self):
        if not hasattr(self, 'file_path'):
            QMessageBox.warning(self, "Warning", "Please select a CSV file first.")
            return
        
        calc_descriptors = self.descriptor_radio.isChecked() or self.both_radio.isChecked()
        calc_fingerprints = self.fingerprint_radio.isChecked() or self.both_radio.isChecked()

        self.thread = CalculationThread(self.file_path, calc_descriptors, calc_fingerprints)
        self.thread.progress_signal.connect(self.update_progress_text)
        self.thread.progress_bar_signal.connect(self.update_progress_bar)
        self.thread.finished_signal.connect(self.calculation_finished)
        self.thread.start()

    def update_progress_text(self, message):
        self.progress_text.append(message)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def calculation_finished(self, output_file):
        QMessageBox.information(self, "Finished", f"Calculation finished. Results saved to '{output_file}'")

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DescriptorApp()
    window.show()
    sys.exit(app.exec())
