import platform

import cv2

from detect import detect_hostiles

THRESHOLD = 50


def draw_hostile_box(frame, target, radius):
    cv2.rectangle(frame, (target[0] - radius // 2, target[1] - radius // 2),
                  (target[0] + radius // 2, target[1] + radius // 2), (0, 0, 255), 2)
    cv2.putText(frame, "Hostile Detected",
                (target[0] - 5 - radius // 2, target[1] - 15 - radius // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


if __name__ == "__main__":
    video_capture = cv2.VideoCapture(0)

    _, frame = video_capture.read()

    # get the frame height and width
    height, width = frame.shape[:2]

    # get the center
    center_x = width // 2
    center_y = height // 2

    threshold_y = 50
    threshold_x = 50

    shoot_range_x = range(center_x - threshold_x, center_x + threshold_x + 1)
    shoot_range_y = range(center_y - threshold_y, center_y + threshold_y + 1)

    print("Video width: ", width)
    print("Video height: ", height)
    print("Center x: ", center_x)
    print("Center y: ", center_y)
    print("Threshold x: ", threshold_x)
    print("Threshold y: ", threshold_y)
    print("Shoot range x: ", shoot_range_x)
    print("Shoot range y: ", shoot_range_y)

    while True:
        _, frame = video_capture.read()

        x, y, r, mask = detect_hostiles(frame)

        print(x, y, r)

        if r > THRESHOLD:
            draw_hostile_box(frame, (int(x), int(y)), int(r))
            if x > center_x:
                print("Hostile is to the right")
            elif x < center_x:
                print("Hostile is to the left")
            if y > center_y:
                print("Hostile is above")
            elif y < center_y:
                print("Hostile is below")
            if x in shoot_range_x and y in shoot_range_y:
                print("Shooting")

        if not 'arm' in platform.machine():
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
