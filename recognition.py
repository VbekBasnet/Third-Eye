import face_recognition
import os, sys
import cv2
import numpy as np
import math
import time
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from djitellopy import tello
import KeyPressModule as kp


kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

global frame
me.streamon()



def getKeyboardInput():
    lr, fb, ud, yv = 0,0,0,0
    speed = 50
    rotate = 100

    if kp.getKey("a"): lr= -speed
    elif kp.getKey("d"): lr= speed

    if kp.getKey("w"): fb = speed
    if kp.getKey("s"): fb = -speed

    if kp.getKey("UP"): ud= speed
    elif kp.getKey("DOWN"): ud= -speed

    if kp.getKey("LEFT"): yv = -rotate
    if kp.getKey("RIGHT"): yv = rotate

    if kp.getKey("SPACE"): me.takeoff()
    if kp.getKey("v"):  me.land(); time.sleep([2])

    if kp.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', frame)
        time.sleep(0.2)



    return [lr,fb,ud,yv]



def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        pTime = 0
        num = 0
        num = num+1
        #detector = FaceMeshDetector(maxFaces=2)




        while True:
            frame = me.get_frame_read().frame

            # Face Mesh
            # frame, faces = detector.findFaceMesh(frame, False)
            #
            # if faces:
            #     face = faces[0]
            #     pointLeft = face[145]
            #     pointRight = face[374]
            #
            #     #Drawing line
            #    # cv2.line(frame, pointLeft, pointRight, (0, 200, 0), 3)
            #     #cv2.circle(frame,pointLeft, 5, (255, 0, 255), cv2.FILLED)
            #     #cv2.circle(frame, pointRight, 5, (255, 0, 255), cv2.FILLED)
            #     w,_= detector.findDistance(pointLeft,pointRight)
            #
            #     #finding Focal length
            #     W = 6.3
            #     #d = 50
            #     #f = (w*d)/W
            #     #print(f)
            #
            #     #finding distance
            #     f = 840
            #     d=(W*f)/w
            #     print(d)
            #
            #     cvzone.putTextRect(frame,f'Distance: {int(d)}cm',
            #                        (face[10][0]-75,face[10][1]-50),
            #                        scale=2)

            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_RGB2BGR)

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                # Creating FPS
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                            3, (0, 255, 0), 2)

                cv2.putText(frame,'Face'+str(num),(left -30, bottom +30),cv2.FONT_HERSHEY_PLAIN,
                            3, (0, 255, 0), 2)

            vals = getKeyboardInput()
            me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
            cv2.imshow('Face Recognition', frame)


            if cv2.waitKey(30) == ord('q'):
                break


        me.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
