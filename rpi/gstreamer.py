import os
import sys
import subprocess
import gi

gi.require_version('Gst', '1.0')

from gi.repository import Gst


def find_remote_ip() -> str:
    output = subprocess.check_output('echo $SSH_CLIENT', shell=True).decode("utf-8")[:-1]
    return output[:output.find(" ")]


def start_stream():
    ip = find_remote_ip()
    # ip = '127.0.0.1'
    if ip == '':
        print('no remote ip')
        sys.exit(-1)
    port = 4000

    fps = 20
    width = 640
    height = 480

    # initialize GStreamer
    Gst.init(None)

    # build the pipeline
    pipeline = Gst.parse_launch(
        f'v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width={width},height={height},'
        f'framerate={fps}/1 ! jpegenc ! rtpjpegpay ! udpsink host={ip} port={port}'
    )

    # start playing
    pipeline.set_state(Gst.State.PLAYING)

    # wait until EOS or error
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

    # free resources
    pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    os.system("clear")
    # os.system('./gs_router &')
    start_stream()
