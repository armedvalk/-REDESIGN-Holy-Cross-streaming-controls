from flask import Flask, render_template, request, jsonify
import obsws_python as obs

app = Flask(__name__)

# OBS WebSocket connection details
OBS_HOST = 'localhost'
OBS_PORT = 4455
OBS_PASSWORD = 'nIbf4Y7xnn7u2fg'
# Replace with your OBS WebSocket password

try:
    obs_client = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
    print("Connected to OBS!")
except Exception as e:
    print(f"Could not connect to OBS: {e}")
    obs_client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    if obs_client is None:
        return jsonify({'status': 'error', 'message': 'Not connected to OBS'}), 500

    data = request.get_json()
    action = data.get('action')

    try:
        if action == 'start_streaming':
            obs_client.start_streaming()
            return jsonify({'status': 'success', 'message': 'Started streaming'})
        elif action == 'stop_streaming':
            obs_client.stop_streaming()
            return jsonify({'status': 'success', 'message': 'Stopped streaming'})
        elif action == 'start_recording':
            obs_client.start_recording()
            return jsonify({'status': 'success', 'message': 'Started recording'})
        elif action == 'stop_recording':
            obs_client.stop_recording()
            return jsonify({'status': 'success', 'message': 'Stopped recording'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid action'}), 400
    except Exception as e:
        print(f"OBS Control Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

