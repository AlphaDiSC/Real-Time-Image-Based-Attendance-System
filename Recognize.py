import cv2
import numpy as np
import face_recognition
import pickle
import Functions as fn
import time

cap = cv2.VideoCapture(0)

with open('classnames.dat', 'rb') as f:
    classNames = pickle.load(f)

with open('dataset_faces.dat', 'rb') as f:
    encodeListKnown = pickle.load(f)
enr_prev = 0
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            enr = classNames[matchIndex].upper()
            if enr != enr_prev:
                print('check')
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, enr, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                status = fn.markAttendance(enr)
                cv2.putText(img, status, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                enr_prev = enr
            else:
                status = "Attendance Already Marked."
                cv2.putText(img, status, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                time.sleep(2)
                enr_prev = 0
    fn.update_attendance()

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()