import os
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, abort
import spacy
import imghdr
from werkzeug.utils import secure_filename
import pytesseract
import numpy as np
import cv2
from PIL import Image
import json
from werkzeug.debug import DebuggedApplication
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
app = Flask(__name__, static_url_path='')
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

app.debug = True
output_dir = "./foods-model"
nlp = spacy.load(output_dir)
language = ['por','eng']
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format)

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
        #         file_ext != validate_image(uploaded_file.stream):
        #     return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/ocr/<filename>')
def ocr(filename):
    # imagem = Image.open(os.path.join(app.config['UPLOAD_PATH'], filename)).convert('RGB')
    image = cv2.imread((os.path.join(app.config['UPLOAD_PATH'], filename)), 0)
    image = cv2.resize(image,(0,0),fx=7,fy=7)
    # image = cv2.imread('/home/ahac/Documents/DISSERTAÇÃO/cardapios/datasets/por/Cy6Qt-fXAAAq79_.jpg', 0)
    blur = cv2.GaussianBlur(image,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    menu = pytesseract.image_to_string(th3, lang=language[0], config='--psm 6')
    items = extract_menu(menu)
    # return jsonify({"menu": items})
    return render_template('menu.html', items=items)
    # return jsonify({"ocr": phrase})
    # return send_from_directory(app.config['UPLOAD_PATH'], filename)

# @app.route('/')
# def index():
    # if request.headers.get('Authorization') == '42':
    #     return jsonify({"42": "a resposta para a vida, o universo e tudo mais"})
    # return jsonify({"message": "API MODEL FOOD - version 0.1"})

def extract_menu(menu):
    doc = nlp(menu.lower())
    items = []
    for ent in doc.ents:
        print(ent.label_, ent.text)
        if ent.label_ == "FOOD":
            items.append(ent.text)
    return items

@app.route('/extract', methods=['GET'])
def extract():
    menu = request.args.get('menu')
    print(menu)
    items = extract_menu(menu)
    return jsonify({"menu": items})

@app.route('/log')
def log():
    return send_from_directory('serving_static/templates', 'log.html')


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)