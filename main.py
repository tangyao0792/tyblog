try:
    import db
    import os
    from handlers import *
    import base64
    import uuid
    from pocket import *
#    from neugpa import NeugpaHandler
#    from grid import GridHandler
#    from notepad import NotepadHandler
    import tornado.web
    import tornado.httpserver
    import tornado.ioloop
    import tornado.options
    from tornado.options import define, options
    define("port", default=8000, help="run on the given port", type=int)
except Exception as e:
    print e
    pass


settings = {
    "cookie_secret": "iamtangyao",
    "login_url": "/login",
}

handlers=[
    (r"/", IndexHandler),
    (r"/neugpa", NeugpaHandler),                        # neugpa
    (r"/grid", GridHandler),                            # grid, copied from m67
    (r"/pad(.*)", NotepadHandler),                      # a small pad, copied from notepad.cc
    (r"/test", TestHandler),                            # for test
    (r"/googleafa84db2e7d78f11.html", GoogleHandler),   # google verification
    (r"/NewPost", NewPostHandler),
    (r"/post/(\d+\-\d+\-\d+\/[^/]+)", PostHandler),
    (r"/catagory/(.*)", CatagoryHandler),
    (r"/archives(.*)", ArchivesHandler),
    (r"/login", LoginHandler),
    (r"/admin(.*)", AdminMainHandler),
    (r"/about", AboutHandler),
    (r"/edit(.*)", EditPostHandler),
    (
        r"/favicon.ico",
        tornado.web.StaticFileHandler,
        os.path.join(os.path.dirname(__file__),
        "static")
    )
]
template_path=os.path.join(os.path.dirname(__file__), 'templates')
static_path=os.path.join(os.path.dirname(__file__), 'static')

if __name__ == "__main__":

    try:
        app = tornado.web.Application(
            handlers=handlers,
            template_path=template_path,
            static_path=static_path,
            **settings
        )
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        print e
        pass
 


