## Note, DO NOT RUN THIS SERVER ON A PUBLIC NETWORK. IT IS NOT SECURE AND IS VULNERABLE TO ATTACKS
AND SOMEONE CAN EASILY just run:
```bash
https://x.x.x.x/generate?prompt=webpage
```

and utilize your OPENAI API KEY and run up your bill!



# Python Version of htmx-ai

This is a Python version of the htmx-ai project. The original project is written in JavaScript and is available at [https://github.com/bufferhead-code/htmx-ai?tab=readme-ov-file](https://github.com/bufferhead-code/htmx-ai?tab=readme-ov-file). You can watch the original author's video to see how the project works [https://www.youtube.com/watch?v=NP6hpM5YLRo](https://www.youtube.com/watch?v=NP6hpM5YLRo).

The Python version is almost identical, with these modifications:
- The code is written in Python (only tested with Python 3.10)
- The server is written in Python using Flask
- The server uses the OpenAI Python library to interact with the OpenAI API
- The server code was refactored a bit to separate the API from the generate html code
- The index.html is being served up from the server itself as a Flask template
- Documented code better
- Added a bit of debug on server side to see what server is doing (set DEBUG_LEVEL=0 to disable)

## Issues

1. For some reason I could not get the hx-ai to POST to the server, had to change it to a GET. Would like to use POST instead (open an issue if you know how to fix this).
2. Need to load the htmx library from a public repo.

## Roadmap

1. Would love to build this into a prototyping tool. Where the user could start with a blank page and then add elements to the page and then generate the code for each section of the page.
2. The user could specify their own "system prompt" to try and define color scheme, styling, etc to make all sections have some uniformity.
3. The user could then download the code for the page they created.
4. The user could generate the template code using htmx for the front end and Flask for the back end and download it as a starting point.
5. Many more dreams if I ever get this far! :)

## Installation

```bash
conda create -n htmx-ai python=3.10
conda activate htmx-ai
pip install -r requirements.txt
```

Now copy the .env.sample file to .env and add your OpenAI API key to the .env file.


## Running the server


To start the server, run the following command:

```bash
python app.py
```


Note: The server defaults to running on port 3333, if that port is already in use, you can change it in the app.py file here:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)
```
