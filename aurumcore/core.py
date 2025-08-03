import os
import json
import time
import threading
from dotenv import load_dotenv
from .obs_integration import OBSController
from .ai_models import BehaviorModel, ModerationModel
from .twitch_integration import TwitchChatListener
from .web_interface import run_web_server

class AurumCore:
    def __init__(self, config_path="config/default.json"):
        load_dotenv()
        self.config = self.load_config(config_path)
        self.obs = OBSController(
            os.getenv('OBS_HOST', 'localhost'),
            os.getenv('OBS_PORT', 4444),
            os.getenv('OBS_PASSWORD', 'aurum2024')
        )
        self.behavior_model = BehaviorModel()
        self.moderation_model = ModerationModel()
        self.running = False
        self.profile = self.load_profile()
        
    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {
                "learning_rate": 0.001,
                "update_interval": 300
            }
    
    def load_profile(self):
        profile_path = "config/streamer_profile.json"
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                return json.load(f)
        return {
            "communication_style": {"formal": 0.5, "humorous": 0.3, "technical": 0.2},
            "moderation_preferences": {"strictness": 0.7}
        }
    
    def save_profile(self):
        with open("config/streamer_profile.json", 'w') as f:
            json.dump(self.profile, f)
    
    def start(self):
        if self.running:
            return
            
        self.running = True
        print("Starting AurumCore...")
        
        # Conectar ao OBS
        if not self.obs.connect():
            print("OBS connection failed")
        
        # Iniciar modelos de IA
        self.behavior_model.load()
        self.moderation_model.load()
        
        # Iniciar listener do Twitch
        self.twitch_listener = TwitchChatListener(
            os.getenv('TWITCH_CHANNEL'),
            os.getenv('TWITCH_TOKEN')
        )
        self.twitch_listener.start(self.handle_message)
        
        # Iniciar servidor web
        web_thread = threading.Thread(target=run_web_server, args=(self,))
        web_thread.daemon = True
        web_thread.start()
        
        # Thread de aprendizado contínuo
        learning_thread = threading.Thread(target=self.continuous_learning)
        learning_thread.daemon = True
        learning_thread.start()
        
        print("AurumCore started successfully!")
    
    def handle_message(self, user, message):
        # Análise de moderação
        toxicity = self.moderation_model.predict(message)
        if toxicity > self.profile["moderation_preferences"]["strictness"]:
            print(f"Moderating message from {user}: {message}")
            self.obs.show_overlay(f"Moderated: {user}")
            # Aqui você pode adicionar ação como timeout/ban
            
        # Aprendizado do comportamento
        self.behavior_model.adapt(message, self.profile)
    
    def continuous_learning(self):
        while self.running:
            try:
                # Atualizar modelos periodicamente
                self.behavior_model.update()
                self.save_profile()
                time.sleep(self.config["update_interval"])
            except Exception as e:
                print(f"Learning error: {str(e)}")
    
    def process_voice_command(self, command):
        response = self.behavior_model.generate_response(command)
        print(f"Voice command: {command} -> Response: {response}")
        # Implementar ações com base no comando
        if "mudar cena" in command.lower():
            scene = command.split("para")[-1].strip()
            self.obs.switch_scene(scene)
            return f"Mudando para cena: {scene}"
        return response

if __name__ == "__main__":
    aurum = AurumCore()
    aurum.start()
    
    try:
        while aurum.running:
            time.sleep(1)
    except KeyboardInterrupt:
        aurum.running = False
        print("Stopping AurumCore...")
