API_TOKEN = ""

import logging
import sys

logger = logging.getLogger()
import json
from ruth_tts_transformer.api import TTS
from flask import Flask, jsonify, send_file

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/", methods=['GET'])
def index():
    return 'Home sweet home!'

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    return send_file(file_name, as_attachment=True)
    
@app.route("/convert/<api_token>/<text>", methods=['GET'])
def convert(api_token, text):

    ## token check
    if api_token != API_TOKEN:
        return jsonify({
            'error': 'Wrong API Token!'
        }), 400
    
    ## conversion

    tts = TTS()
    tts.generate(text)
    file_name = tts.parse() + ".wav"

    ## conversion ends

    return redirect('download', filename=file_name)

  

if __name__ == "__main__":
    app.run(host='0.0.0.0')
