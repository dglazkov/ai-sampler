# ai-sampler
A simple App Engine frontend for GPT-3 and Stable Diffusion 

To set up, create a `.env` file containing two keys:

 * `REPLICATE_API_TOKEN` -- get it [here](https://replicate.com/pricing).
 * `OPENAI_API_TOKEN` -- get it [here](https://beta.openai.com/account/api-keys).

 Then [create](https://cloud.google.com/appengine/docs/standard/python3/building-app) an App Engine project for this directory and deploy it. 