from types import FunctionType
from typing import Any, Callable
from peregrinegpt.prompt import PromptJob
from peregrinegpt.gptcontext import GPTContext
import typing

class Pipeline:
    def __init__(self, gpt: GPTContext):
        self.Jobs: list[PromptJob] = list[PromptJob]()
        self.Results: list[Any] = list[Any]()
        self.GPT: GPTContext = gpt
        self.IsRunning: bool = False 

    def AddJob(self, job: Callable[[list[GPTContext, Any]], Any]) -> Any:
        self.Jobs.append(job)

        return self 

    def CreateJob(self, jobType: type) -> Callable[[GPTContext, Any], Any]:
        job: type = jobType(self.GPT)

        if (not(callable(job))):
            raise TypeError("Job type must be callable.")

        self.Jobs.append(job)

        return job

    def Run(self, args: list[dict[str, str]] = None, onError: Callable[[BaseException], Any] = None) -> list[dict[str, str]]:
        prevResult: Any = None

        for job in self.Jobs:
            try:
                prevResult = job(self.GPT, prevResult)
                self.Results.append(prevResult)

            except Exception as e:
                if (onError != None):
                    onError(e)
                raise e

        return prevResult

    def Save(self, promptFile: str = "prompts.json"):
        self.GPT.Save(promptFile)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        onError: FunctionType = None
        
        if (len(args) > 2):
            onError = args[1]

        return self.Run(args[0], onError)


