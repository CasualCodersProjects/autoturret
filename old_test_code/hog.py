import cv2


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness=1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w,
                      y+h-pad_h), (0, 255, 0), thickness)


# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
# cap.release()

# cap = cv2.VideoCapture(0)
# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('image', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    found, w = hog.detectMultiScale(
        frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
    draw_detections(frame, found)
    cv2.imshow('feed', frame)
    ch = 0xFF & cv2.waitKey(1)
    if ch == 27:
        break
cv2.destroyAllWindows()
