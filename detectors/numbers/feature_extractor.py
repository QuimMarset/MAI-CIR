import mediapipe as mp
import numpy as np
import cv2
mp_hands = mp.solutions.hands



class HandLandmarksExtractor:

    def __init__(self):
        self.create_landmark_extractor()
        self.create_joints_angle_list()


    def create_landmark_extractor(self):
        self.hand_extractor = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2
        )

    
    def create_joints_angle_list(self):
        self.joints_list = [
            [4, 3, 2], # thumb
            [8, 7, 6], # index
            [12, 11, 10], # middle
            [16, 15, 14], # ring
            [20, 19, 18] # pinky
        ]

    
    def extract_train_features(self, images_paths, all_labels):
        features = []
        labels = []
        
        for image_path, label in zip(images_paths, all_labels):
            image = self.preprocess_image(image_path)
            image_features = self.extract_image_features(image)
            if len(image_features) > 0:
                # Train/val images only have one hand
                features.append(image_features[0])
                labels.append(label)

        return np.array(features), np.array(labels)


    def extract_test_features(self, image_path):
        image = self.preprocess_image(image_path)
        features = self.extract_image_features(image)
        return np.array(features)

        
    def extract_video_features(self, video_path):
        features = []

        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_features = self.extract_image_features(image)
            if len(image_features) > 0:
                features.extend(image_features)
        
        cap.release()
        return np.array(features)


    def extract_image_features(self, image):
        features = []
        image = cv2.flip(image, flipCode=1)
        results = self.hand_extractor.process(image)

        if results.multi_handedness:
            # At least one hand has been detected
            hands_landmarks = results.multi_hand_landmarks
            
            for hand_landmarks in hands_landmarks:
                hand_landmarks = hand_landmarks.landmark
                processed_landmarks = self.process_landmarks(hand_landmarks)
                finger_angles = self.compute_finger_angles(hand_landmarks)
                hand_features = [*processed_landmarks, *finger_angles]
                features.append(hand_features)

        return features
    

    def preprocess_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image


    def process_landmarks(self, landmarks):
        processed_landmarks = [
            [landmark.x, landmark.y]
            for landmark in landmarks
        ]
        return np.array(processed_landmarks).flatten()


    def compute_finger_angles(self, landmarks):
        finger_angles = []
        
        for joint in self.joints_list:
            a = np.array([landmarks[joint[0]].x, landmarks[joint[0]].y]) # First coord
            b = np.array([landmarks[joint[1]].x, landmarks[joint[1]].y]) # Second coord
            c = np.array([landmarks[joint[2]].x, landmarks[joint[2]].y]) # Third coord
            
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians*180.0/np.pi)
            if angle > 180:
                angle = 360 - angle
            finger_angles.append(angle)

        return finger_angles