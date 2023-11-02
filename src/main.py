import os
import sys
from typing import Any 
from peregrinegpt.gptcontext import GPTContext
from peregrinegpt.prompt import PromptJob
from peregrinegpt.pipeline import Pipeline

class InfoJob(PromptJob):
    def __init__(self, gpt: GPTContext):
        super().__init__(gpt)

    def Run(self, args: list[Any] = None) -> Any:
        return self.GPT.Prompt("user", "Sing with me. Take me down to the paradise city. ") 

class ContiguousJob(PromptJob):
    def __init__(self, gpt: GPTContext):
        super().__init__(gpt)

    def Run(self, args: list[Any] = None) -> Any:
        if (args != None):
            print(args[-1]["content"])

        self.GPT.Send(args)
        return self.GPT.Prompt("user", "continue")


def Main(args: list[str]):
    context: GPTContext = GPTContext("gpt-3.5-turbo", os.environ["OPENAI_KEY"])
    
    pipeline: Pipeline = Pipeline(context)

    pipeline.CreateJob(InfoJob)
    
    for x in range(10):
        pipeline.CreateJob(ContiguousJob)
    
    pipeline.Run(lambda err : print(err.args[0]))

    # context.LoadMessages()
    # print(json.dumps(context.Prompt("user", args[0]), indent=2))
    # context.Save()

Main(sys.argv[1:])
