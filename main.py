import time

import cv2
import fire

from detect import detect_hostiles
from play_sound import get_sound, play_sound

try:
    from stepper_control_thread import StepperThread
except:
    from dummy_stepper_control_thread import StepperThread

from gpio_control import Pin
from video_get import VideoGet

STEP_X_PIN = 12
DIR_X_PIN = 16
DIR_Y_PIN = 40
STEP_Y_PIN = 38
ENABLE_X_PIN = 8
ENABLE_Y_PIN = 36
AIR_PIN = 37


def draw_hostile_box(frame, target, radius):
    cv2.rectangle(frame, (target[0] - radius // 2, target[1] - radius // 2),
                  (target[0] + radius // 2, target[1] + radius // 2), (0, 0, 255), 2)
    cv2.putText(frame, "Hostile Detected",
                (target[0] - 5 - radius // 2, target[1] - 15 - radius // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


x_stepper = None
y_stepper = None


def sentry(dry_run=False, verbose=False, display_frame=False, display_mask=False, min_radius=50, scale=0, output_scale=0, hostile_output=False, shoot_box_x=50, shoot_box_y=50, sleep_time=0.0025, sound=False):
    '''
    The main sentry loop.
    '''
    video_getter = VideoGet(0).start()

    frame = None

    while frame is None:
        frame = video_getter.frame

    # get the frame height and width
    height, width = frame.shape[:2]

    # get the center
    center_x = width // 2
    center_y = height // 2

    shoot_range_x = range(center_x - shoot_box_x, center_x + shoot_box_x + 1)
    shoot_range_y = range(center_y - shoot_box_y, center_y + shoot_box_y + 1)
    deadzone_range_x = range(center_x - shoot_box_x //
                             2, center_x + shoot_box_x // 2 + 1)
    deadzone_range_y = range(center_y - shoot_box_y //
                             2, center_y + shoot_box_y // 2 + 1)

    if scale:
        height = int(height * scale)
        width = int(width * scale)
        center_x = width // 2
        center_y = height // 2
        shoot_range_x = range(center_x - shoot_box_x,
                              center_x + shoot_box_x + 1)
        shoot_range_y = range(center_y - shoot_box_y,
                              center_y + shoot_box_y + 1)
        deadzone_range_x = range(center_x - shoot_box_x //
                                 2, center_x + shoot_box_x // 2 + 1)
        deadzone_range_y = range(center_y - shoot_box_y //
                                 2, center_y + shoot_box_y // 2 + 1)

    hostile_count = 0

    print("Video width: ", width)
    print("Video height: ", height)
    print("Center x: ", center_x)
    print("Center y: ", center_y)
    print("Shoot Box X: ", shoot_box_x)
    print("Shoot Box Y: ", shoot_box_y)
    print("Shoot range x: ", shoot_range_x)
    print("Shoot range y: ", shoot_range_y)
    print("Deadzone range x: ", deadzone_range_x)
    print("Deadzone range y: ", deadzone_range_y)
    print("Min radius: ", min_radius)

    if not dry_run:
        x_stepper = StepperThread(
            step_pin=STEP_X_PIN, direction_pin=DIR_X_PIN, enable_pin=ENABLE_X_PIN, sleep_time=sleep_time).start()
        y_stepper = StepperThread(step_pin=STEP_Y_PIN,
                                  direction_pin=DIR_Y_PIN, enable_pin=ENABLE_Y_PIN, sleep_time=sleep_time).start()
        shoot_pin = Pin(pin=AIR_PIN)
        shoot_pin.setup()

    sound_gap = 5
    last_sound = 0

    if sound:
        play_sound(get_sound('turret_search'))
        last_sound = time.time()

    try:
        while True:
            frame = video_getter.frame

            if scale:
                # scale the image
                frame = cv2.resize(
                    frame, (int(width * scale), int(height * scale)))

            start = time.time()
            x, y, r, mask = detect_hostiles(frame)
            end = time.time()

            if verbose:
                print("Detect time: ", end - start)
                print(x, y, r)

            if r >= min_radius and not x in deadzone_range_x and not y in deadzone_range_y:
                draw_hostile_box(frame, (int(x), int(y)), int(r))
                if hostile_output:
                    hostile_count += 1
                    cv2.imwrite(f"hostile_{hostile_count}.jpg", frame)
                if x > center_x:
                    if not dry_run:
                        if verbose:
                            print("Moving right")
                        x_stepper.set_direction(direction=1)
                    if verbose:
                        print("Hostile is to the right")
                elif x < center_x:
                    if not dry_run:
                        if verbose:
                            print("Moving left")
                        x_stepper.set_direction(direction=0)
                    if verbose:
                        print("Hostile is to the left")
                if y > center_y:
                    if not dry_run:
                        if verbose:
                            print("Moving down")
                        y_stepper.set_direction(direction=1)
                    if verbose:
                        print("Hostile is below")
                elif y < center_y:
                    if not dry_run:
                        if verbose:
                            print("Moving up")
                        y_stepper.set_direction(direction=0)
                    if verbose:
                        print("Hostile is above")
            else:
                if not dry_run:
                    x_stepper.stop()
                    y_stepper.stop()

            if r >= min_radius and x in shoot_range_x and y in shoot_range_y:
                if not dry_run:
                    shoot_pin.on()
                if verbose:
                    print("Shooting")
                    if sound:
                        if time.time() > last_sound + sound_gap:
                            play_sound(get_sound('turret_deploy'))
                            last_sound = time.time()
            else:
                if not dry_run:
                    shoot_pin.off()
                    if sound:
                        if time.time() > last_sound + sound_gap:
                            play_sound(get_sound('turret_retire'))
                            last_sound = time.time()

            if display_mask:
                cv2.imshow("Mask", mask)
            elif display_frame:
                if output_scale:
                    frame = cv2.resize(
                        frame, (int(width * output_scale), int(height * output_scale)))
                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        video_getter.stop()
        if not dry_run:
            x_stepper.cleanup()
            y_stepper.cleanup()


if __name__ == "__main__":
    fire.Fire(sentry)
