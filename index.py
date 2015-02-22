import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import cv2
import os
from flask import Flask

app = Flask(__name__)

img = cv2.imread('test2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 3)
# res,gray = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 100, 300)

# (cnts, _) = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
# screenCnt = None
# # loop over our contours
# for c in cnts:
#   # approximate the contour
#   peri = cv2.arcLength(c, True)
#   approx = cv2.approxPolyDP(c, 0.02 * peri, True)

#   # if our approximated contour has four points, then
#   # we can assume that we have found our screen
#   if len(approx) == 4:
#     screenCnt = approx
#     break

# cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

minLineLength = 100
maxLineGap = 10

cv2.imshow('image', edges)
cv2.waitKey(0)

# lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
# for x1,y1,x2,y2 in lines[0]:
#     cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

edges = cv2.bilateralFilter(edges, 11, 90, 90)

# lines = cv2.HoughLines(edges,1,np.pi/180,200)
# for rho,theta in lines[0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))

    # cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

(cnts, _) = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

screenCnt = []
rects = []

# loop over our contours
for c in cnts:
  # approximate the contour
  peri = cv2.arcLength(c, True)
  approx = cv2.approxPolyDP(c, 0.02 * peri, True)

  # if our approximated contour has four points, then
  # we can assume that we have found our screen
  if len(approx) >= 4:
    screenCnt.append(approx)
    rects.append(cv2.boundingRect(approx))

cv2.drawContours(img, screenCnt, -1, (0, 255, 0), 3)

cv2.imshow('image', img)
cv2.waitKey(0)

# cv2.imwrite('houghlines3.jpg', img)
# cv2.imshow('test', img)
# cv2.waitKey(0)

# cv2.imwrite('01.png', bw)

# @app.route("/<url>")
# def hello():
#     return 'hi' + url
#     return "Hello world!"

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)