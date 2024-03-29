from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# Konfigurasi direktori untuk menyimpan gambar
app.config["UPLOAD_FOLDER"] = "static"

client = MongoClient("mongodb+srv://Fauzan:Fauzan2608.@cluster0.tjckrzw.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    image_receive = request.files["image-give"]
    profile_receive = request.files["profile-give"]

    if image_receive:
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_receive.filename)
        image_receive.save(image_path)
    else:
        return jsonify({'msg': 'Failed to save diary entry with image.'})

    if profile_receive:
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        
        profile_path = os.path.join(app.config["UPLOAD_FOLDER"], profile_receive.filename)
        profile_receive.save(profile_path)
    else:
        return jsonify({'msg': 'Failed to save diary entry with profile image.'})

    doc = {
        'title': title_receive,
        'content': content_receive,
        'image': image_path,
        'profile': profile_path
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Data has been saved!'})


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'diary': articles})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
