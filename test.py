import time
import os
import cv2
import numpy as np

while True:
    a = input('\nCommands: Check database - "0"\nCreate new directory in database - "1"\nAdd images to directories existing in databases - "2"\n\n\nEnter command: ')
    if a == '0':
        path = "A:/Projects/FaceRecognition/faces"
        path = os.path.realpath(path)
        os.startfile(path)
    elif a == '1':
        while True:
            try: # Use try so that the program doesn't just exit on error
                # Directory
                directory = input('\nEnter name of person to add in the database: ')
                # Parent Directory
                parent_dir = "/Projects/FaceRecognition/faces"
                # Path
                path = os.path.join(parent_dir, directory)
                os.mkdir(path)
                print('%s has been created.\n' %directory)
                b = input("Continue? ")
                if b == 'No' or b == 'no':
                    time.sleep(2)
                    break
            except FileExistsError:
                print('%s already exists!\n' %directory)
                c = input("Try again? ")
                if c == 'Yes' or c == 'yes':
                    time.sleep(2)
                    break
    elif a == '2':
        print('\n\nStreaming started\nTo add an image to an existing folder in the database, press Q\nTo EXIT, press the ESCAPE key')
        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            # Frame grab of webcam video
            ret, frame = video_capture.read()
            cv2.imshow("Webcam", frame)
            focus = 0  # min: 0, max: 255, increment:5
            video_capture.set(28, focus)
            d = cv2.waitKey(1)
            # 81 is the ASCII key for Q and 113 for q
            if d == 81 or d == 113:
                vidcap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                vidcap.read()
                success, image = vidcap.read()
                success = True
                while success:
                    e = input('\n\nName of person in the image: ')
                    f = input('Entry Number: ')
                    g = (e, f)
                    h = input('\n\nName of folder to save to in the database: ')
                    path = '/Projects/FaceRecognition/faces/{}'.format(h)
                    # Save image as jpg with custom name
                    cv2.imwrite(os.path.join(path ,"{}_{}.jpg".format(*g)), image)
                    print('{}_{}.jpg'.format(*g), 'has been saved to %s' %h, '\n\nTo add a new image to an existing folder in the database, press Q\nTo EXIT, press the ESCAPE key')
                    break
            # 27 is the ASCII key for escape
            if d == 27:
                    break
        video_capture.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    else:
        print('\nInput not recognized! Try Again.\n')
        time.sleep(2)