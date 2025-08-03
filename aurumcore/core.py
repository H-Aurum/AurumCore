import os
import json
import time
import threading
import logging
from dotenv import load_dotenv
from .obs_integration import OBSController
from .ai_models import BehaviorModel, ModerationModel
from .twitch_integration import TwitchChatListener
from .web_interface import run_web_server

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("aurumcore.log")
    ]
)

class AurumCore:
    def __init__(self, config_path="config/default.json"):
        self.logger = logging.getLogger('core')
        self.logger.info("Initializing AurumCore...")
        
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
        self.twitch_active = False
        self.ai_loaded = False
        self.profile = self.load_profile()
        
    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                self.logger.info(f"Loaded config from {path}")
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Config load error: {str(e)}. Using defaults.")
            return {
                "learning_rate": 0.001,
                "update_interval": 300,
                "min_toxicity": 0.7
            }
    
    def load_profile(self):
        profile_path = "config/streamer_profile.json"
        try:
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as f:
                    profile = json.load(f)
                    self.logger.info("Loaded streamer profile")
                    return profile
        except Exception as e:
            self.logger.error(f"Profile load error: {str(e)}")
            
        self.logger.info("Created new streamer profile")
        return {
            "communication_style": {"formal": 0.5, "humorous": 0.3, "technical": 0.2},
            "moderation_preferences": {"strictness": 0.7},
            "blocked_words": []
        }
    
    def save_profile(self):
        try:
            with open("config/streamer_profile.json", 'w') as f:
                json.dump(self.profile, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Profile save error: {str(e)}")
            return False
    
    def start(self):
        if self.running:
            return
            
        self.logger.info("Starting AurumCore services...")
        self.running = True
        
        # Conectar ao OBS
        if not self.obs.connect():
            self.logger.error("Failed to connect to OBS")
        
        # Carregar modelos de IA
        self.ai_loaded = self.behavior_model.load() and self.moderation_model.load()
        if not self.ai_loaded:
            self.logger.warning("Some AI models failed to load")
        
        # Iniciar listener do Twitch
        twitch_token = os.getenv('TWITCH_TOKEN')
        twitch_channel = os.getenv('TWITCH_CHANNEL')
        
        if twitch_token and twitch_channel:
            self.twitch_listener = TwitchChatListener(
                token=twitch_token,
                channel=twitch_channel,
                callback=self.handle_message
            )
            self.twitch_active = self.twitch_listener.start_listener()
        else:
            self.logger.warning("Twitch credentials not configured")
        
        # Iniciar servidor web
        run_web_server(self)
        
        # Thread de aprendizado contínuo
        learning_thread = threading.Thread(target=self.continuous_learning)
        learning_thread.daemon = True
        learning_thread.start()
        
        self.logger.info("AurumCore started successfully")
    
    def handle_message(self, message_data):
        try:
            user = message_data['user']
            message = message_data['message']
            
            # Análise de moderação
            toxicity = self.moderation_model.predict(message)
            min_toxicity = self.config.get('min_toxicity', 0.7)
            
            if toxicity > min_toxicity:
                self.logger.info(f"Moderating toxic message ({toxicity:.2f}) from {user}: {message}")
                self.obs.show_overlay(f"Moderado: {user}", duration=3)
                # Aqui você pode adicionar ação como timeout/ban
                
            # Aprendizado do comportamento
            self.behavior_model.adapt(message, self.profile)
        except Exception as e:
            self.logger.error(f"Message handling error: {str(e)}")
    
    def continuous_learning(self):
        self.logger.info("Continuous learning started")
        while self.running:
            try:
                time.sleep(self.config["update_interval"])
                self.save_profile()
            except Exception as e:
                self.logger.error(f"Learning error: {str(e)}")
    
    def process_voice_command(self, command):
        try:
            if not command.strip():
                return "Comando não reconhecido"
                
            response = self.behavior_model.generate_response(
                command, 
                self.profile
            )
            self.logger.info(f"Voice command: '{command}' -> Response: '{response}'")
            return response
        except Exception as e:
            self.logger.error(f"Voice command error: {str(e)}")
            return "Erro no processamento do comando"

    def stop(self):
        self.logger.info("Stopping AurumCore...")
        self.running = False
        self.obs.disconnect()
        self.logger.info("AurumCore stopped")

if __name__ == "__main__":
    aurum = AurumCore()
    try:
        aurum.start()
        while aurum.running:
            time.sleep(1)
    except KeyboardInterrupt:
        aurum.stop()
