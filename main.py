from flask import Flask, request

import config

app = Flask(__name__)

@app.route("/")
def get_running():
    return {
      "running": True
    }

@app.route("/user/get")
def get_user():
  return {
    "username": config.username,
    "height": config.userHeight,
    "readable_height": f"{int((config.userHeight - (config.userHeight % 12))/12)}ft, {(config.userHeight % 12)}in"
  }

@app.route("/user/set/username", methods = ['POST'])
def set_username():
  config.username = request.form['username']

if __name__ == "__main__":
    app.run()