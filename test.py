# https://github.com/skaws2003/Dlib-lip-detection/tree/master
import tensorflow as tf
import cv2
import dlib
from typing import List
from matplotlib import pyplot as plt

def load_video(path:str) -> List[float]: 
    hog_face_detector = dlib.get_frontal_face_detector()
    dlib_facelandmark = dlib.shape_predictor("./detector/shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(path)
    frames = []
    for _ in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))): 
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = hog_face_detector(frame)

        for face in faces:
            face_landmarks = dlib_facelandmark(frame, face)
            # for n in range(0, 68):
            #     x = face_landmarks.part(n).x
            #     y = face_landmarks.part(n).y
            #     cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
            x67 = face_landmarks.part(67).x
            y67 = face_landmarks.part(67).y
            horizontal_padding = 40
            vertical_padding = 30
            lip_window = frame[y67-vertical_padding:y67+vertical_padding, x67-horizontal_padding:x67+horizontal_padding]
            lip_window = tf.expand_dims(lip_window, axis=-1)
            
        frames.append(lip_window)
    cap.release()
    return frames
    mean = tf.math.reduce_mean(frames)
    std = tf.math.reduce_std(tf.cast(frames, tf.float32))
    return tf.cast((frames - mean), tf.float32) / std


test_path = './output_clips/clip30.mp4'
frm = load_video(test_path)

plt.imshow(frm[20])
plt.show()