from flask import Flask, request

import config

import time

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

@app.route("/glove/set/motors", methods = ['POST'])
def set_glove_motors():
  data = request.get_json(force=True)
  try:
    if data['point'] > 12 or data['point'] < 0:
      raise Exception("Not a valid point to toggle!")
    config.motorStatuses[data['point']] = data['state']
  except Exception as e:
    return {"success": False, 'error': str(e)}
  config.deviceStatus["glove"] = int(time.time())
  return {"success": True}

@app.route("/glove")
def get_haptic_states():
  config.deviceStatus["glove"] = int(time.time())
  return {'motors': config.motorStatuses}

@app.route("/glove/refreshrate")
def get_haptic_refresh():
  config.deviceStatus["glove"] = int(time.time())
  return {'rate': config.queryRate['gloves']}

@app.route("/glove/updateAngle")
def set_haptic_angle():
  return {"success": True}

@app.route("/glove/movement")
def set_haptic_angle():
  return {"success": True}

if __name__ == "__main__":
    app.run(host="192.168.0.100")