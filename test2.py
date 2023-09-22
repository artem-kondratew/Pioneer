import cv2 as cv
import numpy as np


def check_points(img, lines):
    h, w, _ = img.shape
    y0 = np.arange(0, h, 1)

    img_x = np.zeros((h, w)).astype(int)
    img_x[:] = np.arange(0, w, 1)

    res = np.zeros((h, w)).astype(int)

    for line in lines:
        x0 = ((y0 - line[1]) / line[0]).astype(int)
        if line[0] == 0:
            # x0 = np.copy(y0)
            # x0[...] = w
            pass
        else:
            pass

        for i, j in zip(range(h), x0):
            if 0 <= j <= w and 0 <= i <= h:
                pass
                #cv.circle(img, (j, i), 1, (0, 0, 0), 1)
        # if line[2][0] < x0 < line[3][0] and pt[0] < x0:

        x0_proj = (line[2][0] < x0) & (x0 < line[3][0])

        x0_pos = np.zeros((h, w)).astype(bool)
        for i in range(w):
            x0_pos[:, i] = img_x[:, i] < x0[:]

        for i in range(w):
            res[:, i] += x0_pos[:, i] & x0_proj[:]

    print(res)
    for i in range(h):
        for j in range(w):
            if res[i, j] % 2:
                #cv.circle(img, (j, i), 1, (0, 255, 0), 1)
                pass
    print("ok")


image = np.array([[[1, 2, 3], [4, 5, 6]],
                [[7, 8, 9], [10, 11, 12]],
                [[13, 14, 15], [16, 17, 18]]])

line1 = (1, 2, (-2, 6), (7, 8))
line2 = (2, -3, (4, 8), (6, 5))

lines = [line1]

check_points(image, lines)
