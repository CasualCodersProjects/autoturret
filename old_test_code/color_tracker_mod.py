import cv2
import color_tracker


def tracker_callback(t: color_tracker.ColorTracker):
    cv2.imshow("debug", t.debug_frame)
    cv2.waitKey(1)


tracker = color_tracker.ColorTracker(
    max_nb_of_objects=1, max_nb_of_points=20, debug=True)
tracker.set_tracking_callback(tracker_callback)

with color_tracker.WebCamera() as cam:
    # Define your custom Lower and Upper HSV values
    tracker.track(cam, [0, 0, 50], [7, 100, 100], max_skipped_frames=24)
