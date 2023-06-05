import flight
import aruco
import multiprocessing as mp


def main():
    q = mp.Queue(1)

    flight_thread = mp.Process(target=flight.flight, args=(q,))
    aruco_thread = mp.Process(target=aruco.img_proc, args=(q,))

    aruco_thread.start()
    flight_thread.start()


if __name__ == '__main__':
    main()
