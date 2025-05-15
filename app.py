from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
import base64
import os

app = Flask(__name__)

# Encryption key and padding
key = b'ThisIsASecretKey'
BLOCK_SIZE = AES.block_size
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s)-1:])]

def encrypt(raw):
    raw = pad(raw)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = base64.b64encode(cipher.encrypt(raw.encode()))
    return encrypted.decode()

def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(enc).decode())
    return decrypted

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    data = request.json
    message = data['message']
    encrypted = encrypt(message)
    return jsonify({'encrypted': encrypted})

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.json
    encrypted = data['encrypted']
    decrypted = decrypt(encrypted)
    return jsonify({'decrypted': decrypted})

if __name__ == '__main__':
    app.run(debug=True)
