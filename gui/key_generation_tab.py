import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class KeyGenerationTab(QWidget):
    def __init__(self, signature_handler):
        super().__init__()
        self.signature_handler = signature_handler
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Key Size Selection
        key_size_layout = QHBoxLayout()
        self.key_size_label = QLabel("Key Size:")
        self.key_size_input = QLineEdit()
        self.key_size_input.setPlaceholderText("Default: 2048")
        key_size_layout.addWidget(self.key_size_label)
        key_size_layout.addWidget(self.key_size_input)
        layout.addLayout(key_size_layout)
        
        # Key Path Selection
        key_path_layout = QHBoxLayout()
        self.key_path_label = QLabel("Key Storage Path:")
        self.key_path_input = QLineEdit()
        self.key_path_input.setPlaceholderText("Default: ./")
        self.key_path_button = QPushButton("Browse")
        self.key_path_button.clicked.connect(self.select_key_path)
        
        key_path_layout.addWidget(self.key_path_label)
        key_path_layout.addWidget(self.key_path_input)
        key_path_layout.addWidget(self.key_path_button)
        layout.addLayout(key_path_layout)
        
        # Generate Key Button
        self.generate_key_button = QPushButton("Generate Key Pair")
        self.generate_key_button.clicked.connect(self.generate_key_pair)
        layout.addWidget(self.generate_key_button)
        
        # Result Label
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Styling
        self.setStyleSheet("""
            QLabel { font-weight: bold; }
            QLineEdit { padding: 5px; }
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
    
    def select_key_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Key Storage Directory")
        if path:
            self.key_path_input.setText(path)
    
    def generate_key_pair(self):
        try:
            key_size = int(self.key_size_input.text()) if self.key_size_input.text() else 2048
            
            key_path = self.key_path_input.text() or './'
            
            private_key_path, public_key_path = self.signature_handler.generate_key_pair(
                key_path=key_path
            )
            
            self.result_label.setText(f"Keys generated successfully!\n"
                                      f"Private Key: {private_key_path}\n"
                                      f"Public Key: {public_key_path}")
            self.result_label.setStyleSheet("color: green;")
        
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            self.result_label.setStyleSheet("color: red;")