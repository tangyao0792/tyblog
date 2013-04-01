import tornado.wsgi
import sae
from neugpa import NeugpaHandler
import os
import tornado.web
import db
import os
from handlers import *
import base64
import uuid
from main import settings, handlers, template_path, static_path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


app = tornado.wsgi.WSGIApplication(
    handlers=handlers,
    template_path=template_path,
    static_path=template_path,
    **settings
)

application = sae.create_wsgi_app(app)
