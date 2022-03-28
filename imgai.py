import cv2
import os
from imageai.Detection import ObjectDetection

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(os.getcwd(), "data",
                      "retinanet", "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
detections = detector.CustomObjects(person=True)

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    # frame = imutils.resize(frame, width=1000)
    # convert video to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect people in the image
    _, people = detector.detectObjectsFromImage(
        input_image=frame, input_type="array", output_type="array", custom_objects=detections)

    # draw bounding boxes around detected people
    for person in people:
        print(person["name"])
        print(person["percentage_probability"])
        print(person["box_points"])
        x, y, w, h = person["box_points"]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, person["name"], (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Video', frame)  # Display video

    # stop script when "q" key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture
video_capture.release()
cv2.destroyAllWindows()
