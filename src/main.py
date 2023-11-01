import os
import sys
import json 
from peregrinegpt.gptcontext import GPTContext

def Main(args: list[str]):
    context: GPTContext = GPTContext("gpt-4", os.environ["OPENAI_KEY"])
    context.LoadMessages()
    print(json.dumps(context.Prompt("user", args[0]), indent=2))
    context.Save()

Main(sys.argv[1:])