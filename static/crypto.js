const key = CryptoJS.enc.Utf8.parse('1234567812345678');
const iv = CryptoJS.enc.Utf8.parse('1234567812345678');

function encryptMessage() {
  const input = document.getElementById('inputText').value;
  const encrypted = CryptoJS.AES.encrypt(input, key, { iv: iv }).toString();
  document.getElementById('encryptedText').value = encrypted;
}

function decryptMessage() {
  const encrypted = document.getElementById('encryptedText').value;
  const decrypted = CryptoJS.AES.decrypt(encrypted, key, { iv: iv }).toString(CryptoJS.enc.Utf8);
  document.getElementById('decryptedText').value = decrypted;
  speakText(decrypted);
}
