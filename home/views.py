from django.shortcuts import render

import requests

import cv2 as cv
import pytesseract

from config.settings import MEDIA_ROOT
import os

from .forms import TestMedicineForm
from .models import Medicine

import numpy as np


# get grayscale image
def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)# noise removal
def remove_noise(image):
    return cv.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv.erode(image, kernel, iterations = 1)#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv.morphologyEx(image, cv.MORPH_OPEN, kernel)#canny edge detection
def canny(image):
    return cv.Canny(image, 100, 200)#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv.warpAffine(image, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
    return rotated#template matching
def match_template(image, template):
    return cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)


def index(request):
    return render(request, "index.html")

def matching(request):

    form = TestMedicineForm(request.POST, request.FILES)
    
    instance = form.save()
    path = os.path.join(MEDIA_ROOT, str(instance.image))
    test_img = cv.imread(path, 0)

    method = "cv.TM_CCORR_NORMED"
    
    opt = 0
    opt_image = ""
    opt_temp = None

    for medicine in Medicine.objects.all():
        template = cv.imread(os.path.join(MEDIA_ROOT, str(medicine.image)), 0)
        res = cv.matchTemplate(test_img, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        current = (max_val + min_val) / 2

        if current > opt:
            opt = current
            opt_image = str(medicine.image)
            opt_temp = template

    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


    custom_config = r'-l eng+uzb+rus --psm 6'
    #text = pytesseract.image_to_string(opt_temp)
    #text = pytesseract.image_to_string(opt_temp, config=custom_config)
    text = pytesseract.image_to_string(test_img, config=custom_config)

    context = {'image' : opt_image, 'opt': opt, 'text': text}

    return render(request, 'result.html', context=context)
