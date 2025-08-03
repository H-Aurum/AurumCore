import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

class BehaviorModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        
    def load(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
            self.model = AutoModelForSequenceClassification.from_pretrained("neuralmind/bert-base-portuguese-cased")
            print("Behavior model loaded successfully")
        except Exception as e:
            print(f"Error loading behavior model: {str(e)}")
            self.model = None
    
    def adapt(self, message, profile):
        # Implementação simplificada para demonstração
        if "humor" in message.lower():
            profile["communication_style"]["humorous"] = min(1.0, profile["communication_style"]["humorous"] + 0.05)
        elif "tecnologia" in message.lower():
            profile["communication_style"]["technical"] = min(1.0, profile["communication_style"]["technical"] + 0.05)
        return profile
    
    def generate_response(self, command):
        # Respostas básicas para demonstração
        responses = {
            "mudar cena": "Cena alterada com sucesso!",
            "desligar microfone": "Microfone desativado",
            "iniciar stream": "Transmissão iniciada"
        }
        
        for key, response in responses.items():
            if key in command.lower():
                return response
        return "Comando executado com sucesso!"

class ModerationModel:
    def __init__(self):
        self.classifier = None
        
    def load(self):
        try:
            self.classifier = pipeline(
                "text-classification", 
                model="portuguese-bert-toxicity",
                tokenizer="portuguese-bert-toxicity"
            )
            print("Moderation model loaded successfully")
        except:
            print("Using fallback moderation")
            self.classifier = None
    
    def predict(self, text):
        if self.classifier:
            result = self.classifier(text)[0]
            return result['score'] if result['label'] == 'toxic' else 0
        # Fallback simples
        toxic_keywords = ["idiota", "burro", "lixo", "merda"]
        return 0.8 if any(word in text.lower() for word in toxic_keywords) else 0.1
