import os
from wsgiref import simple_server

from dotenv import load_dotenv
load_dotenv()

def app(environ, response):
    response("200 OK", [("Content-Type", "text/plain")])
    return [b"Hello world"]


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 3000))
    httpd = simple_server.make_server("", PORT, app)
    print(f"✅ Listening on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        httpd.server_close()
