import cv2
import face_recognition
import os
import pickle

path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

with open('classnames.dat', 'wb') as f:
    pickle.dump(classNames, f)

def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
        except IndexError as e:
            print()
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(encodeListKnown, f)

print('Encoding Complete')