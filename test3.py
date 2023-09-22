from pioneer_sdk import Pioneer
import time

rpi_ip = '192.168.43.148'
gs_router_port = 5656

drone = Pioneer(name='pioneer', ip=rpi_ip, mavlink_port=gs_router_port, connection_method='udpout',
                  device='/dev/serial0', baud=230400, logger=True, log_connection=True)

drone.arm()
drone.takeoff()
time.sleep(5)

tr = [[0, 1], [1, 2]]

for i in range(len(tr)):
    drone.go_to_local_point_body_fixed(x=tr[i][0], y=tr[i][1], z=0, yaw=0)

    while not drone.point_reached():
        pass

drone.led_control(r=100, b=100)

drone.land()
