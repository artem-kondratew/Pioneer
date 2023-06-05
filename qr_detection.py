import cv2 as cv

img = cv.imread('qrcode.png')

detector = cv.QRCodeDetector()

retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(img)

print(points)
for point in points[0]:
    print(point[0])
    img = cv.circle(img, (int(point[0]), int(point[1])), 4, (255, 0, 255), 2)

cv.imshow("qr", img)
cv.waitKey(0)
