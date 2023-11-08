import json
from peregrinegpt.gptcontext import GPTContext

class ChatBot:
    def __init__(self, promptFile: str, gpt: GPTContext) -> None:
        self.Prompts: list[dict[str, str]] = []
        self.GPT: GPTContext = gpt
        self.IsRunning: bool = False
        self.Prompts: list[dict[str, str]] = []

        with open(promptFile, 'r') as fp:
            self.Prompts = json.load(fp)

    def Initialize(self):
        self.GPT.Messages = self.Prompts
        self.GPT.Update()

    def Run(self):
        pass 
