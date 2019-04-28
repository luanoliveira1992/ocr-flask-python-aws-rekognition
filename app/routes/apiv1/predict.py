#!/usr/bin/python3
from flask import jsonify, request,flash,redirect
import logging
from flask_restplus import Namespace, Resource
from collections import defaultdict
from app.ocr.call_ocr_aws import ocr
from werkzeug.utils import secure_filename
from werkzeug import FileStorage
import os
import re
import datetime


predict = Namespace('predict')

upload_parser = predict.parser()
upload_parser.add_argument('file', location='files',
                   type=FileStorage, required=True)


@predict.route('/')
@predict.expect(upload_parser)
class OCRPredict(Resource):
    
    """
     Recive a file was input in request, and call  aws rekognition to orc
    """
    def post(self):
        
        if 'file' not in request.files:
            flash("File not found")
            return redirect(request.url)

        file_ = request.files['file']
        
        if file_.filename == '':
           flash('No selected file')
           return redirect(request.url)
       
        file_name = secure_filename(file_.filename)
        file_.save(os.path.join('./app/ocr/uploads', file_name))
        ocr_ = ocr('./app/ocr/uploads/'+file_name)
       
        text_in_list =  ocr_.return_ocr()
        text_in = ' '.join(text_in_list)
       
        return {'prediction' : text_in}
       
