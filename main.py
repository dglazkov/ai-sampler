import urllib.request
import fnmatch
import os
import re
import traceback
import uuid

import openai
import replicate
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from google.cloud import storage

origins = []

try:
    with open('allowed-domains.txt') as file:
        origins = [re.compile(fnmatch.translate(line))
                   for line in file.read().splitlines()]

except Exception:
    pass

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=origins)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_TOKEN")

bucket_name = 'ai-sampler-generated-images'
storage_client = storage.Client()


def upload_generated_image(image_url):
    file = urllib.request.urlopen(image_url)

    filename = f"{uuid.uuid4()}.png"

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)

    blob.upload_from_string(file.read(), content_type='image/png')

    return f"https://storage.googleapis.com/{bucket_name}/{filename}"


@app.route("/api/stable-diffusion", methods=["POST"])
def stable_diffusion():
    prompt = request.form["prompt"]

    if prompt is None:
        return jsonify({
            "error": 'No prompt supplied'
        })
    try:
        replicate_client = replicate.Client(
            api_token=os.getenv("REPLICATE_API_TOKEN"))
        model = replicate_client.models.get("stability-ai/stable-diffusion")
        image_url = model.predict(**request.form)[0]
        response = jsonify({
            "prompt": prompt,
            "image_url": image_url
        })
        return response

    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.print_exc()}"
        })


@app.route("/api/stable-diffusion", methods=["GET"])
def stable_diffusion_sample():
    return render_template("stable-diffusion-sample.html")


@app.route("/api/gpt-3", methods=["POST"])
def gpt_3():
    prompt = request.form["prompt"]
    if prompt is None:
        return jsonify({
            "error": 'No prompt supplied'
        })
    try:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response = jsonify({
            "prompt": prompt,
            "text": response.choices[0].text.strip()
        })
        return response

    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.print_exc()}"
        })


@app.route("/api/gpt-3", methods=["GET"])
def gpt_3_sample():
    return render_template("gpt-3-sample.html")


@app.route("/api/dall-e", methods=["POST"])
def dall_e():
    prompt = request.form["prompt"]
    if prompt is None:
        return jsonify({
            "error": 'No prompt supplied'
        })
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )        
        return jsonify({
            "prompt": prompt,
            "image_url": upload_generated_image(response['data'][0]['url'])
        })

    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.print_exc()}"
        })


@app.route("/api/dall-e", methods=["GET"])
def dall_e_sample():
    return render_template("dall-e-sample.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
