from flask import Flask, request

import config
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

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
    "readable_height": f"{int((config.userHeight - (config.userHeight % 12))/12)}ft, {(config.userHeight % 12)}in",
    "hud_enabled": config.HUDMode
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
  config.deviceStatus["frontend"] = int(time.time())
  return config.deviceStatus

@app.route("/sensorData")
def get_sensor_information():
  return {"handAngles": config.handAngles, "headAngles": config.headAngles}

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

@app.route("/glove/updateAngle", methods = ['POST'])
def set_haptic_angle():
  data = request.get_json(force=True)
  config.handAngles['pitch'] = data['pitch'] * 180 / 3.1415
  config.handAngles['roll'] = data['roll'] * 180 / 3.1415
  return {"success": True}

@app.route("/glove/movement", methods = ['POST'])
def receive_haptic_movement():
  data = request.get_json(force=True)
  print(data)
  if data["move"] == "x":
    config.HUDMode = not config.HUDMode
  return {"success": True}

@app.route("/glasses/refreshrate")
def get_glasses_refresh():
  config.deviceStatus["headset"] = int(time.time())
  return {'rate': config.queryRate['headset']}

@app.route("/glasses")
def get_glasses_state():
  config.deviceStatus["headset"] = int(time.time())
  returnDict = {"left": {
    "text": [],
    "rect": [],
    "circ": []
  }, "right": {
    "text": [],
    "rect": [],
    "circ": []
  }}
  if config.HUDMode:
    returnDict["left"]["text"].append([0, 12, config.username])
    returnDict["left"]["text"].append([0, 50, ":D"])
    returnDict["right"]["text"].append([0, 12, config.username])

    returnDict["right"]["rect"].append([40, 40, 20, 30])
  return returnDict

@app.route("/glasses/updateAngle", methods = ['POST'])
def set_glasses_angle():
  data = request.get_json(force=True)
  config.headAngles['yaw'] = data['yaw'] * 180 / 3.1415
  config.headAngles['roll'] = data['roll'] * 180 / 3.1415
  return {"success": True}

if __name__ == "__main__":
    app.run(host="192.168.0.100")