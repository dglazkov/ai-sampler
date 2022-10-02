import json
import os
import traceback

import openai
import replicate
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

origins = []

try:
    with open('allowed-domains.txt') as file:
        origins = file.read().splitlines()
except Exception:
    origins = []

print(origins)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=origins)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_TOKEN")


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
        image_url = model.predict(prompt=prompt)[0]
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
            "text": response.choices[0].text
        })
        return response

    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.print_exc()}"
        })


@app.route("/api/gpt-3", methods=["GET"])
def gpt_3_sample():
    return render_template("gpt-3-sample.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
