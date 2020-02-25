import cv2
import logging as log
from time import sleep

from utils import average_squares


class FindHand:
    
    def __init__(self):
        cascPath = "cascade_1.xml"
        self.handCascade = cv2.CascadeClassifier(cascPath)
        log.basicConfig(filename='webcam.log', level=log.INFO)

        self.video_capture = cv2.VideoCapture(0)
        self.anterior = 0
        self.first_frame = None
    
    def get_hand_location(self):
        if not self.video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass

        # Capture frame-by-frame
        ret, frame = self.video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.first_frame is None:
            self.first_frame = gray
        new_frame = cv2.absdiff(self.first_frame, gray)
        self.first_frame = gray

        hands = self.handCascade.detectMultiScale(
            new_frame,
            1.2,
            13
        )

        # Find hand with most area
        hands = average_squares(hands)
        if len(hands) > 0:
            largest_area_index = (hands[:,2] * hands[:,3]).argmax()
            hand = hands[largest_area_index]

            # Draw a rectangle around the hands
            x, y, w, h = hand
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Normalize the values of hand
            hand = hand / (new_frame.shape + new_frame.shape)  # Add tuples to combine them
            mx = hand[0] + hand[2] / 2
            my = hand[1] + hand[3] / 2
            #cv2.imshow('Video', frame)
            return mx, my

        # Display the resulting frame
        #cv2.imshow('Video', frame)

        return None

    def __del__(self):
        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()
