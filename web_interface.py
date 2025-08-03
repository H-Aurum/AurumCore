from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
aurum_core = None

def run_web_server(core_instance):
    global aurum_core
    aurum_core = core_instance
    app.run(host='0.0.0.0', port=5000)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obs/switch_scene', methods=['GET'])
def switch_scene():
    scene = request.args.get('scene')
    if aurum_core.obs.switch_scene(scene):
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/voice_command', methods=['POST'])
def voice_command():
    data = request.json
    response = aurum_core.process_voice_command(data['command'])
    return jsonify(response=response)
