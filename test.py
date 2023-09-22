import numpy as np
import cv2 as cv

image = cv.imread("shapes.jpg")

point1 = (340, 340)
point2 = (360, 330)
point = point2


def check_point(pt, lines):
    cv.circle(image, pt, 5, (0, 255, 0), 2)
    h, w, _ = image.shape
    #cv.line(img, (0, point[1]), (w, point[1]), (165, 0, 255), 2)
    cnt = 0
    for line in lines:
        y0 = pt[1]
        x0 = int((y0 - line[1]) / line[0])
        #cv.line(img, pt, (int(x0), y0), (0, 0, 255), 2)

        if line[2][0] < x0 < line[3][0] and pt[0] < x0:
            #cv.circle(img, (x0, y0), 5, (255, 255, 0), 2)
            cnt += 1
    if cnt % 2:
        return True
    return False


img = np.array([[[1, 2, 3], [4, 5, 6]],
                [[7, 8, 9], [10, 11, 12]],
                [[13, 14, 15], [16, 17, 18]]])

h, w, _ = img.shape

img_x = np.zeros((h, w)).astype(int)
img_x[:] = np.arange(0, w, 1)
print(img_x)

y0 = np.arange(0, h, 1)
print("y0", y0)

line1 = (1, 2, (-2, 6), (7, 8))
line2 = (2, -3, (4, 8), (6, 5))

lines = [line1]

res = np.zeros((h, w)).astype(int)

for line in lines:
    x0 = ((y0 - line[1]) / line[0]).astype(int)
    x0_proj1 = line[2][0] < x0
    x0_proj2 = x0 < line[3][0]
    x0_proj = x0_proj1 & x0_proj2
    print('x0', x0)
    print('x0_proj', x0_proj)

    x0_pos = np.zeros((h, w)).astype(bool)


    for i in range(len(x0_pos[0])):
        x0_pos[:, i] = img_x[:, i] < x0

    # res = x0_proj & x0_pos

    print(x0_pos)

    for i in range(len(x0_pos[0])):
        res[:, i] += x0_pos[:, i] & x0[:]

    print(res)

    # if line[2][0] < x0 < line[3][0] and pt[0] < x0:

    # res = res1 & res2
    # res = res < line[3][0]
    # res = stat_x < res[:]
    # print(res.shape, stat_x.shape)



