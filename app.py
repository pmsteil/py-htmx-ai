"""
    The main.py file is a Flask web application that uses the OpenAI API to generate HTML and CSS code based on a given prompt.

    To install the dependencies, run the following pip command:
        pip install -r requirements.txt

    The application defines a single route (/) that accepts POST requests. When a request is received, it extracts a 'prompt' from the request data. This prompt is then used to generate a message that is sent to the OpenAI API.

    The OpenAI API is expected to return HTML and CSS code based on the prompt. The generated code is intended to be directly written to the innerHTML of an HTML element and used in production.

    The application emphasizes that the generated code should not include any extra text or comments, and should not use any libraries or imports not provided in the task. It also provides guidelines for using images and SVG icons, and for ensuring that HTML elements are properly closed.

    To run this application, you need to have the OpenAI API key set as an environment variable. The application uses this key to authenticate with the OpenAI API.

    The application is designed to be used as part of a larger system that allows users to generate HTML and CSS code based on prompts. The generated code can be used to create web applications with Tailwind CSS styling.

    The application demonstrates how the OpenAI API can be used to generate code snippets based on user prompts, and how these snippets can be integrated into web applications to enhance development workflows.

    To start this flask server, run the following command:
        python main.py

    The server will start running on port 80 by default. You can change the port by modifying the app.run() method.

    If you get this error: "Permission denied", you can run the following command:
        sudo python main.py

"""
import os
from flask import Flask, request, jsonify, render_template, send_file, Response
from openai import OpenAI
from dotenv import load_dotenv
from openai import ChatCompletion
from bs4 import BeautifulSoup


# load ENV vars
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

# define the default model to use
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", 0)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home() -> str:
    return render_template('index.html')

class ChatBot:
    def __init__(self, previous_messages:list[dict]) -> None:
        self.previous_messages = previous_messages

    def generate_html(self, prompt:str, with_context:bool=False) -> str:
        client = OpenAI()
        system_prompt = ("You are an expert at writing HTML and CSS. "
                        "Your Task is to write new HTML and CSS Code for a web app, according to the provided task details. "
                        "The html code you write can make use of Tailwind classes for styling. "
                        "Your generated code will be directly written to innerHTML of an HTML Element and used in production.")

        user_prompt = ("- CODE DESCRIPTION :\n"
                    "```\n" +
                    prompt +
                    "\n```\n\n"
                    "Answer with generated code only. DO NOT ADD ANY EXTRA TEXT DESCRIPTION OR COMMENTS BESIDES THE CODE. Your answer contains code only ! "
                    "Only include images if you are specifically asked for it. If asked to use images you can use https://source.unsplash.com/random/ as the image source. You can use one keyword to get a specific image by providing it like this https://source.unsplash.com/random/?keyword. "
                    "When using images make sure that they are not stretched by using object-cover or bg-cover on the image. "
                    "Write the full code for the new HTML and CSS for the web app. which uses tailwind classes if needed. you can use the svg icon code of heroicons directly if needed."
                    "The code that you write will be written directly into an HTML DOM Make sure that all html elements are closed properly and that your full code in enclosed with ```html blocks."
                    "Do not use libraries or imports except what is provided in this task; otherwise it would crash the component because not installed. Do not import extra libraries besides what is provided above !"
                    "Write the Code as the creative genius that you are - with good ui formatting.")

        debug( f"Calling OpenAI({OPENAI_MODEL})... with prompt: \n" + prompt, 1)
        
        current_prompts = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        current_conversation:list[dict] = []
        if with_context:
            current_conversation = [message for message in self.previous_messages]
        for prompt in current_prompts:
            current_conversation.append(prompt)
        response = client.chat.completions.create(model=OPENAI_MODEL, messages=current_conversation)

        html_code = response.choices[0].message.content.split("```html")[1].split("```")[0].strip()

        debug(f"RETURNING HTML CODE:\n{html_code}\n", 2)

        return html_code

html_chatbot = ChatBot([])

@app.route('/generate', methods=['GET'])
def generate_html_with_ai_button() -> str:
    """
    Generate HTML and CSS code based on a given prompt
    Add the prompt and the response to previous_messages within html_chatbot
    """
    if request.method == 'GET':
        prompt = request.args.get('prompt', None)
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        html_code = html_chatbot.generate_html(f'{prompt}', with_context=True)
        prompt_and_response = [{'role': 'user', 'content': f'{prompt}'}, {'role': 'assistant', 'content': html_code}]
        for prompt in prompt_and_response:
            html_chatbot.previous_messages.append(prompt)

        return html_code

@app.route('/download_file/<filename>')
def download_file(filename:str) -> Response:
    """
    Download a file that is in the same directory as app.py
    If <filename> == prototype.html, create prototype.html first
    """
    if filename == 'prototype.html':
        update_prototype_html_file()
    return send_file(filename, as_attachment=True)

def update_prototype_html_file():
    for message in reversed(html_chatbot.previous_messages):
        if message['role'] == 'assistant':
            prototype_html = message['content']
            break
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'prototype.html')
    with open(file_path, 'w') as prototype:
        html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Prototype</title>
        <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body>{prototype_html}</body>
        </html>'''
        prototype.write(html_content)

def debug(message:str, level:int=1) -> None:
    """
    Print debug messages based on the DEBUG_LEVEL environment variable.
    Args:
        message (str): The message to print.
        level (int): The debug level of the message.
    """
    if DEBUG_LEVEL and int(DEBUG_LEVEL) >= level:
        print(message)
        
# Run the server on port 3333
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)
