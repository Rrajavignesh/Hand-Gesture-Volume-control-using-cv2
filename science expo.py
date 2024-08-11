import cv2 #image processing
import mediapipe as mp #hand tracking
import pyautogui #keybord simulation

x1 = y1 = x2 = y2 = 0 #two specific landmark
webcam = cv2.VideoCapture(0) #webcam using open cv
my_hands = mp.solutions.hands.Hands() #initilize the mediapipe hands module
drawing_utils = mp.solutions.drawing_utils #drawing landmark using mediapipe

while True:
    _, image = webcam.read()    #continuously capture frames from the webcam
    image = cv2.flip(image, 1)
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8: #identifi the thumb finger
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4: #identifi the index finger
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
            if dist > 50:
                pyautogui.press("volumeup")
            else:
                pyautogui.press("volumedown")

    cv2.imshow("Hand volume control using python", image)
    key = cv2.waitKey(1)
    if key == 27: #27 represant exit key to exit
        break

webcam.release()
cv2.destroyAllWindows()
