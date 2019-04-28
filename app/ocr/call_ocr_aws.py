#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

class ocr:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.map = {}

    def return_ocr(self):

        client=boto3.client('rekognition')
        with open(self.arquivo, 'rb') as image:
            response = client.detect_text(Image={'Bytes': image.read()})
        
       

        textDetections=response['TextDetections']

        detected_words =[]
        for text in textDetections:
            if(text['Type'] == 'WORD'): # There are several types, we are looking for only word
                detected_words.append(text['DetectedText'])
        
        return detected_words