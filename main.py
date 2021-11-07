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
  data = request.get_json(force=True)
  try:
    config.username = data["username"]
  except:
    return {"success": False}
  return {"success": True}

@app.route("/user/set/height", methods = ['POST'])
def set_height():
  data = request.get_json(force=True)
  try:
    config.userHeight = data["height"]
  except:
    return {"success": False}
  return {"success": True}

@app.route("/status/set", methods = ['POST'])
def set_device_status():
  data = request.get_json(force=True)
  try:
    if data['device'] not in config.deviceStatus:
      raise Exception("Not a valid device!")
    config.deviceStatus[data['device']] = data['state']
  except Exception as e:
    return {"success": False, 'error': str(e)}
  return {"success": True}

@app.route("/status")
def get_devices():
  return config.deviceStatus


if __name__ == "__main__":
    app.run()