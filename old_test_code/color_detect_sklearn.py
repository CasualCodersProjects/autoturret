import cv2
from sklearn.cluster import AffinityPropagation
import numpy as np


def main():

    video_capture = cv2.VideoCapture(0)
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))

    print("Video width: ", video_width)
    print("Video height: ", video_height)

    while True:
        _, frame = video_capture.read()

        mask = cv2.inRange(frame, (0, 0, 128), (80, 80, 255))

        reds = np.argwhere(mask)

        print(f'There are {len(reds)} red pixels.')

        if len(reds) > 0:
            model = AffinityPropagation(damping=0.9).fit(reds)
            hat = model.predict(reds)
            clusters = np.unique(hat)
            print(f'There are {len(clusters)} clusters.')

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
