# ai-sampler
A simple App Engine frontend for GPT-3 and Stable Diffusion 

To set up:

Create the `.env` file containing two keys:

 * `REPLICATE_API_TOKEN` -- get it [here](https://replicate.com/pricing).
 * `OPENAI_API_TOKEN` -- get it [here](https://beta.openai.com/account/api-keys).

Optionally, create the `allowed-domains.txt` file listing the origins (one per line) of domains you would like this app to allow cross-origin requests from. The line can be a case-sensitive origin string or a glob pattern.

Then [create](https://cloud.google.com/appengine/docs/standard/python3/building-app) an App Engine project for this directory and deploy it.
