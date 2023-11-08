import json
from peregrinegpt.gptcontext import GPTContext

class ChatBot:
    def __init__(self, promptFile: str, gpt: GPTContext) -> None:
        self.Prompts: list[dict[str, str]] = []
        self.GPT = gpt
        
        with open(promptFile, 'r') as fp:
            self.Prompts = json.load(fp)
    
    def Initialize(self):
        for prompt in self.Prompts:
            self.GPT.AddPrompt(prompt)
        self.GPT.Update()

    def Run(self):
        pass