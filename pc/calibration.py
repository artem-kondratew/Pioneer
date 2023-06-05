import numpy as np
import cv2 as cv
import pickle
import rpi_camera

number_of_samples = 15

number_of_hor_corners = 6
number_of_ver_corners = 9

counter = 0
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
obj_p = np.zeros((number_of_hor_corners*number_of_ver_corners, 3), np.float32)
obj_p[:, :2] = np.mgrid[0:number_of_ver_corners, 0:number_of_hor_corners].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
obj_points = []  # 3d point in real world space
img_points = []  # 2d points in image plane.

#cap = rpi_camera.open_cap()
cap = cv.VideoCapture(0)

while True:
    _, img = cap.read()
    cv.imshow('pioneer_camera_stream', img)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    if cv.waitKey(1) == ord('p'):
        ret, corners = cv.findChessboardCorners(gray, (number_of_ver_corners, number_of_hor_corners), None)

        # If found, add object points, image points (after refining them)
        if ret:
            obj_points.append(obj_p)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)
            img = cv.drawChessboardCorners(img, (number_of_ver_corners, number_of_hor_corners), corners2, ret)
            cv.imshow('img', img)
            print(f'сделано {counter + 1} снимков. Осталось сделать еще {number_of_samples - counter - 1}')
            counter += 1
            cv.waitKey(500)
            cv.destroyWindow('img')
        else:
            print('Не удалось сделать снимок')

    if counter == number_of_samples:
        cv.destroyAllWindows()
        break

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

file = open('calibration_matrix.data', 'wb')
pickle.dump((mtx, dist), file)
file.close()
