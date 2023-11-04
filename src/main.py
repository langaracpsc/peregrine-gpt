import os
import sys
import json
from typing import Any 
from peregrinegpt.gptcontext import GPTContext
from peregrinegpt.prompt import PromptJob
from peregrinegpt.pipeline import Pipeline

class SetupJob(PromptJob):
    def __init__(self, gpt: GPTContext):
        super().__init__(gpt)

    def Run(self, args: list[Any] = None) -> Any:
        return self.GPT.Prompt("user", "You are a lyricist, write me a line of a song.")
 
class FollowUpJob(PromptJob):
    def __init__(self, gpt: GPTContext):
        super().__init__(gpt)

    def Run(self, args: list[Any] = None) -> Any:
        print(args[-1]["content"], end="\n\n")
        
        if (len(args) >= 3):
            print(args[-3]["content"], end="\n\n")
        elif (len(args) == 2):
            print(args[-2]["content"], end="\n\n")

        self.GPT.Prompt("user", "Explain the previous line in 2 sentences.")
        print()
        return self.GPT.Prompt("user", "Write another line")
        
def RunChat(gpt: GPTContext):
    gpt.LoadMessages("registration.json")
    gpt.Send(gpt.Messages)

    prompt = input("user> ")

    while (prompt.lower() != "exit"):
        response = gpt.Prompt("user", prompt)
        print(f"gpt> {gpt.Messages[-1]['content']}")

        prompt = input("\nuser> ")
    return

def Main(args: list[str]):
    context: GPTContext = GPTContext("gpt-3.5-turbo-16k", os.environ["OPENAI_KEY"])

    # RunChat(context)

    pipeline: Pipeline = Pipeline(context)

    pipeline.CreateJob(SetupJob)

    for x in range(100):
        pipeline.CreateJob(FollowUpJob)

    pipeline.Run(lambda err : print(err.args[0]))

    for result in pipeline.Results:
        print(result)
        # print(result[-1][-2]["content"])
        # print(result[-1][-1]["content"])

    # context.LoadMessages()
    # print(json.dumps(context.Prompt("user", args[0]), indent=2))
    # context.Save()

Main(sys.argv[1:])
