API_TOKEN = "0000-0000-0000-0000"

import logging
import sys

logger = logging.getLogger()
import json
from ruth_tts_transformer.api import TTS
from flask import Flask, jsonify, send_file, redirect, url_for

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/", methods=['GET'])
def index():
    return 'Home sweet home!'

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)
    

tts = TTS()

@app.route("/convert/<api_token>/<voice_name>/<location>/<text>", methods=['GET'])
def convert(api_token, voice_name, location, text):

    ## token check
    if api_token != API_TOKEN:
        return jsonify({
            'error': 'Wrong API Token!'
        }), 400
    
    ## location check
    if str(location).lower() != "new-york":
        return jsonify({
            'error': 'Invalid location!'
        }), 400

    ## voice check
    if str(voice_name).lower() != "gabby":
        return jsonify({
            'error': 'Invalid voice name!'
        }), 400

    ## conversion

    
    tts.generate(text)
    file_name = tts.parse() + ".wav"
    ## conversion ends
    download_url = url_for('download', filename=file_name)
    return "<a href='{}'>Click Here To Download</a>".format(download_url)

  

if __name__ == "__main__":
    app.run(host='0.0.0.0')
