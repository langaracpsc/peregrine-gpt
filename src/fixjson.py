import os
import sys
import json 
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable
from peregrinegpt import Pipeline, Prompt, PromptJob, GPTContext
from peregrinegpt.concurrency import ParallelRunner, as_completed

class JsonFixJob(PromptJob):
    def __init__(self, gpt: GPTContext, file: str):
        super().__init__(gpt)
        self.File: str = file

    def Run(self, args: list[Any] = None) -> Any:
        with open(self.File, 'r') as fp:
            self.GPT.Prompt("user", json.load(fp)[-1]["content"])
        
        return self.GPT.Prompt("user", "This json has some errors, fix them and reply with the correct and complete json and nothing else.")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.Run(args[0])

def Main(args: list[str]):
    with open(args[0], 'r') as fp:
        pipeline: Pipeline = Pipeline(GPTContext("gpt-3.5-turbo-16k", os.getenv("OPENAI_KEY")))

        pipeline.AddJob(lambda gpt, result : gpt.Prompt("user", f"{json.load(fp)[-1]['content']}"))
        pipeline.AddJob(lambda gpt, result : gpt.Prompt("user", "This json has some errors, fix them and reply with the correct and complete json and nothing else."))
        
        pipeline.Run()

    with open(args[1], 'w') as fp:
        fp.write(pipeline.Results[-1][-1]["content"])

# Main(sys.argv[1:])

class JsonFixRunner(ParallelRunner):
    def __init__(self, gpt: GPTContext) -> None:
        super().__init__(gpt)
        self.Results: list = []

    def OnWait(runner: ParallelRunner):
        completed: list[Future] = list(runner.GetCompleted())
        print(f"Futures completed {0 if completed is None else len(completed)}")

    def Run(self, onWait: Callable[[Any], Any] = OnWait, onError: Callable[[Exception], Any] = None) -> bool:
        return super().Run(onWait, onError)

    def OnComplete(self) -> Any:
        completed: list[Future] = self.GetCompleted()
        self.Results = [result[-1]["content"] for result in [future.result() for future in completed]]

runner: JsonFixRunner = JsonFixRunner(GPTContext("gpt-3.5-turbo-16k", os.getenv("OPENAI_KEY")))

fixed = lambda file : f"{file.split('.')[0]}_fixed.json"

files: list[str] = json.load(open(sys.argv[1], 'r'))# os.listdir(sys.argv[1])

for file in files: 
    runner.AddJob(JsonFixJob(GPTContext("gpt-3.5-turbo-16k", os.getenv("OPENAI_KEY")), f"{sys.argv[2]}/{file}"))

runner.Run()

x: int = 0

for result in runner.Results:
    with open(f"{sys.argv[3]}/{fixed(files[x])}", 'w') as fp:
        fp.write(result)
    x += 1

# runner.AddJob(lambda gptContext : gptContext.Prompt("user", "hello gpt"))\
#     .AddJob(lambda gptContext : gptContext.Prompt("user", "hello sir, you're now llama"))\
#     .AddJob(lambda gptContext : gptContext.Prompt("user", "Hi, please leave me alone"))\
#     .Run()



