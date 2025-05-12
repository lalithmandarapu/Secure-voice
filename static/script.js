let recognition;
const webcam = document.getElementById('webcam');

function startInput() {
  const mode = document.getElementById('inputMode').value;
  if (mode === 'voice') startVoiceInput();
  else startGestureInput();
}

function startVoiceInput() {
  const lang = document.getElementById('language').value;
  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = lang;
  recognition.onresult = e => {
    document.getElementById('inputText').value = e.results[0][0].transcript;
  };
  recognition.start();
}

function speakText(text) {
  const lang = document.getElementById('language').value;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;
  speechSynthesis.speak(utterance);
}

async function startGestureInput() {
  webcam.style.display = "block";

  const hands = new Hands({ locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}` });
  hands.setOptions({ maxNumHands: 1, modelComplexity: 1 });

  hands.onResults(results => {
    if (results.multiHandLandmarks.length > 0) {
      document.getElementById('inputText').value = "Gesture Detected: ✋"; // Placeholder
    }
  });

  const camera = new Camera(webcam, {
    onFrame: async () => await hands.send({ image: webcam }),
    width: 320,
    height: 240
  });

  camera.start();
}
