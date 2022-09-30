import replicate
import os
import json
from flask import Flask, jsonify, request
# from google.cloud import secretmanager
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# def get_secret(key):
#     client = secretmanager.SecretManagerServiceClient()
#     project_id = os.environ["PROJECT_NAME"]
#     resource_name = f"projects/{project_id}/secrets/{key}/versions/latest"
#     response = client.access_secret_version(resource_name)
#     return response.payload.data.decode('UTF-8')

@app.route("/api/stable-diffusion", methods=["POST"])
def stable_diffusion():
    prompt = json.loads(request.data)["prompt"]
    if prompt is None:
        return jsonify({
            'error': 'No prompt supplied'
        })
    replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    model = replicate_client.models.get("stability-ai/stable-diffusion")
    image_url = model.predict(prompt=prompt)[0]
    return jsonify({ 
        "prompt": prompt,
        "image_url": image_url 
    })

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
