
import os
from dotenv import load_dotenv
load_dotenv()
import logging
import sys

logger = logging.getLogger()
import json
from ruth_tts_transformer.api import TTS
from flask import Flask, jsonify, send_file, redirect, url_for, request

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/", methods=['GET'])
def index():
    return 'Home sweet home!'

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

def delete_old_file(current_file):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.endswith('.wav') and f != current_file:
            os.remove(f)

tts = TTS()


@app.route("/convert/<api_token>/", methods=['GET'])
def convert(api_token):

    ## token check
    if api_token != os.environ['API_TOKEN']:
        return jsonify({
            'error': 'Wrong API Token!'
        }), 400
    
    ## voice check
    voice_name = request.args.get('voice_name')
    if not voice_name:
        return jsonify({
            'error': 'voice_name parameter is required!'
        }), 400

    if str(voice_name).lower() != "gabby":
        return jsonify({
            'error': 'Invalid voice_name parameter.'
        }), 400


    ## location check
    location = request.args.get('location')
    if not location:
        return jsonify({
            'error': 'location parameter is required!'
        }), 400
        
    if str(location).lower() != "new-york":
        return jsonify({
            'error': 'Invalid location parameter!'
        }), 400
    
    ## text check
    text = request.args.get('text')
    if not text:
        return jsonify({
            'error': 'text parameter is required!'
        }), 400
        


    ## conversion
    tts.generate(text)
    file_name = tts.parse() + ".wav"
    ## conversion ends

    ## delete previous files
    delete_old_file(file_name)

    ## send download link
    download_url = url_for('download', filename=file_name)
    return "<a href='{}'>Click Here To Download</a>".format(download_url)

@app.route("/convert/", methods=['POST'])
def convert_post():


    try:
        body = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({
            'error': 'Bad parameter(s) in request.'
        }), 400
    except:
        logger.log_uncaught_exception()

    ## token check
    if 'token' not in body:
        return jsonify({
            'error': 'token is required.'
        }), 400
    
    if body['token'] != os.environ['API_TOKEN']:
        return jsonify({
            'error': 'wrong api token.'
        }), 400
    
    ## token check
    if 'voice_name' not in body:
        return jsonify({
            'error': 'voice_name is required.'
        }), 400
    
    if str(body['voice_name']).lower() != 'gabby':
        return jsonify({
            'error': 'wrong voice_name.'
        }), 400

    ## location check
    if 'location' not in body:
        return jsonify({
            'error': 'location is required.'
        }), 400
    
    if str(body['location']).lower() != 'new-york':
        return jsonify({
            'error': 'wrong location.'
        }), 400

    ## text check
    text = body['text']
    if not text:
        return jsonify({
            'error': 'text parameter is required!'
        }), 400

    ## conversion
    tts.generate(text)
    file_name = tts.parse() + ".wav"
    ## conversion ends

    ## delete previous files
    delete_old_file(file_name)

    ## send download link
    download_url = url_for('download', filename=file_name)
    return "<a href='{}'>Click Here To Download</a>".format(download_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
