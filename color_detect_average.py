import cv2
import numpy as np


def main():

    video_capture = cv2.VideoCapture(0)
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))

    print("Video width: ", video_width)
    print("Video height: ", video_height)

    while True:
        _, frame = video_capture.read()

        # chunk into 4x4 groups of pixels
        # and find the average red value
        # of each group

        group = 4
        chunk_width = video_width // group
        chunk_height = video_height // group

        pixel_groups = []

        for x in range(0, video_width, chunk_width):
            for y in range(0, video_height, chunk_height):

                avg_red_value = np.mean(
                    frame[y:y + chunk_height, x:x + chunk_width, 2])
                avg_green_value = np.mean(
                    frame[y:y + chunk_height, x:x + chunk_width, 1])
                avg_blue_value = np.mean(
                    frame[y:y + chunk_height, x:x + chunk_width, 0])

                if avg_blue_value < 128 and avg_green_value < 128:
                    pixel_groups.append((avg_red_value, y, x))

                # pixel_groups.append((avg_red_value, y, x))

        # print(pixel_groups)

        most_red = (0, 0, 0)

        for hue, py, px in pixel_groups:
            red = (hue, py, px)
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
