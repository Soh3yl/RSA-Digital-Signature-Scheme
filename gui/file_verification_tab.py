import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class FileVerificationTab(QWidget):
    def __init__(self, signature_handler):
        super().__init__()
        self.signature_handler = signature_handler
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        file_layout = QHBoxLayout()
        self.file_label = QLabel("File to Verify:")
        self.file_input = QLineEdit()
        self.file_button = QPushButton("Browse")
        self.file_button.clicked.connect(self.select_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_button)
        layout.addLayout(file_layout)
        
        signature_layout = QHBoxLayout()
        self.signature_label = QLabel("Signature File:")
        self.signature_input = QLineEdit()
        self.signature_button = QPushButton("Browse")
        self.signature_button.clicked.connect(self.select_signature)
        
        signature_layout.addWidget(self.signature_label)
        signature_layout.addWidget(self.signature_input)
        signature_layout.addWidget(self.signature_button)
        layout.addLayout(signature_layout)
        
        key_layout = QHBoxLayout()
        self.key_label = QLabel("Public Key:")
        self.key_input = QLineEdit()
        self.key_button = QPushButton("Browse")
        self.key_button.clicked.connect(self.select_public_key)
        
        key_layout.addWidget(self.key_label)
        key_layout.addWidget(self.key_input)
        key_layout.addWidget(self.key_button)
        layout.addLayout(key_layout)
        
        self.verify_button = QPushButton("Verify Signature")
        self.verify_button.clicked.connect(self.verify_signature)
        layout.addWidget(self.verify_button)
        
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        self.setStyleSheet("""
            QLabel { font-weight: bold; }
            QLineEdit { padding: 5px; }
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Verify")
        if file_path:
            self.file_input.setText(file_path)
    
    def select_signature(self):
        signature_path, _ = QFileDialog.getOpenFileName(self, "Select Signature File", 
                                                        filter="Signature Files (*.sig)")
        if signature_path:
            self.signature_input.setText(signature_path)
    
    def select_public_key(self):
        key_path, _ = QFileDialog.getOpenFileName(self, "Select Public Key", 
                                                  filter="PEM Files (*.pem)")
        if key_path:
            self.key_input.setText(key_path)
    
    def verify_signature(self):
        try:
            file_path = self.file_input.text()
            signature_path = self.signature_input.text()
            public_key_path = self.key_input.text()
            
            if not all([file_path, signature_path, public_key_path]):
                raise ValueError("Please fill in all fields")
            
            is_valid = self.signature_handler.verify_signature(
                file_path, 
                signature_path, 
                public_key_path
            )
            
            if is_valid:
                self.result_label.setText("Signature Verified Successfully!")
                self.result_label.setStyleSheet("color: green;")
            else:
                self.result_label.setText("Signature Verification Failed!")
                self.result_label.setStyleSheet("color: red;")
        
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            self.result_label.setStyleSheet("color: red;")
