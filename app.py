from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
import base64
import hashlib

app = Flask(__name__)

def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

SECRET_KEY = 'securevoicekey123'

def encrypt(text):
    key = hashlib.sha256(SECRET_KEY.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(text).encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt(encrypted_text):
    key = hashlib.sha256(SECRET_KEY.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_text))
    return decrypted.decode('utf-8').rstrip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    input_text = data.get('text')
    encrypted = encrypt(input_text)
    decrypted = decrypt(encrypted)
    return jsonify({
        'original': input_text,
        'encrypted': encrypted,
        'decrypted': decrypted
    })

if __name__ == '__main__':
    app.run(debug=True)
