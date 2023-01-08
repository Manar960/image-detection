import cv2
import numpy as np

image = cv2.imread('img1/example.jpg')
# to gray scale
imgGry = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# thrasholding
ret, thrash = cv2.threshold(imgGry, 120, 255, cv2.CHAIN_APPROX_NONE)
destance = cv2.GaussianBlur(image, (3, 3), 3, 0)
edges = cv2.Canny(destance, 25, 100)
kernel = np.ones((10, 10), 'uint8')
dilation = cv2.dilate(edges, kernel, iterations=1)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
hierarchy = hierarchy[0]
for cnt in range(len(contours)):
    peri = cv2.arcLength(contours[cnt], True)
    approx = cv2.approxPolyDP(contours[cnt], 0.02 * peri, True)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5

    if hierarchy[cnt][2] == -1 and hierarchy[cnt][3] == -1:
        if len(approx) == 2 or len(approx)< 5:
            cv2.putText(image, "Line", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
        else:
               cv2.putText(image, "Carve", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))

    elif hierarchy[cnt][2] != -1 and hierarchy[cnt][3] == -1 and hierarchy[hierarchy[cnt][2]][2] == -1:
        if len(approx) == 3:
            cv2.putText(image, "Tringel", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
        elif len(approx) == 4:

                cv2.putText(image, "Rectangel", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))

        else:
            cv2.putText(image, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
    elif ((hierarchy[cnt][3] == -1) and (hierarchy[cnt][2] != -1)):
        cv2.putText(image, "Face", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
    elif ((hierarchy[hierarchy[cnt][3]][3] == -1) and (hierarchy[cnt][2] != -1)):
        cv2.putText(image, "22 ", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))

    elif hierarchy[cnt][3] != -1 and hierarchy[cnt][0] == -1 and hierarchy[cnt][1] == -1:
        cv2.putText(image, "11 ", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
    else:
        if hierarchy[cnt][1] == -1:
            cv2.putText(image, "Mouth", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
        elif (hierarchy[hierarchy[cnt][1]][1] == -1):
            x, y, w, z = cv2.boundingRect(approx)
            xm = int(x + (w / 3))
            ym = int(y + (z / 1.5))
            cv2.putText(image, "Nose", (xm+20, ym), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
        else:
            cv2.putText(image, "Eye", (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))

cv2.imshow('det', image)
cv2.waitKey(0)
cv2.destroyAllWindows()