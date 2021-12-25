import os
from wsgiref import simple_server

from dotenv import load_dotenv

from pyproject import app

if __name__ == "__main__":
    load_dotenv()  # Loads environment variables from .env file
    PORT = int(os.getenv("PORT", 3000))
    httpd = simple_server.make_server("", PORT, app)
    print(f"✅ Listening on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        httpd.server_close()
