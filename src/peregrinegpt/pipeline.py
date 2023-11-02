from typing import Any, Callable
from peregrinegpt.prompt import PromptJob
from peregrinegpt.gptcontext import GPTContext
import typing

class Pipeline:
    def __init__(self, gpt: GPTContext):
        self.Jobs: list[PromptJob] = list[PromptJob]()
        self.Results: list[Any] = list[Any]()
        self.GPT: GPTContext = gpt

    def AddJob(self, job: PromptJob) -> Any:
        if (not(issubclass(type(job), PromptJob))):
            raise TypeError("Job object must be a variant of PromptJob.")

        self.Jobs.append(job)

        return self 

    def CreateJob(self, jobType: type) -> PromptJob:
        job: type = jobType(self.GPT)
        self.Jobs.append(job)

    def Run(self, onError: Callable[[BaseException], Any] = None) -> bool:
        prevResult: Any = None

        for job in self.Jobs:
            try:
                prevResult = job(prevResult)

                self.Results.append(prevResult)

            except Exception as e:
                if (onError != None):
                    onError(e)

                return False

        return True
    
    def Save(self, promptFile: str = "prompts.json"):
        self.GPT.Save(promptFile)
