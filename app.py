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

def _generate_html_based_on_prompt(prompt:str) -> str:
    """
    Generate HTML and CSS code based on a given prompt using the OpenAI API.
    Args:
        prompt (str): The prompt for generating the code.
    Returns:
        str: The generated HTML and CSS code.
    """
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
    response = client.chat.completions.create(model=OPENAI_MODEL,
                                              messages=[
                                                  {"role": "system", "content": system_prompt},
                                                  {"role": "user", "content": user_prompt}
                                              ])

    html_code = response.choices[0].message.content.split("```html")[1].split("```")[0].strip()

    debug(f"RETURNING HTML CODE:\n{html_code}\n", 2)

    return html_code


@app.route('/', methods=['GET'])
def home() -> str:
    return render_template('index.html')


@app.route('/generate', methods=['POST', 'GET'])
def generate_html() -> str:
    """
    Generate HTML and CSS code based on a given prompt.
    This function has a side effect of updating prototype.html
    with the generated html.
    """
    if request.method == 'GET':
        prompt = request.args.get('prompt', None)
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        hx_target = request.headers.get('hx-target')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prototype_path = os.path.join(current_dir, 'prototype.html')
        with open(prototype_path, 'r') as file:
            current_html = file.read()
        soup = BeautifulSoup(current_html, 'html.parser') # soup is yummy

        target_div = soup.find('div', id=hx_target)
        prompt_prefix = f"Here's what I have so far:\n{target_div}"

        html_code = _generate_html_based_on_prompt(f'{prompt_prefix}\n{prompt}')
        
        update_prototype(html_code, hx_target)

        return html_code

    # hmm, couldn't get post to work... so using get for now
    # POST http://127.0.0.1:3333/generate 415 (UNSUPPORTED MEDIA TYPE)
    elif request.method == 'POST':
        data = request.json
        prompt = data.get('prompt', None)

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        html_code = _generate_html_based_on_prompt(prompt)
        response = jsonify({'html_code': html_code})
        return response
    

def update_prototype(html_code:str, hx_target:str) -> None:
    """
    Update prototype.html in the div
    that has an id that matches the hx-target of whatever generated the html
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prototype_path = os.path.join(current_dir, 'prototype.html')
    with open(prototype_path, 'r') as file:
        current_html = file.read()
    soup = BeautifulSoup(current_html, 'html.parser') # soup is yummy

    target_div = soup.find('div', id=hx_target)
    target_div.clear()
    target_div.append(html_code)

    with open(prototype_path, 'w') as file:
        file.write(soup.prettify(formatter=None))


@app.route('/download_file/<filename>')
def download_file(filename:str) -> Response:
    """
    Download a file that is in the same directory as app.py
    """
    return send_file(filename, as_attachment=True)


def debug(message:str, level:int=1) -> None:
    """
    Print debug messages based on the DEBUG_LEVEL environment variable.
    Args:
        message (str): The message to print.
        level (int): The debug level of the message.
    """
    if DEBUG_LEVEL and int(DEBUG_LEVEL) >= level:
        print(message)


def reset_prototype_html() -> None:
    """
    Reset prototype.html by reading prototype-start.html and copying it...
    If index.html changes, we currently have to manually change prototype-start.html
    Not the best way to do this, but the important part is that prototype-start.html
    doesn't have the "Regenerate section with AI" buttons or the top bar.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prototype_start_path = os.path.join(current_dir, 'prototype-start.html')
    prototype_path = os.path.join(current_dir, 'prototype.html')
    with open(prototype_start_path, 'r') as prototype_start:
        starting_html = prototype_start.read()
    
    with open(prototype_path, 'w') as prototype:
        prototype.write(starting_html)
        
# Run the server on port 3333
if __name__ == '__main__':
    reset_prototype_html() # Right now we're only reseting prototype.html on startup
    app.run(host='0.0.0.0', port=3333, debug=True)
