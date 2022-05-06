import numpy as np
import cv2
import time
import platform

LOWER_MASK_LOWER_RED = np.array([0, 50, 20])
LOWER_MASK_UPPER_RED = np.array([5, 255, 255])
UPPER_MASK_LOWER_RED = np.array([175, 50, 20])
UPPER_MASK_UPPER_RED = np.array([180, 255, 255])
RECT_WIDTH = 50
RECT_HEIGHT = 50


def to_hsv(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


def convert_bgr_to_hsv(b, g, r):
    h, s, v = cv2.cvtColor(np.array([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]
    return h, s, v


def get_reds(frame):
    mask = cv2.inRange(frame, LOWER_MASK_LOWER_RED, LOWER_MASK_UPPER_RED)
    mask = mask + cv2.inRange(frame, UPPER_MASK_LOWER_RED,
                              UPPER_MASK_UPPER_RED)
    reds = np.argwhere(mask)
    return reds


def get_pixel_average(arr):
    xs = []
    ys = []
    for px, py in arr:
        xs.append(px)
        ys.append(py)
    if len(xs) > 0 and len(ys) > 0:
        avg_x = np.mean(xs)
        avg_y = np.mean(ys)
        return (int(avg_y), int(avg_x))
    return (0, 0)


def get_pixel_max(arr, frame):
    max_hue_value = np.array([-1, -1, -1])
    max_frame_location = np.array([-1, -1])
    for py, px in arr:
        frame_hue_value = frame[py, px]
        hue = frame_hue_value[0] if frame_hue_value[0] < max_hue_value[0] else max_hue_value[0]
        saturation = frame_hue_value[1] if frame_hue_value[1] > max_hue_value[1] else max_hue_value[1]
        value = frame_hue_value[2] if frame_hue_value[2] > max_hue_value[2] else max_hue_value[2]
        new_hue_value = np.array([hue, saturation, value])
        if np.array_equal(new_hue_value, max_hue_value):
            max_hue_value = new_hue_value
            max_frame_location = np.array([px, py])
    return max_frame_location


def draw_hostile_box(frame, target):
    cv2.rectangle(frame, (target[0] - RECT_WIDTH // 2, target[1] - RECT_HEIGHT // 2),
                  (target[0] + RECT_WIDTH // 2, target[1] + RECT_HEIGHT // 2), (0, 0, 255), 2)
    cv2.putText(frame, "Hostile Detected",
                (target[0] - 5 - RECT_WIDTH // 2, target[1] - 15 - RECT_HEIGHT // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


if __name__ == "__main__":
    video_capture = cv2.VideoCapture(0)

    lastPrint = 0

    while True:
        _, frame = video_capture.read()

        hsv_frame = to_hsv(frame)

        reds = get_reds(hsv_frame)
        # target = get_pixel_average(reds)
        target = get_pixel_max(reds, hsv_frame)

        if target.all() != -1:
            draw_hostile_box(frame, target)
            # print the target every second
            if lastPrint < time.time() - 1:
                print(target)
                b, g, r = frame[target[1], target[0]]
                print(convert_bgr_to_hsv(b, g, r))
                lastPrint = time.time()

        if not 'arm' in platform.machine():
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
