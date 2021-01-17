from django.db import models
from config.settings import MEDIA_ROOT

import cv2 as cv
import pytesseract
import os

class MedicineGroup(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Medicine(models.Model):

    image = models.ImageField(upload_to='medicines')

    group = models.ForeignKey('MedicineGroup', on_delete=models.CASCADE)

    text = models.CharField(max_length = 200, default="", blank=True)

    def save(self, *args, **kwargs): 

        super(Medicine, self).save(*args, **kwargs)

        if self.text == "": 

            path = os.path.join(MEDIA_ROOT, str(self.image))
            test_img = cv.imread(path, 0)

            pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

            custom_config = r'-l eng+uzb+rus --psm 6'
            text = pytesseract.image_to_string(test_img, config=custom_config)
        
            self.text = text
            if self.text == "":
                self.text = '-'
            self.save()

    def __str__(self):
        return self.text

class MedicineTest(models.Model):
    image = models.ImageField(upload_to = 'test')
