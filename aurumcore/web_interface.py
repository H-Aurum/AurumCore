from flask import Flask, render_template, request, jsonify
import threading
import logging

app = Flask(__name__)
aurum_core = None
logger = logging.getLogger('web_interface')

def run_web_server(core_instance, host='0.0.0.0', port=5000):
    global aurum_core
    aurum_core = core_instance
    
    # Desativar logging do Flask em produção
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    threading.Thread(target=lambda: app.run(
        host=host, 
        port=port,
        debug=False,
        use_reloader=False
    )).start()
    
    logger.info(f"Web interface running at http://{host}:{port}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obs/switch_scene', methods=['GET'])
def switch_scene():
    scene = request.args.get('scene')
    if aurum_core.obs.switch_scene(scene):
        return jsonify(success=True, message=f"Cena alterada para: {scene}")
    return jsonify(success=False, message="Falha ao mudar de cena")

@app.route('/obs/toggle_source', methods=['GET'])
def toggle_source():
    source = request.args.get('source')
    if aurum_core.obs.toggle_source(source):
        return jsonify(success=True, message=f"Fonte '{source}' alternada")
    return jsonify(success=False, message=f"Falha ao alternar fonte '{source}'")

@app.route('/voice_command', methods=['POST'])
def voice_command():
    try:
        data = request.json
        command = data.get('command', '')
        if command:
            response = aurum_core.process_voice_command(command)
            return jsonify(success=True, response=response)
        return jsonify(success=False, response="Comando vazio")
    except Exception as e:
        logger.error(f"Voice command error: {str(e)}")
        return jsonify(success=False, response="Erro no processamento")

@app.route('/system/status', methods=['GET'])
def system_status():
    return jsonify({
        "obs_connected": aurum_core.obs.connected,
        "twitch_active": aurum_core.twitch_active,
        "ai_loaded": aurum_core.ai_loaded,
        "profile": aurum_core.profile
    })
