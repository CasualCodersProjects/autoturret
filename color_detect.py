import cv2
# import imutils
import asyncio


def chunk_work(width, height):
    return [
        (0, 0, width//2, height//2),
        (width//2, 0, width, height//2),
        (0, height//2, width//2, height),
        (width//2, height//2, width, height)
    ]


async def worker(frame, start_x, end_x, start_y, end_y):
    most_blue = (0, 0, 0)
    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            blue = frame[j, i, 0]
            green = frame[j, i, 1]
            red = frame[j, i, 2]
            if blue > most_blue[0]:
                if green < blue/2 or red < blue/2:
                    most_blue = (blue, i, j)
    return most_blue


async def main():

    video_capture = cv2.VideoCapture(0)
    video_width = int(video_capture.get(3))
    video_height = int(video_capture.get(4))

    print("Video width: ", video_width)
    print("Video height: ", video_height)

    chunks = chunk_work(video_width, video_height)

    while True:
        _, frame = video_capture.read()

        most_blue = (0, 0, 0)

        blues = []

        for chunk in chunks:
            start_x, start_y, end_x, end_y = chunk
            blues.append(asyncio.ensure_future(
                worker(frame, start_x, end_x, start_y, end_y)))

        for blue in blues:
            blue = await blue
            if blue[0] > most_blue[0]:
                most_blue = blue

        cv2.circle(frame, (most_blue[1], most_blue[2]), 10, (0, 0, 255), -1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
