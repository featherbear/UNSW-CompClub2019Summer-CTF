from lib.api import APIHandler
from lib import database
import tornado.web
import tornado.ioloop

try:
    import git
    repo = git.Repo(search_parent_directories=True)
    __VERSION = repo.head.object.hexsha[:7]
except:
    __VERSION = "UNKNOWN"

app = tornado.web.Application([
    ("/api/v2/(.*)", APIHandler)
])

if database.conn is not None:
    import lib.auth

    lib.auth.initDatabase()

    import lib.authSession

    lib.authSession.initDatabase()
    # lib.authSession.cleanup()

    import lib.ctf

    lib.ctf.initDatabase()

else:
    raise Exception("Cannot create the database connection.")


def run(file: str = None, **kwargs):
    print("==============================")
    print("= CTF Service by Andrew Wong =")
    print("=                            =")
    print(f"=            version {__VERSION} =")
    print("==============================")
    print()

    if file:
        print("Loading config file:", file)
        import lib
        from lib.config import readConfig
        lib.config = config = readConfig(file)
    else:
        from lib.config import config

    if kwargs:
        print("Applying configuration overrides")
        config.update(kwargs)

    server = tornado.httpserver.HTTPServer(app)

    port = config["SERVER"].get("port", 8000)
    try:
        server.bind(port)
    except OSError:
        print("Port", port, "is in use!\nAborting...")
        return

    print("Starting server on port %s\n" % port)

    try:
        # TODO: Check if behaviour happens on Windows
        
        # Try to import fork, if an exception is raised, then the OS does not have os.fork
        from os import fork


        server.start(0)
    except:
        print(":: os.fork not present on system (Windows) - Defaulting to single process")
        server.start(1)

    

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()

else:
    import asyncio
    from tornado.platform.asyncio import AnyThreadEventLoopPolicy
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

    import tornado.wsgi
    application = tornado.wsgi.WSGIAdapter(app)
