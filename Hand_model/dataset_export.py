import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import csv
import time

pTime = 0
cTime = 0

mp_drawing = mp.solutions.drawing_utils				#draw line
mp_hands = mp.solutions.hands						#import hand model

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

	while cap.isOpened():
		ret, frame = cap.read()

		#recolor feed
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		#set flag
		image.flags.writeable = False

		#Dectection
		results = hands.process(image)
		#print(results)


		#set flag to true
		image.flags.writeable = True

		#recolor image back to BGR for rendering (opencv love BGR)
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		x = 0
		y = 0
		w = 350
		h = 350
		# Crop ảnh
		cropped_image = image[y:y+h, x:x+w]
		cv2.imshow('Dectec area', cropped_image)

		if cv2.waitKey(1) & 0xFF == ord('e'):
			cv2.imwrite(os.path.join('Y', '{}.jpg'.format(uuid.uuid1())), image)


		# Rendering results
		if results.multi_hand_landmarks:
			for num, hand in enumerate(results.multi_hand_landmarks):
				mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
										  mp_drawing.DrawingSpec(color = (72, 40, 200), thickness = -1, circle_radius = 3),
										  mp_drawing.DrawingSpec(color = (72, 40, 200), thickness = 2, circle_radius = 4))




		cv2.imshow('Raw Webcam Feed', image)

		if cv2.waitKey(10) & 0xFF == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()