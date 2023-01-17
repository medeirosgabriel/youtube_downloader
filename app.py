from flask import Flask
from flask import request, send_from_directory
from downloader import *

app = Flask(__name__)
app.run(debug=True, port=5000)

# GsF05B8TFWg

@app.route('/youtube/video', methods=['POST'])
def getVideo():
    data = request.get_json()
    link = data['link']
    name = downloadVideo(link)
    return send_from_directory("./video", f"{name}.mp4", as_attachment=True)

@app.route('/youtube/music', methods=['POST'])
def getMusic():
    data = request.get_json()
    link = data['link']
    name = data['name']
    downloadMusic(link, name)
    return send_from_directory("./music", f"{name}.mp3", as_attachment=True)

@app.route('/youtube/music/<id>/<name>', methods=['GET'])
def getMusic2(id, name):
    link = 'https://www.youtube.com/watch?v=' + id
    downloadMusic(link, name)
    return send_from_directory("./music", f"{name}.mp3", as_attachment=True)

@app.route('/youtube/video/<id>', methods=['GET'])
def getVideo2(id):
    link = 'https://www.youtube.com/watch?v=' + id
    name = downloadVideo(link)
    return send_from_directory("./video", f"{name}.mp4", as_attachment=True)

