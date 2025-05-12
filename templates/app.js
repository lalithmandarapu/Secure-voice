let recognition;
const inputText = document.getElementById('inputText');
const webcam = document.getElementById('webcam');

async function startInput() {
  const mode = document.getElementById('inputMode').value;
  if (mode === 'voice') {
    startVoiceInput();
  } else {
    startGestureInput();
  }
}

// Voice Input
function startVoiceInput() {
  const lang = document.getElementById('language').value;
  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = lang;
  recognition.onresult = e => {
    inputText.value = e.results[0][0].transcript;
  };
  recognition.start();
}

// TTS Output
function speakText(text) {
  const lang = document.getElementById('language').value;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;
  speechSynthesis.speak(utterance);
}

// Gesture Input with MediaPipe
async function startGestureInput() {
  webcam.style.display = "block";

  const hands = new Hands({ locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}` });
  hands.setOptions({ maxNumHands: 1, modelComplexity: 1 });

  hands.onResults(results => {
    if (results.multiHandLandmarks.length > 0) {
      inputText.value = "Detected Gesture: Thumbs Up"; // Replace with actual classifier
    }
  });

  const camera = new Camera(webcam, {
    onFrame: async () => await hands.send({ image: webcam }),
    width: 320,
    height: 240
  });

  camera.start();
}
