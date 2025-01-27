from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QMessageBox, QTabWidget)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui.key_generation_tab import KeyGenerationTab
from gui.file_signing_tab import FileSigningTab
from gui.file_verification_tab import FileVerificationTab
from RSA_Digital_Signature.RSADigitalSignature import RSADigitalSignature

class RSASignatureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSA Digital Signature Tool")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        self.signature_handler = RSADigitalSignature()
        
        self.key_generation_tab = KeyGenerationTab(self.signature_handler)
        self.file_signing_tab = FileSigningTab(self.signature_handler)
        self.file_verification_tab = FileVerificationTab(self.signature_handler)
        
        self.tab_widget.addTab(self.key_generation_tab, "Key Generation")
        self.tab_widget.addTab(self.file_signing_tab, "File Signing")
        self.tab_widget.addTab(self.file_verification_tab, "File Verification")
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #C0C0C0;
                background: white;
            }
            QTabBar::tab {
                background: #E0E0E0;
                color: black;
                padding: 10px;
                border: 1px solid #C0C0C0;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: white;
                color: #2C3E50;
                border-bottom: 2px solid #3498DB;
            }
        """)