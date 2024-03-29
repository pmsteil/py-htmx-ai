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

from flask import Flask, request, jsonify
from openai import OpenAI, ChatCompletion

# load ENV vars
from dotenv import load_dotenv
from openai import ChatCompletion
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)


openai = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

def _generate_html_based_on_prompt( prompt):
    """
    Generate HTML and CSS code based on a given prompt using the OpenAI API.
    Args:
        prompt (str): The prompt for generating the code.
    Returns:
        str: The generated HTML and CSS code.
    """
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

    combined_prompt = system_prompt + user_prompt

    response = ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    html_code = response['choices'][0]['message']['content'].split("```html")[1].split("```")[0]

    return html_code


@app.route('/try', methods=['GET'])
def generate_html2():
    """
    Generate HTML and CSS code based on a given prompt.
    """
    prompt = "Create a button with a red background and white text color."
    html_code = _generate_html_based_on_prompt(prompt)
    return html_code

@app.route('/', methods=['POST'])
def generate_html():
    """
    API endpoint called by the front end app to generate HTML and CSS code based on a given prompt.
    """
    data = request.get_json()
    prompt = data['prompt'].replace('\\n', '\n')
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

    # combined_prompt = system_prompt + user_prompt

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    html_code = response['choices'][0]['message']['content'].split("```html")[1].split("```")[0]

    return jsonify({'html_code': html_code})

if __name__ == '__main__':
    app.run(port=9999, debug=True)
