import sys
import os
import subprocess
import cv2
import numpy as np
import datetime

# Load the Haar Cascade classifiers (ensure the xml files are in the same directory)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

if face_cascade.empty():
    raise IOError('Unable to load the face cascade XML file.')
if eye_cascade.empty():
    raise IOError('Unable to load the eye cascade XML file.')

def open_ebook(path):
    """Open an ebook file with the default system viewer."""
    if os.name == 'nt':
        os.startfile(path)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', path])
    else:
        subprocess.Popen(['xdg-open', path])

def track_eyes(output_video=None):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Error: Could not open camera.')
        return

    writer = None
    if output_video:
        # Define the codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        writer = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Error: Could not read frame.')
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                eye_center = (x + ex + ew // 2, y + ey + eh // 2)
                cv2.circle(frame, eye_center, 3, (0, 0, 255), -1)
        cv2.imshow('Eye Tracking', frame)
        if writer:
            writer.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ebook_path = 'your_ebook.pdf'  # replace with your ebook file
    open_ebook(ebook_path)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'eye_capture_{timestamp}.avi'
    track_eyes(output_file)
