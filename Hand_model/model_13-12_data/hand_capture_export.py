import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import csv


mp_drawing = mp.solutions.drawing_utils				#draw line
mp_hands = mp.solutions.hands						#import hand model

class_name = "U"

image_folder_path = 'extra'  # Thay đổi đường dẫn đến thư mục chứa hình ảnh của bạn

image_files = os.listdir(image_folder_path)
image_files = [os.path.join(image_folder_path, file) for file in image_files if file.endswith(('png', 'jpg', 'jpeg'))]

with mp_hands.Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as hands:

	for image_path in image_files:
		frame = cv2.imread(image_path)

		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image.flags.writeable = False
		results = hands.process(image)
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

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


			#append class name
			landmarks_row.insert(0, class_name)
			with open('model_13-12.csv', mode = 'a', newline = '') as f:
				csv_writer = csv.writer(f, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
				csv_writer.writerow(landmarks_row)
			
		except:
			pass





		cv2.imshow('Raw Webcam Feed', image)

		if cv2.waitKey(10) & 0xFF == ord('q'):
			break

cv2.destroyAllWindows()