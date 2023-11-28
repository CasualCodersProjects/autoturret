import cv2
import numpy as np

img = cv2.imread("coloredCircles.png")
red_pixels = np.argwhere(cv2.inRange(img, (0, 0, 225), (30, 30, 300)))
for px, py in red_pixels:
    cv2.circle(img, (py, px), 5, (0, 255, 255), 1)
cv2.imwrite("out.png", img)