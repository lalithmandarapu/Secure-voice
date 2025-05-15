function startVoiceRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onresult = function (event) {
        const text = event.results[0][0].transcript;
        document.getElementById('inputText').value = text;
    };

    recognition.onerror = function (event) {
        alert('Speech recognition error: ' + event.error);
    };

    recognition.start();
}
function startGestureRecognition() {
    const video = document.getElementById('gestureVideo');
    video.classList.remove('d-none');
    navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        video.srcObject = stream;
    });

    setTimeout(() => {
        document.getElementById('inputText').value = 'Hello from ASL!';
        alert('Gesture recognized: Hello from ASL!');
    }, 4000);
}

function encryptText() {
    const message = document.getElementById('inputText').value;
    fetch('/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('encryptedText').value = data.encrypted;
    });
}

function decryptText() {
    const encrypted = document.getElementById('encryptedText').value;
    fetch('/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ encrypted: encrypted })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('decryptedText').value = data.decrypted;
        speak(data.decrypted);
    });
}

function speak(text) {
    const utter = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utter);
}
