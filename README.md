# Pure Python web server - PyProject

A blogging platform written in pure python (no web frameworks used) for developer to share their coding knowledge

## How was this web app made?

The web app is based on [WSGI](https://wsgi.readthedocs.io/en/latest/index.html) and will work perfectly with any WSGI complaint web servers.

Here's a short summary of a WSGI application:

- WSGI application are callable python objects (functions or classes with a **call** method that are passed two arguments: a WSGI environment as first argument and a function that starts the response.
- the application has to start a response using the function provided and return an iterable where each yielded item means writing and flushing.
- you can add middlewares to your application by wrapping it.

Most Python web frameworks are WSGI compatible, and use a WSGI complaint web server to call them when a request happens return its response to client.

I took some liberties to design the architecture of the project similar to that of a Flask app, and used to some essential libraries for templating, DB storage, conversion of markdown to html and sanitizing of user input.

There was a lot of research invloved as there is scarce information on this topic, I also had to implement code to manage exceptionx instead of crashing and I had to study source code of Python web frameworks, and other libraries to understand how they implemented certain things.

You can find the core code which is the backbone of the app in the folders `pyproject/lib`, `pyproject/errors`.

## How to run this project

1. Clone the project

```sh
git clone https://github.com/SrikarKSV/pure-python-server.git
```

2. Install all the dependencies

```sh
pip install -r requirements.txt
```

3. Fill the environment variables in a .env file, you can find the example in .env.example

4. Use gunicorn server to start the application

```sh
gunicorn -w 4 main:app
```

5. If you don't want make an instance of database, don't mention DATABASE_URI in .env file and the app will create a sqlite db with the table automatically

> **_NOTE_** ⚠: If your computer has an error when running gunicorn, you can directly run the python file main.py and it will spin up a WSGI server from python standard library (But it's really slow)

### Libraries used in the app

1. Jinja2
2. Python-Markdown
3. SQLAlchemy
4. bleach
5. python-dotenv (For development)

The goals of the project:

- Understand how python web servers works under the hood
- Connect the small pieces that frameworks takes care of
- Study the source code of these frameworks to imitate their functionality

**NOT** the goals of the project:

- To create the entire functionality of a python web framework
- To create every functionality from scratch
- To not use a single external package

### Todos:

- [x] Create a routing system
- [x] Use Jinja templating language to render html
- [x] Serve static files
- [x] Parse both GET and POST requests form
- [x] A page which shows all the articles
- [x] A form page to add new articles
- [x] Use markdown for article content
- [x] Update and delete articles
- [x] Style with CSS
- [x] Add meta tags
