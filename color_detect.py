import cv2
# import imutils
import numpy as np


def main():

    video_capture = cv2.VideoCapture(0)
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))

    print("Video width: ", video_width)
    print("Video height: ", video_height)

    while True:
        _, frame = video_capture.read()

        most_red = (0, 0, 0)

        reds = []

        reds = np.argwhere(cv2.inRange(frame, (0, 0, 175), (50, 50, 255)))

        for px, py in reds:
            red_value = frame[px, py, 0]
            red = (red_value, py, px)
            if red[0] > most_red[0]:
                most_red = red

        if most_red != (0, 0, 0):
            cv2.circle(frame, (most_red[1], most_red[2]), 10, (0, 0, 255), -1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
