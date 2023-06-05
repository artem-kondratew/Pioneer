import sys
import cv2 as cv

cap_width = 640
cap_height = 480

cap_x_center = cap_width // 2
cap_y_center = cap_height // 2
cap_center = (cap_x_center, cap_y_center)


def open_cap():
    capture_pipeline = (f'udpsrc caps="application/x-rtp,media=(string)video,encoding-name=(string)JPEG" port=4000 !'
                        f'rtpjpegdepay ! jpegdec ! queue ! videoconvert ! video/x-raw,width={cap_width},'
                        f'height={cap_height},format=BGR ! appsink')

    capture = cv.VideoCapture(capture_pipeline, cv.CAP_GSTREAMER)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    if not capture.isOpened():
        print('Не удалось открыть камеру')
        sys.exit(-1)

    return capture


if __name__ == '__main__':
    cap = open_cap()
    while True:
        _, img = cap.read()
        cv.imshow('Camera view', img)
        cv.waitKey(50)
