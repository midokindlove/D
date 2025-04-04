import requests

class DeepSeekAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"  # تأكد من الرابط الصحيح
    
    def ask_question(self, question):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",  # أو أي نموذج آخر
            "messages": [{"role": "user", "content": question}]
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
