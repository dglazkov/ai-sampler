import replicate
import openai
import traceback

import os
import json
from flask import Flask, jsonify, request
# from google.cloud import secretmanager
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_TOKEN")


@app.route("/api/stable-diffusion", methods=["POST"])
def stable_diffusion():
    prompt = json.loads(request.data)["prompt"]
    if prompt is None:
        return jsonify({
            "error": 'No prompt supplied'
        })
    try: 
        replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
        model = replicate_client.models.get("stability-ai/stable-diffusion")
        image_url = model.predict(prompt=prompt)[0]
        return jsonify({ 
            "prompt": prompt,
            "image_url": image_url 
        })
    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.print_exc()}"
        })
        

@app.route("/api/gpt-3", methods=["POST"])
def gpt_3():
    prompt = json.loads(request.data)["prompt"]
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
        return jsonify({ 
            "prompt": prompt,
            "text": response.choices[0].text
        })
    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.print_exc()}"
        })

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
