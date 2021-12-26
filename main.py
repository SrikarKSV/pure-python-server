import os
from wsgiref import simple_server

from dotenv import load_dotenv
from sqlalchemy.inspection import inspect

from pyproject import app
from pyproject.errors.ExceptionMiddleware import ExceptionMiddleware
from pyproject.models import Base, engine

if __name__ == "__main__":
    load_dotenv()  # Loads environment variables from .env file

    # If table don't exist, Create.
    if not inspect(engine).has_table("posts"):
        Base.metadata.tables["posts"].create(engine)

    PORT = int(os.getenv("PORT", 3000))
    app = ExceptionMiddleware(app)
    httpd = simple_server.make_server("", PORT, app)
    print(f"✅ Listening on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        httpd.server_close()
