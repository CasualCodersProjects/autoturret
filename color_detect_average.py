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
                red_value = np.mean(
                    frame[y:y + chunk_height, x:x + chunk_width, 2])
                pixel_groups.append(red_value)

        print(pixel_groups)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
