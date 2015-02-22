import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import requests
import numpy as np
import cv2
import os
from flask import Flask

app = Flask(__name__)

import time

while True:
  import urllib, json
  # url = "http://capture-treehacks.herokuapp.com/poll"
  # url = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor=false"
  url = "http://localhost:3000/poll"
  downloadName = 'download.jpg'
  response = urllib.urlopen(url);
  data = json.loads(response.read())
  if 'imgUrl' in data:
    urllib.urlretrieve(data[u'imgUrl'], downloadName)

    img = cv2.imread(downloadName)
    height, width, depth = img.shape
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

    # cv2.imshow('image', edges)
    # cv2.waitKey(0)

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
        x, y, w, h = cv2.boundingRect(approx)
        px, py, pw, ph = float(x) / width, float(y) / height, float(w) / width, float(h) / height
        percents = [px, py, pw, ph]
        rects.append(percents)

    biggestRect = rects[0]
    for r in rects:
      bx, by, bw, bh = biggestRect
      x, y, w, h = r
      area1 = bw * bh
      area2 = w * h
      if area2 > area1:
        biggestRect = r

    # Filter some rectangles
    # 1. if the rect similar to a previously seen rect, don't include it
    # 2. if the rect is outside the area of the biggest rect, don't include it
    delta = 0.1
    finalrects = []
    for i, r1 in enumerate(rects):
      x, y, w, h = r1
      keep = True

      # previously seen rect
      for j, r2 in enumerate(rects):
        rx, ry, rw, rh = r2
        if i > j and abs(rx - x) < delta and abs(ry - y) < delta and abs(rw - w) < delta and abs(rh - h) < delta:
            keep = False

      # out of biggest rect
      if x > bx + bw or x < bx or y > by + bh or y < by:
        keep = False

      if keep:
        finalrects.append(r1)

    # Get boundaries
    minpx = 1
    minpy = 1
    maxpx = 0
    maxpy = 0
    for r in finalrects:
      px, py, pw, ph = r
      minpx = min(minpx, px)
      minpy = min(minpy, py)
      maxpx = max(maxpx, px + pw)
      maxpy = max(maxpy, py + ph)

    # Normalize rects to max percents
    maxpw = maxpx - minpx
    maxph = maxpy - minpy
    def normalize(rect):
      x, y, w, h = rect
      newx = (x - minpx) / (maxpx - minpx)
      newy = (y - minpy) / (maxpy - minpy)
      neww = w / maxpw
      newh = h / maxph
      return [newx, newy, neww, newh]
    finalrects = map(normalize, finalrects)

    aspectRatio = float(width) / height
    cv2.drawContours(img, screenCnt, -1, (0, 255, 0), 3)

    payload = {
      'rects': json.dumps(finalrects),
      'aspectRatio': json.dumps(aspectRatio)
    }
    postURL = 'http://localhost:3000/rects'
    r = requests.post(postURL, data=payload)

    # cv2.imshow('image', img)
    # cv2.waitKey(0)

    # cv2.imwrite('houghlines3.jpg', img)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)

    # cv2.imwrite('01.png', bw)
  print 'data: ' + str(data)

  time.sleep(1)

# @app.route("/<url>")
# def hello():
#     return 'hi' + url
#     return "Hello world!"

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)