import os
import sys
from peregrinegpt.gptcontext import GPTContext

def Main(args: list[str]):
    context: GPTContext = GPTContext("gpt-4", os.environ["OPENAI_KEY"])
    print(context.Prompt("user", args[0]))

Main(sys.argv[1:])