import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class BehaviorModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.response_templates = {
            "formal": "Compreendo sua solicitação. Vou executar: {command}",
            "humorous": "Haha, claro! Fazendo: {command} com estilo!",
            "technical": "Executando comando: {command}. Status: OK"
        }
        
    def load(self, model_name="neuralmind/bert-base-portuguese-cased"):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            print("Behavior model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading behavior model: {str(e)}")
            self.model = None
            return False
    
    def adapt(self, message, profile):
        if "humor" in message.lower() or "risada" in message.lower() or "haha" in message.lower():
            profile["communication_style"]["humorous"] = min(1.0, profile["communication_style"]["humorous"] + 0.05)
        elif "tecnologia" in message.lower() or "pc" in message.lower() or "hardware" in message.lower():
            profile["communication_style"]["technical"] = min(1.0, profile["communication_style"]["technical"] + 0.05)
        elif "obrigado" in message.lower() or "por favor" in message.lower():
            profile["communication_style"]["formal"] = min(1.0, profile["communication_style"]["formal"] + 0.05)
        return profile
    
    def generate_response(self, command, profile):
        if not self.model:
            return "Sistema pronto para executar comandos."
        
        # Determinar estilo predominante
        styles = profile["communication_style"]
        predominant_style = max(styles, key=styles.get)
        
        # Selecionar template apropriado
        template = self.response_templates.get(predominant_style, self.response_templates["formal"])
        
        # Respostas baseadas em comandos específicos
        if "mudar cena" in command.lower():
            scene = command.split("para")[-1].strip() if "para" in command else "cena solicitada"
            return template.format(command=f"Mudando para cena: {scene}")
            
        elif "microfone" in command.lower():
            action = "desativar" if "desativar" in command.lower() else "ativar"
            return template.format(command=f"Microfone {action}do")
            
        elif "iniciar" in command.lower() and "stream" in command.lower():
            return template.format(command="Iniciando transmissão")
            
        return template.format(command=command)

class ModerationModel:
    def __init__(self):
        self.classifier = None
        
    def load(self, model_name="portuguese-bert-toxicity"):
        try:
            self.classifier = pipeline(
                "text-classification", 
                model=model_name,
                tokenizer=model_name
            )
            print("Moderation model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading moderation model: {str(e)}")
            self.classifier = None
            return False
    
    def predict(self, text):
        if not text.strip():
            return 0.0
            
        if self.classifier:
            try:
                result = self.classifier(text)[0]
                return result['score'] if result['label'] == 'toxic' else 0
            except:
                pass
                
        # Fallback para palavras-chave
        toxic_keywords = [
            "idiota", "burro", "lixo", "merda", "vsf", "fdp", "porra",
            "bosta", "retardado", "imbecil", "estúpido", "nojento"
        ]
        
        # Contagem de palavras tóxicas
        toxic_count = sum(1 for word in toxic_keywords if word in text.lower())
        
        # Calcula score baseado na contagem
        return min(1.0, toxic_count * 0.3)
