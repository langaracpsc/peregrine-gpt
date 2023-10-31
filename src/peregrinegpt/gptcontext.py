import openai
import json

class GPTContext:    
    def __init__(self, model: str, apiKey: str, promptFile: str = None):
        self.Model: str = model
        self.APIKey: str = apiKey
        self.Messages: list[dict[str]] = [ ]
        openai.api_key = self.APIKey

    def LoadMessages(self, promptFile: str = "prompts.json"):
        self.PromptFile = promptFile

        with open(promptFile, "r") as fp:
            self.Messages = json.load(fp)

    def Save(self, promptFile: str = "prompts.json"): 
        try:
            with open(promptFile, "w") as fp:
                json.dump(self.Messages, fp)
                
        except:
            print("An error occured in saving messages.")
            return False

        return True

    def Prompt(self, role: str, message: str):
        self.Messages.append(dict({ "role": role, "content": message }))
        response: dict = openai.ChatCompletion.create(model=self.Model, messages=self.Messages)
        self.Messages.append(response["choices"][0]["message"])

        return self.Messages