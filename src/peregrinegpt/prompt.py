from typing import Any
from gptcontext import GPTContext

class PromptJob:
    def __init__(self, gpt: GPTContext):
        self.GPT: GPTContext = gpt
        pass

    def Run(self, args: list[Any] = None) -> Any:
        return

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.Run(args)
