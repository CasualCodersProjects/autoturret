import cv2
import numpy as np

from video_get import VideoGet

LOWER_MASK_LOWER_RED = np.array([0, 50, 20])
LOWER_MASK_UPPER_RED = np.array([5, 255, 255])
UPPER_MASK_LOWER_RED = np.array([175, 50, 20])
UPPER_MASK_UPPER_RED = np.array([180, 255, 255])

# great resource: http://vikrantfernandes.com/web/html/Color-track.html


def detect_hostiles(frame, lower_mask_lower_red=LOWER_MASK_LOWER_RED, lower_mask_upper_red=LOWER_MASK_UPPER_RED, upper_mask_lower_red=UPPER_MASK_LOWER_RED, upper_mask_upper_red=UPPER_MASK_UPPER_RED):
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    # convert to hsv
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # create kernel
    kernel = np.ones((5, 5), np.uint8)

    # create mask
    mask = cv2.inRange(hsv, lower_mask_lower_red, lower_mask_upper_red)
    mask += cv2.inRange(hsv, upper_mask_lower_red, upper_mask_upper_red)

    # morphological opening
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    # morphological closing
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.erode(mask, kernel, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) <= 0:
        return (-1, -1, 0, mask)

    # Contour with greatest area
    c = max(cnts, key=cv2.contourArea)
    # Radius and center pixel coordinate of the largest contour
    ((x, y), radius) = cv2.minEnclosingCircle(c)

    return (int(x), int(y), radius, mask)


if __name__ == "__main__":

    video_getter = VideoGet(0).start()

    try:
        while True:
            frame = video_getter.frame
            x, y, radius, mask = detect_hostiles(frame)
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            print(x, y, radius)
            # cv2.imshow("Video", frame)
            # cv2.imshow("Mask", mask)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                video_getter.stop()
                break
    except KeyboardInterrupt:
        video_getter.stop()
