## Note, DO NOT RUN THIS SERVER ON A PUBLIC NETWORK. IT IS NOT SECURE AND IS VULNERABLE TO ATTACKS
AND SOMEONE CAN EASILY just run:
```bash
https://x.x.x.x/generate?prompt=webpage
```

and utilize your OPENAI API KEY and run up your bill!



# Python Version of htmx-ai

This is a Python version of the htmx-ai project. The original project is written in JavaScript and is available at [https://github.com/bufferhead-code/htmx-ai?tab=readme-ov-file](https://github.com/bufferhead-code/htmx-ai?tab=readme-ov-file).

The Python version is almost identical, but for some reason I could not get the hx-ai to POST to the server, had to change it to a GET.

## Installation

```bash
conda create -n htmx-ai python=3.10
conda activate htmx-ai
pip install -r requirements.txt
```

## Running the server

The server defaults to running on port 80. To start the server, run the following command:

```bash
python app.py
```


