import multiprocessing as mp
import cv2 as cv
import numpy as np
import sys
import pickle
from rpi_camera import open_cap, cap_center, delay

aruco_marker_size = 0.2  # m


def get_calibrated_params() -> (np.array, np.array):
    try:
        file = open('calibration_matrix.data', 'rb')
        matrix, dist_params = pickle.load(file)
        return matrix, dist_params
    except FileNotFoundError:
        print('Не удалось открыть калибровочный файл')
        sys.exit(-1)


def find_center(marker) -> (int, int):
    x = marker.sum(axis=0) / len(marker)
    return x.astype(int)


def draw_marker_pose(img, marker_list):
    if not marker_list:
        return
    for marker in marker_list:
        x, y = find_center(marker[0])
        cv.circle(img, (x, y), 4, (0, 255, 0), 2)
        cv.line(img, (x, y), cap_center, (0, 255, 255), 2)


def find_recs_tvecs(corners, marker_sz, cap_mtx, cap_dist) -> (list, list):
    marker_points = np.array([[-marker_sz / 2, marker_sz / 2, 0],
                              [marker_sz / 2, marker_sz / 2, 0],
                              [marker_sz / 2, -marker_sz / 2, 0],
                              [-marker_sz / 2, -marker_sz / 2, 0]], dtype=np.float32)
    rvecs = []
    tvecs = []
    for _ in corners:
        _, R, t = cv.solvePnP(marker_points, corners[0], cap_mtx, cap_dist, False, cv.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
    return rvecs, tvecs


def get_aruco_id(array: np.array) -> int | None:
    if not array:
        return None
    return array[0][0]


def find_actual_aruco(aruco_markers, aruco_ids):
    max_id = np.max(aruco_ids)
    # print(max_id)
    # print(aruco_markers)


def img_proc(q: mp.Queue):
    aruco5 = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_5X5_50)
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(aruco5, parameters)

    mtx, dist = get_calibrated_params()
    cap = open_cap()
    # cap = cv.VideoCapture(0)

    while True:
        cap_read_ret, image = cap.read()
        if not cap_read_ret:
            continue

        image = cv.rotate(image, cv.ROTATE_180)
        markerCorners, markerIds, _ = detector.detectMarkers(image)
        if markerCorners:
            find_actual_aruco(markerCorners, markerIds)

        rvec, tvec = find_recs_tvecs(markerCorners, aruco_marker_size, mtx, dist)
        if rvec and tvec:
            cv.drawFrameAxes(image, mtx, dist, rvec[0], tvec[0], 0.01)
            cap_x = np.array([[float(tvec[0][0]).__round__(3)], [float(tvec[0][1]).__round__(3)]])
            cap_y = np.array([tvec[0][0], tvec[0][1]]).round(3)
            print('COORDINATES:\n', cap_x)
            if True:  # abs(x) >= 0 and abs(y) >= 0:
                if not q.empty():
                    q.get()
                q.put(cap_x)
                # print(cap_x)

        cv.circle(image, cap_center, 4, (255, 0, 255), 2)

        draw_marker_pose(image, markerCorners)
        cv.aruco.drawDetectedMarkers(image, markerCorners, markerIds)

        cv.imshow('Camera view', image)
        cv.waitKey(delay)


if __name__ == '__main__':
    img_proc(mp.Queue(1))
