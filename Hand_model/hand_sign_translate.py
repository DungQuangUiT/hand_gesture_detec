import cv2
import mediapipe as mp						#mp - thu vien mediapipe
import csv
import uuid
import os
import numpy as np
import pandas as pd
import pickle
import time

#load model
with open('model_13-12.pkl', 'rb') as f:
	model = pickle.load(f)

pTime = 0
cTime = 0
tTime = 8

mp_drawing = mp.solutions.drawing_utils				#draw line
mp_hands = mp.solutions.hands						#import hand model


cap = cv2.VideoCapture(0)
image2 = cv2.imread("blank_bg.jpg")

tran_text = []

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

		# Rendering results
		if results.multi_hand_landmarks:
			for num, hand in enumerate(results.multi_hand_landmarks):
				mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
										  mp_drawing.DrawingSpec(color = (72, 40, 200), thickness = -1, circle_radius = 3),
										  mp_drawing.DrawingSpec(color = (72, 40, 200), thickness = 2, circle_radius = 4))


		#export coordinate
		try:
			#extract hand landmarks
			all_hands_landmarks = []
			for num, hand in enumerate(results.multi_hand_landmarks):
				all_hands_landmarks.append(hand.landmark)

			Hands = all_hands_landmarks
			# Lặp qua tất cả các landmarks trong biến "Hands" và thu thập thông tin
			landmarks_data = []
			for hand_landmarks in Hands:
			    for landmark in hand_landmarks:
			        x = landmark.x
			        y = landmark.y
			        z = landmark.z
			        landmarks_data.append([x, y, z])

			# Chuyển danh sách các landmarks thành một danh sách phẳng
			landmarks_row = list(np.array(landmarks_data).flatten())


			#make detection
			X = pd.DataFrame([landmarks_row])
			body_language_class = model.predict(X)[0]
			body_language_prob = model.predict_proba(X)[0]
			print(body_language_class, body_language_prob)

			#get status box
			cv2.rectangle(image, (0, 0), (250, 60), (73, 38, 187), -1)
			#display class
			cv2.putText(image, 'CLASS',
						  (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (45, 30, 30), 1, cv2.LINE_AA)
			cv2.putText(image, body_language_class.split(' ')[0],
						(90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 240, 230), 2, cv2.LINE_AA)
			#display probability
			cv2.putText(image, 'PROB',
						  (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (45, 30, 30), 1, cv2.LINE_AA)
			cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2)),
						(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 240, 230), 2, cv2.LINE_AA)


		except:
			pass

		#hiển thị text translated from hand sign
		cTime = time.time()
		if (cTime - tTime >= 4) and (round(body_language_prob[np.argmax(body_language_prob)], 2) > 0.8):
			tran_text.append(body_language_class)
			tran_text_final = list(np.array(tran_text).flatten())
			tran_text_final = str(tran_text_final).replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(" ", "")
			cv2.putText(image2, str(tran_text_final),
						  (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (45, 30, 30), 1, cv2.LINE_AA)
			tTime = cTime


		cTime = time.time()
		fps = 1/(cTime - pTime)
		pTime = cTime
		cv2.rectangle(image, (0, 435), (50, 490), (73, 38, 187), -1)
		cv2.putText(image, str(int(fps)), (4, 468), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 240, 230), 2, cv2.LINE_AA)


		cv2.imshow("Image", image2)
		cv2.imshow('Raw Webcam Feed', image)


		if cv2.waitKey(10) & 0xFF == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()