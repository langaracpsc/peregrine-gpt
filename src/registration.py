import os
import sys
import json
from typing import Any

from peregrinegpt.gptcontext import GPTContext
from peregrinegpt.pipeline import Pipeline
from peregrinegpt.prompt import PromptJob
from peregrinegpt.web.scraping import DataScraper

def LoadQuestions(questionFile: str) -> list[dict[str, str]]:
    questions: list[dict[str, str]]
    prompts: list[dict[str, str]] = []

    with open(questionFile, 'r') as fp:
        questions = json.load(fp)["answered"]

    for question in questions:
        prompts.append({"role": "user", "content": question["question"]})
        prompts.append({"role": "assistant", "content": question["answer"]})

    return prompts

class SetupJob(PromptJob):  
    def __init__(self, gpt: GPTContext, rolePrompt: str):
        super().__init__(gpt)
        self.RolePrompt: str = rolePrompt

    def Run(self, args: list[Any] = None) -> Any:
        scraper: DataScraper = DataScraper()

        scraper.Scrape("https://langara.ca/reg-guide/before-you-register/how-to-access-registration.html")

        self.GPT.Prompt("system", self.RolePrompt)
       
        print("Role prompted")
        print("Prompting info.")

        return self.GPT.Prompt("user", f"{scraper.GetDataStr()}\n\nPhrase all the info you got from that blob of text.")


class LoadedJob(PromptJob):
    def __init__(self, gpt: GPTContext, promptFile: str):
        super().__init__(gpt)
        self.PromptFile: str = promptFile
    
    def Run(self, args: list[Any] = None) -> Any:
        messages: list[dict] = None

        with open(self.PromptFile, "r") as fp:
            self.GPT.Send(json.load(fp))

        print("Prompts loaded.")

        print(f"Prompt size {len(self.GPT.Messages)}")
        return self.GPT.Prompt("user", "How do i access registration?")

class QuestionGenJob(PromptJob):
    def __init__(self, gpt: GPTContext):
        super().__init__(gpt)

    def Run(self, args: list[Any] = None) -> Any:
        print("Prompting question.")
        return self.GPT.Prompt("user", "Generate 10 or more questions that can be answered with that info. Reply with questions in format Question: [QUESTION] and nothing else, put each question in a new line.")

class AnswerJob(PromptJob):
    def __init__(self, gpt: GPTContext):
        super().__init__(gpt)

    def Run(self, args: list[Any] = None) -> Any:
        print("Generating answers.")
        return self.GPT.Prompt("user", """Now answer those questions with as much accuracy as possible. If you dont have enough information, put the question in a separate list.
        Put all the questions with their answers in a JSON format, like so {\"question\": \"[QUESTION]\", \"answer\": \"[ANSWER]\"}, and make a JSON list of them.
        Reply with both type of pairs in a JSON format like so { \"answered\": [JSON LIST OF QUESTIONS WITH ANSWERS], "unanswered": [JSON LIST OF QUESTIONS THAT COULDNT BE ANSWERED] }. 
        Put the reason why you couldnt answer the unanswered questions in their answer field. Reply with the latter json only. 
        """)


def Main(args: list[str]):
    if (len(args) < 1): 
        print("")
    
    context: GPTContext = GPTContext("gpt-3.5-turbo-16k", os.getenv("OPENAI_KEY"))

    pipeline: Pipeline = Pipeline(context)

    # pipeline.AddJob(SetupJob(context, "You are Peregrine, an advisor at Langara college and a part of the Langara Computer Science Club. You have info on everything a Langara student needs to know and are capable of helping them directly. The students can reach out to you and ask questions about a specific department, or the club, and it's your duty to try and help them as much as possible with the credible information you have on the college. You will chat with students to solve their issues and give them suggestions about their college activities. You will answer in different types of details and formats depending upon the question."))
    # pipeline.CreateJob(QuestionGenJob)
    # pipeline.CreateJob(AnswerJob)

    pipeline.AddJob(LoadedJob(context, args[0]))

    pipeline.Run()
    # pipeline.Save(args[1])

    # with open(args[0], 'w') as fp:
    #     fp.write(pipeline.Results[-1][-1]["content"])

    prompts: list[dict[str, str]] = LoadQuestions(args[1])

    for prompt in prompts:
        pipeline.GPT.AddPrompt(prompt)

    pipeline.GPT.Update()
    pipeline.Save(args[1])
    print("Updated")

Main(sys.argv[1:])
