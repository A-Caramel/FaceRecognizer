from imutils import paths
import face_recognition
import pickle
import cv2
import os
import time
import glob
import math

########################################################################################################################

# FPS display #
start_time = time.time()
display_time = 2
fc = 0
FPS = 0

########################################################################################################################

# Encoding of faces #
# Grab picture from their respective directory in the faces folder
imagePaths = list(paths.list_images('faces'))
knownEncodings = []
knownNames = []


# Training
for (i, imagePath) in enumerate(imagePaths):
    # Extract person name from their folders in faces
    name = imagePath.split(os.path.sep)[-2]
    # Convert image to BGR (OpenCV ordering) to dlib RGB
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Use Face_recognition to locate faces
    boxes = face_recognition.face_locations(rgb, model='hog')
    # Eigenface quantification
    encodings = face_recognition.face_encodings(rgb, boxes)
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)
# Save encodings
data = {"encodings": knownEncodings, "names": knownNames}
# Pickle saves data into a file for later use
f = open("face_enc", "wb")
f.write(pickle.dumps(data))
f.close()
# Find path for xml file containing haarcascade file
cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPathface)
data = pickle.loads(open('face_enc', "rb").read())

########################################################################################################################

# Webcam face detection #
print("Streaming started")
video_capture = cv2.VideoCapture(0)
focus = 0  # min: 0, max: 255, increment:5
video_capture.set(28, focus)

# loop over frames from the video file stream
while True:
    # Frame grab of webcam video
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60), flags=cv2.CASCADE_SCALE_IMAGE)

    # BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb)
    names = []
    for encoding in encodings:
        # Compare encodings with encodings in data["encodings"]
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            # Find feature vector of faces that match between the webcam and database
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        names.append(name)
        for ((x, y, w, h), name) in zip(faces, names):
            # Rescale the face coordinates
            # Draw the predicted face name on the image
            # Color is in BGR - Look up a table
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Initialize FPS counter
    fc += 1
    TIME = time.time() - start_time
    if (TIME) >= display_time:
        FPS = fc / (TIME)
        fc = 0
        start_time = time.time()
    fps_disp = "FPS: " + str(FPS)[:5]
    image = cv2.putText(frame, fps_disp, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Window
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

a = input('Press "Enter" to exit')