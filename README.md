# RSA Digital Signature Tool
## Overview
This is a comprehensive PyQt5-based GUI application for RSA Digital Signature operations, including key generation, file signing, and signature verification.
## Features
•	Generate RSA Key Pairs
•	Sign Files with Private Key
•	Verify File Signatures with Public Key
## Prerequisites
•	Python 3.8+
## Install dependencies: 
pip install -r requirements.txt
## Running the Application
python main.py
## Usage
## 1.	Key Generation Tab: 
-Generate RSA key pairs

-Specify key size and storage path

-Save public and private keys

## 2.	File Signing Tab: 
-Select file to sign

-Choose private key

-Specify signature empty file

-Sign the file

## 3.	File Verification Tab: 
-Select signed file

-Choose signature file

-Select corresponding public key

-Verify signature

## 4.	You can also use the app without GUI. (check out “test” folder)
## Security Notes
-Keep private keys confidential

-Use strong key sizes (recommended: 2048+ bits)

-Verify signatures carefully


