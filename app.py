import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

recognized_letter = ""
input_sequence = []

# Updated gesture recognition using landmark distances and basic angle logic
def detect_letter_from_landmarks(landmarks):
    thumb_tip = np.array([landmarks[4].x, landmarks[4].y])
    index_tip = np.array([landmarks[8].x, landmarks[8].y])
    middle_tip = np.array([landmarks[12].x, landmarks[12].y])
    ring_tip = np.array([landmarks[16].x, landmarks[16].y])
    pinky_tip = np.array([landmarks[20].x, landmarks[20].y])

    index_folded = landmarks[8].y > landmarks[6].y
    middle_folded = landmarks[12].y > landmarks[10].y
    ring_folded = landmarks[16].y > landmarks[14].y
    pinky_folded = landmarks[20].y > landmarks[18].y
    thumb_folded = landmarks[4].x > landmarks[3].x

    if not index_folded and middle_folded and ring_folded and pinky_folded:
        return "L"
    elif not index_folded and not middle_folded and not ring_folded and not pinky_folded:
        return "A"
    elif not index_folded and middle_folded and ring_folded and pinky_folded:
        return "I"
    elif not thumb_folded and not index_folded and not middle_folded and not ring_folded and not pinky_folded:
        return "O"
    elif index_folded and middle_folded and ring_folded and pinky_folded:
        return "T"
    elif not thumb_folded and index_folded and middle_folded and ring_folded and pinky_folded:
        return "H"
    elif not index_folded and not middle_folded and ring_folded and pinky_folded:
        return "V"
    else:
        return ""

def capture_gesture():
    global recognized_letter
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Webcam not accessible")
        recognized_letter = "Error"
        return

    start_time = time.time()
    timeout = 10

    while time.time() - start_time < timeout:
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                recognized_letter = detect_letter_from_landmarks(hand_landmarks.landmark)
                if recognized_letter:
                    break

        if recognized_letter:
            cv2.putText(image, f'Letter: {recognized_letter}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Gesture Detection', image)
        if cv2.waitKey(5) & 0xFF == 27 or recognized_letter:
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gesture', methods=['POST'])
def gesture():
    global recognized_letter, input_sequence
    recognized_letter = ""
    thread = threading.Thread(target=capture_gesture)
    thread.start()
    thread.join()

    if recognized_letter:
        input_sequence.append(recognized_letter)

    return jsonify({
        'letter': recognized_letter,
        'input': ''.join(input_sequence)
    })

@app.route('/reset_input', methods=['POST'])
def reset_input():
    global input_sequence
    input_sequence = []
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True)
