from flask.helpers import url_for
from flask.templating import render_template
from flask import request, redirect

__authors__ = ["shawkins", "Tsintsir", "sonph", "LeBat"]  # add yourself!

# internal (project libs)
from config import PORT_NUM, arg_parser

# base (python packages)
import sys

# external (pip packages)
from flask import Flask
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop

app = Flask(__name__)


@app.route('/settings/ssh/')
def ssh_management():
    key = request.args.get("key", False)
    return render_template("settings/ssh.html", key=key)


@app.route('/settings/ssh/new/', methods=["GET", "POST"])
def new_ssh():
    if request.method == "POST":
        key_name = request.form["key_name"]
        key_contents = request.form["pubkey_contents"]
        key_accepted = True  # TODO: this
        if key_accepted:
            return redirect(url_for("ssh_management", key=key_name))
        else:
            error_message = "[not implemented]"
            return render_template("settings/new_ssh.html", error_toast=error_message)
    return render_template("settings/new_ssh.html")


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/my_var=<var>/')
def hello_var(var):
    return render_template("hello_var.html", var=var)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    # Parse arguments
    args = arg_parser.parse_args()
    # If we got a port_num config from args, override with that
    if args.port_num is not None:
        PORT_NUM = args.port_num
    PORT_NUM = int(PORT_NUM)
    # set up WSGI/tornado magic
    wsgi_container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(wsgi_container)
    http_server.listen(PORT_NUM)

    sys.stderr.write('Listening on port %d\n' % PORT_NUM)

    # this blocks the thread, don't do anything after this!
    tornado.ioloop.IOLoop.instance().start()
