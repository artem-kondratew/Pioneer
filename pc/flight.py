import time
import multiprocessing as mp
import numpy as np
from pioneer_sdk import Pioneer

point = np.array([[float], [float]])

rpi_ip = '192.168.43.148'
gs_router_port = 5656

pioneer = Pioneer(name='pioneer', ip=rpi_ip, mavlink_port=gs_router_port, connection_method='udpout',
                  device='/dev/serial0', baud=230400, logger=True, log_connection=True)

x_des = np.array([[0.0],
                  [0.0]])

TAKEOFF_EPSILON = 0.1      # meters
TAKEOFF_CORRECT_TIME = 10  # seconds


def transform_coordinates(cap_x: point) -> point:
    rotate_matrix = np.array([[0, -1],
                              [1, 0]])
    return np.dot(rotate_matrix, cap_x)


def pxy_regulator(x_desired: point, x_measured: point) -> point:
    k = 0.5
    return k * (x_desired - x_measured)


def is_point_reached(x_desired: point, x_measured: point) -> bool:
    dx = abs(x_desired - x_measured)
    return (dx < TAKEOFF_EPSILON).all()


def move(x: float, y: float, z=0.0, angle=0):
    pioneer.go_to_local_point_body_fixed(y, x, z, angle)


def start():
    while True:
        if pioneer.connected():
            break
    pioneer.arm()
    pioneer.takeoff()


def correct_takeoff(q: mp.Queue) -> bool:
    start_time = time.time()

    while True:
        if time.time() - start_time > TAKEOFF_CORRECT_TIME:
            pass
            #return False

        if q.empty():
            continue

        cap_x = q.get()
        x = transform_coordinates(cap_x)
        u = -pxy_regulator(x_des, x)
        move(u[0], u[1])

        if is_point_reached(x_des, x):
            pass
            #return True


def user():
    time.sleep(10)
    move(2, 0)


def flight(q: mp.Queue):
    start()
    user()
    # print(correct_takeoff(q))
    #if correct_takeoff(q):
    #    move(2, 2)
    #if pioneer.point_reached():
    #    pioneer.land()


flight(mp.Queue(1))