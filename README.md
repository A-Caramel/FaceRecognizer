# FaceRecognizer
# by Alfredo Benavides

Includes 2 scripts: FaceRecognizer utilizing FaceCascades with SVM and user customizable database

"main.py" utilizes SVM and FaceCascades to recognize and classify faces. Furthermore, the program labels and boxes recognized faces on the video feed based on existing directories of people in the database. Faces not in the database will be recognized but will be labeled as "Unknown" on the video feed.

"test.py" allows users to check the current directories in the database, manually create folders in the database, and add images to those manually created folders.

There is future plans to develop a mobile/windows application that can run both scripts simultaneously for ease of use.
