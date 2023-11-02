from typing import Any
from peregrinegpt.gptcontext import GPTContext

class PromptJob:
    def __init__(self, gpt: GPTContext):
        self.GPT: GPTContext = gpt
        pass

    def Run(self, args: list[Any] = None) -> Any:
        return

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.Run(args[0])
