This is the repo for the Hamburg Python Pizza 2023 talk

# Choose HTMX and avoid learning too much JavaScript.

This is a FastAPI project that shows you some of the basics of HTMX and how to serve it from FastAPI.

The example shows:
- login (with error message)
- detecting on the backend if htmx is used
- how to set a session id (Javascript)
- how to serve a dashboard via SSE (Server Sent Events)
- serving to out of bound elements


Check out https://htmx.org/ for documentation.

👉 Slides are in the slides folder

## Installation

Create new new virtual environment:
`python3 -m venv venv` or on Windows `py -3 -m venv venv`

Activate it
`source venv/bin/activate` or on Windows `venv\Scripts\activate`

Install the requirements
`python -m pip install -r requirements.txt`


## Running the program

Move into the `app` folder
`cd app`

Start the program
`python main.py`

The user logins are on top of the `fake_backend.py` file, for example user `a@b.c`, password `d`

