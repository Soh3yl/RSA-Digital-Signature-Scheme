import sys
from PyQt5.QtWidgets import QApplication
from gui.rsa_signature_app import RSASignatureApp

def main():
    app = QApplication(sys.argv)
    window = RSASignatureApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()