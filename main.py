
import cv2
import fire

from detect import detect_hostiles
from stepper_control import Stepper

THRESHOLD = 50
STEPS_PER_LOOP = 10


def draw_hostile_box(frame, target, radius):
    cv2.rectangle(frame, (target[0] - radius // 2, target[1] - radius // 2),
                  (target[0] + radius // 2, target[1] + radius // 2), (0, 0, 255), 2)
    cv2.putText(frame, "Hostile Detected",
                (target[0] - 5 - radius // 2, target[1] - 15 - radius // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


x_stepper = None
y_stepper = None


def sentry(dry_run=False, verbose=False, display_frame=False, display_mask=False, scale=0, output_scale=0):
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

    if not dry_run:
        x_stepper = Stepper(shoot_range_x, STEPS_PER_LOOP, scale=scale)
        y_stepper = Stepper(shoot_range_y, STEPS_PER_LOOP, scale=scale)

    while True:
        _, frame = video_capture.read()

        if scale:
            # scale the image
            frame = cv2.resize(
                frame, (int(width * scale), int(height * scale)))

        x, y, r, mask = detect_hostiles(frame)

        if verbose:
            print(x, y, r)

        if r > THRESHOLD:
            draw_hostile_box(frame, (int(x), int(y)), int(r))
            if x > center_x:
                if not dry_run:
                    if verbose:
                        print("Moving right")
                    x_stepper.step(direction=1, steps=STEPS_PER_LOOP)
                if verbose:
                    print("Hostile is to the right")
            elif x < center_x:
                if not dry_run:
                    if verbose:
                        print("Moving left")
                    x_stepper.step(direction=0, steps=STEPS_PER_LOOP)
                if verbose:
                    print("Hostile is to the left")
            if y > center_y:
                if not dry_run:
                    if verbose:
                        print("Moving down")
                    y_stepper.step(direction=1, steps=STEPS_PER_LOOP)
                if verbose:
                    print("Hostile is below")
            elif y < center_y:
                if not dry_run:
                    if verbose:
                        print("Moving up")
                if verbose:
                    print("Hostile is above")
            if x in shoot_range_x and y in shoot_range_y:
                # if dry_run:
                if verbose:
                    print("Shooting")

        
        if display_mask:
            cv2.imshow("Mask", mask)
        elif display_frame:
            if output_scale:
                frame = cv2.resize(
                    frame, (int(width * output_scale), int(height * output_scale)))
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    fire.Fire(sentry)
