
from flask import Flask, render_template, jsonify
#import requests
import PyATEMMax
from visca_over_ip import Camera
#import websocket
#from pyATEM import ATEM
#from pyATEM.const import VideoSource

app = Flask(__name__)

ATEM_IP = "192.168.1.91"  # Replace with the IP address of your ATEM switcher

# Rear, Front, Altar
PTZ_CAMERAS = [
    {"IP": "192.168.1.71", "CamNum": 1},
    {"IP": "192.168.1.73", "CamNum": 2},
    {"IP": "192.168.1.72", "CamNum": 3}
]

SCENES = [
    {"Camera" : PTZ_CAMERAS[0], "PRESET" : 0, "PRESENTATION" : 1, "NAME" : "Main"}, # Main
    {"Camera" : PTZ_CAMERAS[0], "PRESET" : 4, "PRESENTATION" : 2, "NAME" : "Sermon"}, # Sermon
    {"Camera" : PTZ_CAMERAS[2], "PRESET" : 0, "PRESENTATION" : 1, "NAME" : "Altar"}, # Altar
    {"Camera" : PTZ_CAMERAS[0], "PRESET" : 3, "PRESENTATION" : 1, "NAME" : "Reading"}, # Reading
    {"Camera" : PTZ_CAMERAS[1], "PRESET" : 0, "PRESENTATION" : 1, "NAME" : "Front"}, # Front
    {"Camera" : PTZ_CAMERAS[0], "PRESET" : 3, "PRESENTATION" : 0, "NAME" : "Reading/Sermon No Presenter"} # Reading/Sermon No Presenter
]

@app.route('/')
def index():
    return render_template('index.html')

active_ptz_scene = None

@app.route('/control_ptz_and_switch_scene/<int:scene_number>')
def control_ptz_and_switch_scene(scene_number):
     global active_ptz_scene
     scene = SCENES[scene_number]
     ptz_camera = scene["Camera"]
     call_ptz_preset(ptz_camera["IP"], scene["PRESET"])
     atem_control(ptz_camera["CamNum"], scene["PRESENTATION"]) # add present.
     
     active_ptz_scene = scene_number
     response_data = {
            "success": True,
            "message": f"Preset {scene['NAME']} set on PTZ camera at {ptz_camera['IP']}. {scene['PRESENTATION']} present. mode." # Switched to {scene_index} on ATEM switcher."
        }
     #return f"Preset {camera_preset} set on PTZ camera at {ptz_camera['IP']}. Switched to {scene_index} on ATEM switcher."
     return jsonify(response_data)
    





def call_ptz_preset(ptz_ip, preset_number):
    visca_controller = Camera(ptz_ip)
    visca_controller.recall_preset(preset_number)
    visca_controller.close_connection()

    #end, ignore all the junk below lol
    # Replace with the camera's port number
    #camera_port = 5678

    # Create a TCP socket connection
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect((ptz_ip, camera_port))
    #command = bytes([0x80, 0x01, 0x04, 0x3F, 0x02, preset_number, 0xFF])
    #visca_controller._send_command(command)
    # Send the preset command to the camera
    #preset_command = "01 04 3F 02 0"  + str(preset_number) + " FF"
    #sock.sendall(preset_command.encode())

    # Close the connection
    #sock.close()





def atem_control(scene_index, presenter):
    atem = PyATEMMax.ATEMMax()
    atem.connect(ATEM_IP)
    atem.waitForConnection()
    atem.setPreviewInputVideoSource("mixEffect1", scene_index)
    
    if presenter == 1 and atem.switcher.keyer["mixEffect1"]["keyer1"].onAir.enabled == False:
        atem.setKeyerOnAirEnabled("mixEffect1","keyer1",True)
        atem.setKeyerOnAirEnabled("mixEffect1","keyer2",False)
    if presenter == 2 and atem.switcher.keyer["mixEffect1"]["keyer2"].onAir.enabled == False:
        atem.setKeyerOnAirEnabled("mixEffect1","keyer2",True)
        atem.setKeyerOnAirEnabled("mixEffect1","keyer1",False)
    if presenter == 0:
        atem.setKeyerOnAirEnabled("mixEffect1","keyer2",False)
        atem.setKeyerOnAirEnabled("mixEffect1","keyer1",False)
    
    atem.execAutoME("mixEffect1")

    
    
    
    atem.disconnect()






@app.route('/start_streaming')
def start_streaming():
    # Add code here to trigger streaming from OBS
    # You might need to use a specific OBS WebSockets API or other methods
    # For simplicity, a placeholder message is returned in this example.
    
    response_data = {
            "success": True,
            "message": f"Started streaming from OBS!"
        }

    #return "Started streaming from OBS!"
    return jsonify(response_data)

@app.route('/stop_streaming')
def stop_streaming():
    # Add code here to trigger streaming from OBS
    # You might need to use a specific OBS WebSockets API or other methods
    # For simplicity, a placeholder message is returned in this example.
    
    response_data = {
            "success": True,
            "message": f"Stopped streaming from OBS!"
        }

    #return "Started streaming from OBS!"
    return jsonify(response_data)


@app.route('/start_recording')
def start_recording():
    # Add code here to trigger streaming from OBS
    # You might need to use a specific OBS WebSockets API or other methods
    # For simplicity, a placeholder message is returned in this example.
    
    response_data = {
            "success": True,
            "message": f"Started recording from OBS!"
        }

    #return "Started streaming from OBS!"
    return jsonify(response_data)

@app.route('/stop_recording')
def stop_recording():
    # Add code here to trigger streaming from OBS
    # You might need to use a specific OBS WebSockets API or other methods
    # For simplicity, a placeholder message is returned in this example.
    
    response_data = {
            "success": True,
            "message": f"Stopped recording from OBS!"
        }

    #return "Started streaming from OBS!"
    return jsonify(response_data)



""" server_address = "ws://192.168.1.169"
password = "nlbJf4Y7xnn7u2fg"
def send_obs_request(request_type):
  ws = websocket.WebSocket()
  ws.connect(server_address)

  # Authentication if password is set
  if password:
      ws.send(f"Authenticate: {password}")
      response = ws.recv()
      if response != "Authentication successful":
          print("Authentication failed!")
          return

  # Send request based on type
  if request_type == "start_stream":
      ws.send({"request-type": "StartStreaming"})
  elif request_type == "stop_stream":
      ws.send({"request-type": "StopStreaming"})
  elif request_type == "start_recording":
      ws.send({"request-type": "StartRecording"})
  elif request_type == "stop_recording":
      ws.send({"request-type": "StopRecording"})
  else:
      print(f"Invalid request type: {request_type}")
      return

  response = ws.recv()
  print(f"OBS response: {response}")
  ws.close() """




if __name__ == '__main__':
    #print("trying out")
    #call_ptz_preset("192.168.1.71", 0)
    #atem_control(1,2)
    app.run(host='0.0.0.0', port=5000)













