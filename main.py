import os
from threading import Thread
import gstreamer


def main():
    os.system("clear")
    # os.system('./gs_router &')
    stream = Thread(target=gstreamer.start_stream)

    stream.start()


if __name__ == "__main__":
    main()
