import subprocess
import threading
from server import Server
from flask import Flask
from flask import send_file
from flask import jsonify
from flask import request

s = Server()
app = Flask(__name__)
@app.route("/")
def index():
    return send_file("fronted/index.html")

@app.route("/log")
def log():
    log_ = s.log_r()
    if log_:
        return log_
    return  "null"

@app.route("/start")
def start():
    return s.start()

@app.route("/stop")
def stop():
    return s.stop()

@app.route("/cmd")
def cmd():
    cmd = request.args.get("cmd")
    return s.command(cmd)

@app.route("/kill")
def kill():
    return s.kill()

app.run()