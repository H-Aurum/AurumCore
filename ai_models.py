import torch
from transformers import pipeline

class BehaviorModel:
    def __init__(self):
        self.model = None
        
    def load(self):
        try:
            self.model = pipeline('text-generation', model='pierreguillou/gpt2-small-portuguese')
            return True
        except Exception as e:
            print(f"Error loading behavior model: {str(e)}")
            return False
            
    def generate_response(self, text):
        if not self.model:
            return "Sistema offline"
        return self.model(text, max_length=50)[0]['generated_text']

class ModerationModel:
    def __init__(self):
        self.classifier = None
        
    def load(self):
        try:
            self.classifier = pipeline('text-classification', model='portuguese-bert-toxicity')
            return True
        except:
            print("Using fallback moderation")
            return False
            
    def predict(self, text):
        if self.classifier:
            result = self.classifier(text)[0]
            return result['score'] if result['label'] == 'toxic' else 0
        # Fallback simples
        toxic_keywords = ["idiota", "burro", "lixo", "merda"]
        return 0.8 if any(word in text.lower() for word in toxic_keywords) else 0.1
