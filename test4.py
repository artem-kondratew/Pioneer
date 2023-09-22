import cv2 as cv
import numpy as np


img = cv.imread("/home/user/Pictures/img.jpg")


gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

kernel = np.array(
    [[0.01, 0.08, 0.01],
     [0.08, 0.64, 0.08],
     [0.01, 0.08, 0.01]]
)

conv = cv.blur(gray, (3, 3))

cv.imshow("img", conv)
cv.imshow("orig", img)
cv.waitKey(0)
