import os
import time
import threading
from dotenv import load_dotenv
from .obs_integration import OBSController
from .ai_models import BehaviorModel, ModerationModel
from .twitch_integration import TwitchChatListener
from .web_interface import run_web_server

class AurumCore:
    def __init__(self):
        load_dotenv()
        self.obs = OBSController(
            os.getenv('OBS_HOST', 'localhost'),
            os.getenv('OBS_PORT', 4444),
            os.getenv('OBS_PASSWORD', 'aurum2024')
        )
        self.behavior_model = BehaviorModel()
        self.moderation_model = ModerationModel()
        self.running = False
        self.profile = {
            "communication_style": {"formal": 0.5, "humorous": 0.3, "technical": 0.2},
            "moderation_preferences": {"strictness": 0.7}
        }
    
    def start(self):
        if self.running:
            return
            
        self.running = True
        print("Starting AurumCore...")
        
        # Conectar ao OBS
        self.obs.connect()
        
        # Carregar modelos
        self.behavior_model.load()
        self.moderation_model.load()
        
        # Iniciar Twitch
        token = os.getenv('TWITCH_TOKEN')
        channel = os.getenv('TWITCH_CHANNEL')
        if token and channel:
            self.twitch = TwitchChatListener(token, channel, self.handle_message)
            self.twitch.start()
        
        # Iniciar web server
        web_thread = threading.Thread(target=run_web_server, args=(self,))
        web_thread.daemon = True
        web_thread.start()
        
        print("AurumCore started successfully!")
    
    def handle_message(self, user, message):
        # Análise de moderação
        toxicity = self.moderation_model.predict(message)
        if toxicity > self.profile["moderation_preferences"]["strictness"]:
            print(f"Moderating message from {user}: {message}")
            self.obs.show_overlay(f"Moderated: {user}")
        
        # Aprendizado
        self.profile = self.behavior_model.adapt(message, self.profile)
    
    def process_voice_command(self, command):
        return self.behavior_model.generate_response(command)

if __name__ == "__main__":
    aurum = AurumCore()
    aurum.start()
    try:
        while aurum.running:
            time.sleep(1)
    except KeyboardInterrupt:
        aurum.running = False
