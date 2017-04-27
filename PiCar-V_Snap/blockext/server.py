"""A nano HTTP server."""

#from __future__ import (absolute_import, division,
#                        print_function, unicode_literals)
#from future.builtins import *
from future.utils import native

from future import standard_library
standard_library.install_hooks()
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn


try:
    from urllib import quote as _quote_str
    from urllib import unquote as _unquote_str
    def quote(part):
        return _quote_str(part.encode("utf-8"))
    def unquote(part):
        if not isinstance(part, bytes): part = part.decode("utf-8")
        return _unquote_str(part).decode("utf-8")
except ImportError:
    from urllib.parse import quote, unquote



#-- Response --#

class Response(object):
    """HTTP response headers, status, and content."""
    def __init__(self, content, status=200, **headers):
        if not isinstance(content, bytes): content = content.encode("utf-8")
        self.content = bytes(content)
        self.status = status
        defaults = dict(
            content_type="text/plain",
            content_length=str(len(self.content)),
            access_control_allow_origin="*",
        )
        defaults.update(headers)
        if "content_type" not in headers:
            headers["content_type"] = "text/plain"
        self.headers = dict((k.title().replace("_", "-"), v)
                            for (k, v) in defaults.items())

def Download(content, content_type="application/octet-stream"):
    """Response that downloads the file."""
    return Response(content, content_type=content_type,
                             content_disposition="attachment")

def Redirect(location):
    """Response that temporary-redirects to the new location."""
    return Response(location.encode("utf-8"), 302, location=location)

def NotFound():
    return Response("ERROR: Not found", 404)


#-- Server --#

def GetRequestHandlerFactory(app):
    app_ = app
    class DerivedGetRequestHandler(GetRequestHandler):
        app = app_
    return DerivedGetRequestHandler


class GetRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format_, *args):
        if args[0].startswith(native("GET /poll")):
            return
        return BaseHTTPRequestHandler.log_message(self, format_, *args)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers",
                         "X-Requested-With, X-Application")
        self.end_headers()

    def do_GET(self):
        args = self.path.split("/")
        args = list(map(unquote, args))
        assert args.pop(0) == "" # since path starts with a slash
        response = self.app.get_response(*args)

        self.send_response(response.status)
        for k, v in response.headers.items():
            self.send_header(k, str(v))
        self.end_headers()
        self.wfile.write(native(response.content))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def Server(app, host, port):
    handler = GetRequestHandlerFactory(app)
    server = ThreadedHTTPServer((host, port), handler)
    return server

