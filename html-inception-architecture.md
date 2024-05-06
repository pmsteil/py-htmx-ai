# HTMLInception - Use an HTML page to generate an HTML page :)

## Architecture

### Backend
The backend is a python flask server. It has a single endpoint `/generate_page` that takes a POST request with a JSON body containing the user's prompt.


## LLM
The server uses GROQ api to generate the HTML based on the user's prompt.

# Frontend
Use Tailwind CSS for styling and HTMX for any user interaction on the page.
Generate an HTML page using HTMX with a prompt in the top bar of a page.
This prompt will then hx-post to a /generate_page python endpoint to generate the html based on the user's prompt
and replace all of the html in the generated_page div of the page.

The user can again use the top bar where they can make changes and re-generate the html for the entire page.


## Instructions

Generate the HTML page as well as the python code.
Make sure the HTML page only uses HTMX for any user interaction on the page and no inline javascript is used.
Generate a function that will generate the text based on a system prompt and use the Groq API to generate the text.



## Code Examples
Use this code to generate the text based on the system prompt and user prompt.


import os
import requests
import json
import logging

# Get the environment variables
temperature = float(os.environ.get("AI_TEMPERATURE", 0.5))
max_length = int(os.environ.get("AI_MAX_LENGTH", 256))
top_p = float(os.environ.get("AI_TOP_P", 1.0))
frequency_penalty = float(os.environ.get("AI_FREQUENCY_PENALTY", 1.0))
presence_penalty = float(os.environ.get("AI_PRESENCE_PENALTY", 1.0))
stop = os.environ.get("AI_STOP", "")
url = os.environ.get("AI_URL", "https://api.groq.io/v1/generate")

def generate_text(system_prompt: str, user_prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": f"System Prompt: {system_prompt}\nUser Prompt: {user_prompt}",
        "temperature": temperature,
        "max_length": max_length,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stop": stop
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()["text"]
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None

# Example usage:
system_prompt = "This is a system prompt."
user_prompt = "This is a user prompt."
generated_text = generate_text(system_prompt, user_prompt)
print(generated_text)
