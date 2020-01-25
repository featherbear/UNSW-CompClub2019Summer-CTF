from lib.api import APIHandler
from lib import database
import tornado.web
import tornado.ioloop

__VERSION = "0.0.3"


app = tornado.web.Application([
    ("/api/v1/(.*)", APIHandler)
])

if database.conn is not None:
    import lib.auth

    lib.auth.initDatabase()

    import lib.authSession

    lib.authSession.initDatabase()
    lib.authSession.cleanup()

    import lib.ctf

    lib.ctf.initDatabase()

else:
    raise Exception("Cannot create the database connection.")


def run(file: str = None, **kwargs):
    print("UNSW CSE CompClub 2019 Summer CTF Server")
    print("                      [ by Andrew Wong ]")
    print("----------------------------------------")
    print("Server version:", __VERSION)

    if file:
        print("Loading config file:", file)
        import lib
        from lib.config import readConfig
        lib.config = config = readConfig(file)
    else:
        from lib.config import config

    if kwargs:
        print("Applying config overrides")
        config.update(kwargs)
    print("----------------------------------------")

    server = tornado.httpserver.HTTPServer(app)

    port = config["SERVER"].get("port", 8000)
    try:
        server.bind(port)
    except OSError:
        print("Port", port, "is in use!\nAborting...")
        return

    try:
        from os import fork
        server.start(0)
    except:
        print(":: os.fork not present on system (Windows) - Defaulting to single process")
        server.start(1)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
    print("Server running on port %s\n" % port)

else:
    import asyncio
    from tornado.platform.asyncio import AnyThreadEventLoopPolicy
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

    import tornado.wsgi
    application = tornado.wsgi.WSGIAdapter(app)
