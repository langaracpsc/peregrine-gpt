import os
import sys
from peregrinegpt.chatbot import ChatBot
from peregrinegpt.gptcontext import GPTContext

class RegistrationBot(ChatBot):
    def __init__(self, promptFile: str, gpt: GPTContext) -> None:
        super().__init__(promptFile, gpt)
    def Run(self):
        self.IsRunning = True
        while (self.IsRunning):
            prompt = input("> ")
            
            if (prompt == "exit"):
                self.IsRunning = False
            
            self.GPT.Prompt("user", prompt)

            print(self.GPT.Messages[-1])

reg = RegistrationBot(sys.argv[1], GPTContext("gpt-3.5-turbo-16k", os.getenv("OPENAI_KEY")))

reg.Initialize()
reg.Run()


