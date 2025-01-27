import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from cryptography.hazmat.primitives import serialization

class FileSigningTab(QWidget):
    def __init__(self, signature_handler):
        super().__init__()
        self.signature_handler = signature_handler
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # File Selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("File to Sign:")
        self.file_input = QLineEdit()
        self.file_button = QPushButton("Browse")
        self.file_button.clicked.connect(self.select_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_button)
        layout.addLayout(file_layout)
        
        # Private Key Selection
        key_layout = QHBoxLayout()
        self.key_label = QLabel("Private Key:")
        self.key_input = QLineEdit()
        self.key_button = QPushButton("Browse")
        self.key_button.clicked.connect(self.select_private_key)
        
        key_layout.addWidget(self.key_label)
        key_layout.addWidget(self.key_input)
        key_layout.addWidget(self.key_button)
        layout.addLayout(key_layout)
        
        # Signature Path Selection
        signature_layout = QHBoxLayout()
        self.signature_label = QLabel("Signature Path:")
        self.signature_input = QLineEdit()
        self.signature_button = QPushButton("Browse")
        self.signature_button.clicked.connect(self.select_signature_path)
        
        signature_layout.addWidget(self.signature_label)
        signature_layout.addWidget(self.signature_input)
        signature_layout.addWidget(self.signature_button)
        layout.addLayout(signature_layout)
        
        # Sign File Button
        self.sign_button = QPushButton("Sign File")
        self.sign_button.clicked.connect(self.sign_file)
        layout.addWidget(self.sign_button)
        
        # Result Label
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Styling
        self.setStyleSheet("""
            QLabel { font-weight: bold; }
            QLineEdit { padding: 5px; }
            QPushButton {
                background-color: #2ECC71;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Sign")
        if file_path:
            self.file_input.setText(file_path)
    
    def select_private_key(self):
        key_path, _ = QFileDialog.getOpenFileName(self, "Select Private Key", 
                                                  filter="PEM Files (*.pem)")
        if key_path:
            self.key_input.setText(key_path)
    
    def select_signature_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Signature", options=options)
        if directory:
            self.signature_input.setText(directory)
    
    def sign_file(self):
        try:
            file_path = self.file_input.text()
            key_path = self.key_input.text()
            signature_directory = self.signature_input.text()
            
            if not all([file_path, key_path, signature_directory]):
                raise ValueError("Please fill in all fields")
            
            # Load private key
            with open(key_path, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(), 
                    password=None
                )
            
            # Update signature handler's private key
            self.signature_handler.private_key = private_key
            
            # Create signature path
            signature_path = os.path.join(signature_directory, "signature.sig")
            
            # Sign file
            signature = self.signature_handler.sign_file(
                file_path, 
                signature_path
            )
            
            self.result_label.setText(f"File signed successfully!\nSignature saved to: {signature_path}")
            self.result_label.setStyleSheet("color: green;")
        
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            self.result_label.setStyleSheet("color: red;")
