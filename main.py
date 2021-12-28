import os
from wsgiref import simple_server

from dotenv import load_dotenv

from pyproject import app
from pyproject.db import db_init
from pyproject.errors.ExceptionMiddleware import ExceptionMiddleware

load_dotenv()  # Loads environment variables from .env file
db_init()  # Initialize DB session

app = ExceptionMiddleware(app)

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 3000))
    httpd = simple_server.make_server("", PORT, app)
    print(f"✅ Listening on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        httpd.server_close()
