import openai

class GPTContext:    
    def __init__(self, model: str, apiKey: str):
        self.Model: str = model
        self.APIKey: str = apiKey
        self.Messages: list[dict[str]] = [ ]
        openai.api_key = self.APIKey

    def Prompt(self, role: str, message: str):
        self.Messages.append(dict({ "role": role, "content": message }))
        response: dict = openai.ChatCompletion.create(model=self.Model, messages=self.Messages)
        self.Messages.append(response["choices"][0]["message"])
        return self.Messages