import cv2
# import imutils
import numpy as np


def main():

    rect_width = 50
    rect_height = 50

    frame_counter = 0
    frame_counter_max = 10

    video_capture = cv2.VideoCapture(0)
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))

    print("Video width: ", video_width)
    print("Video height: ", video_height)

    while True:
        _, frame = video_capture.read()

        most_red = (0, 0, 0)

        reds = []

        reds = np.argwhere(cv2.inRange(frame, (0, 0, 125), (50, 50, 255)))

        # for px, py in reds:
        #     red_value = frame[px, py, 0]
        #     red = (red_value, py, px)
        #     if red[0] > most_red[0]:
        #         most_red = red

        xs = []
        ys = []

        for px, py in reds:
            xs.append(px)
            ys.append(py)

        if len(xs) > 0 and len(ys) > 0:
            avg_x = np.mean(xs)
            avg_y = np.mean(ys)

            if avg_x > 0 and avg_y > 0:
                most_red = (0, int(avg_y), int(avg_x))

        if most_red != (0, 0, 0):
            # cv2.circle(frame, (most_red[1], most_red[2]), 10, (0, 0, 255), -1)
            cv2.rectangle(frame, (most_red[1] - rect_width // 2, most_red[2] - rect_height // 2),
                          (most_red[1] + rect_width // 2, most_red[2] + rect_height // 2), (0, 0, 255), 2)
            cv2.putText(frame, "Hostile Detected",
                        (most_red[1] - 5 - rect_width // 2, most_red[2] - 15 - rect_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
