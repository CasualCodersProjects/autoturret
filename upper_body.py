# from https://github.com/Limerin555/Real-time_Upper_Body_Detection/blob/e796cb43ffe3987ce3fbd8051c5f66b4fe340171/real_time_upper_body_detection.py
import cv2
import imutils

haar_upper_body_cascade = cv2.CascadeClassifier(
    "data/haarcascades/haarcascade_upperbody.xml")

# Uncomment this for real-time webcam detection
# If you have more than one webcam & your 1st/original webcam is occupied,
# you may increase the parameter to 1 or respectively to detect with other webcams, depending on which one you wanna use.

# video_capture = cv2.VideoCapture(0)

# For real-time sample video detection
video_capture = cv2.VideoCapture(0)
video_width = video_capture.get(3)
video_height = video_capture.get(4)

while True:
    ret, frame = video_capture.read()

    # resize original video for better viewing performance
    frame = imutils.resize(frame, width=1000)
    # convert video to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    upper_body = haar_upper_body_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        # Min size for valid detection, changes according to video size or body size in the video.
        minSize=(50, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the upper bodies
    for (x, y, w, h) in upper_body:
        # creates green color rectangle with a thickness size of 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        # creates green color text with text size of 0.5 & thickness size of 2
        cv2.putText(frame, "Hostile Detected", (x + 5, y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('Video', frame)  # Display video

    # stop script when "q" key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture
video_capture.release()
cv2.destroyAllWindows()
