import os
from flask import Flask, jsonify, request, render_template, send_from_directory
import spacy

app = Flask(__name__, static_url_path='')
output_dir = "./foods-model"
nlp = spacy.load(output_dir)

@app.route('/')
def index():
    # if request.headers.get('Authorization') == '42':
    #     return jsonify({"42": "a resposta para a vida, o universo e tudo mais"})
    return jsonify({"message": "API MODEL FOOD - version 0.1"})

@app.route('/extract', methods=['GET'])
def extract():
    menu = request.args.get('menu')
    
    print(menu)
    doc = nlp(menu.lower())
    items = []
    for ent in doc.ents:
        print(ent.label_, ent.text)
        if ent.label_ == "FOOD":
            items.append(ent.text)
    return jsonify({"menu": items})

@app.route('/log')
def log():
    return send_from_directory('serving_static/templates', 'log.html')


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)