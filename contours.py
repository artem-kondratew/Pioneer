import cv2 as cv
import numpy as np

# img = cv.imread("cube.jpg")
image = cv.imread("shapes.jpg")

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (3, 3), 3, 0)
canny = cv.Canny(blur, 25, 75)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
dilate = cv.dilate(canny, kernel)

contours, _ = cv.findContours(dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
max_contour = contours[0]
max_area = 0
for contour in contours:
    area = cv.contourArea(contour)
    if area > max_area:
        max_contour = contour
        max_area = area
# max_contour = contours[0]
peri = cv.arcLength(max_contour, True)
poly = cv.approxPolyDP(max_contour, 0.02 * peri, True)

for point in poly:
    cv.circle(image, point[0], 5, (255, 0, 255), 2)


def build_lines(poly):
    lines = []
    for i in range(len(poly)):
        j = i + 1
        if j == len(poly):
            j = 0

        pt1 = poly[i][0]
        pt2 = poly[j][0]

        epsilon = 1e-10

        dy = pt1[1] - pt2[1]
        dx = pt1[0] - pt2[0]
        if dx == 0:
            dx = epsilon
        k = dy / dx
        # if k == 0:
        #    k = epsilon
        b = pt1[1] - k * pt1[0]
        lines.append((k, b, pt1, pt2))
    return lines


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
                cv.circle(img, (j, i), 1, (0, 0, 0), 1)
        # if line[2][0] < x0 < line[3][0] and pt[0] < x0:

        x0_proj = (line[2][0] < x0) & (x0 < line[3][0])

        x0_pos = np.zeros((h, w)).astype(bool)
        for i in range(w):
            x0_pos[:, i] = img_x[:, i] < x0[:]

        for i in range(w):
            res[:, i] += x0_pos[:, i] & x0_proj[:]

    for i in range(h):
        for j in range(w):
            if res[i, j] % 2:
                cv.circle(img, (j, i), 1, (0, 255, 0), 1)
    print("ok")


lines = build_lines(poly)

check_points(image, lines)

cv.imshow("img", image)
cv.waitKey(0)
