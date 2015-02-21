import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import cv2
import os
from flask import Flask

app = Flask(__name__)

@app.route("/<url>")
def hello():
    return 'hi' + url
    # img = cv2.imread('messi5.jpg', 0)
    return "Hello world!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)