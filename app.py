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

# Gesture recognition for V, I, O, L, A, T, H (demo purpose)
def detect_letter_from_landmarks(landmarks):
    fingers_up = []

    fingers_up.append(landmarks[4].x < landmarks[3].x)      # Thumb
    fingers_up.append(landmarks[8].y < landmarks[6].y)      # Index
    fingers_up.append(landmarks[12].y < landmarks[10].y)    # Middle
    fingers_up.append(landmarks[16].y < landmarks[14].y)    # Ring
    fingers_up.append(landmarks[20].y < landmarks[18].y)    # Pinky

    if fingers_up == [False, True, True, False, False]:
        return "V"
    elif fingers_up == [False, True, False, False, False]:
        return "I"
    elif fingers_up == [True, True, True, True, True]:
        return "O"
    elif fingers_up == [False, True, False, True, True]:
        return "L"
    elif fingers_up == [False, True, True, True, True]:
        return "A"
    elif fingers_up == [False, False, False, False, False]:
        return "T"
    elif fingers_up == [True, True, False, False, False]:
        return "H"
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
    local_recognized_letter = ""

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
                current_letter = detect_letter_from_landmarks(hand_landmarks.landmark)
                if current_letter and current_letter != local_recognized_letter:
                    local_recognized_letter = current_letter
                    recognized_letter = local_recognized_letter
                    break

        if local_recognized_letter:
            cv2.putText(image, f'Letter: {local_recognized_letter}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Gesture Detection', image)
        if cv2.waitKey(5) & 0xFF == 27 or local_recognized_letter:
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
