import cv2

img = cv2.imread("shapes.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 3, 0)
canny = cv2.Canny(blur, 25, 75)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilate = cv2.dilate(canny, kernel)

contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in range(0, len(contours)):
    # cv2.drawContours(img, contours, i, (255, 0, 255), 2)

    peri = cv2.arcLength(contours[i], True)
    poly = [cv2.approxPolyDP(contours[i], 0.02 * peri, True)]

    # if cv2.contourArea(contours[i]) > 10000:
    # cv2.drawContours(img, poly, 1, (255, 0, 255), 2)
    cv2.drawContours(img, poly, 0, (0, 255, 0), 2)

cv2.imshow("img", img)
cv2.imshow("dilate", dilate)
cv2.waitKey(0)