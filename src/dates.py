import os
import sys
from peregrinegpt import Prompt, PromptJob, Pipeline, GPTContext
from peregrinegpt.web.scraping import DataScraper

def SetupJob(gpt: GPTContext, args: list[dict[str, str]]) -> list[dict[str, str]]:
    scraper = DataScraper()
    scraper.Scrape("https://langara.ca/registration-and-records/important-dates/index.html")
    
    # print("Role prompted")
    print("Prompting info.")

    return gpt.Prompt("user", f"{scraper.GetDataStr()}\n\nPhrase all the info you got from that blob of text.")

def QuestionGen(gpt: GPTContext, args: list[dict[str, str]]):
    print("Prompting question.")
    return gpt.Prompt("user", "Generate 10 or more questions that can be answered with that info. Reply with questions in format Question: [QUESTION] and nothing else, put each question in a new line.")

def AnswerJob(gpt: GPTContext, args: list[dict[str, str]]):
    print("Generating answers.")
    return gpt.Prompt("user", """Now answer those questions with as much accuracy as possible. If you dont have enough information, put the question in a separate list.
    Put all the questions with their answers in a JSON format, like so {\"question\": \"[QUESTION]\", \"answer\": \"[ANSWER]\"}, and make a JSON list of them.
    Reply with both type of pairs in a JSON format like so { \"answered\": [JSON LIST OF QUESTIONS WITH ANSWERS], "unanswered": [JSON LIST OF QUESTIONS THAT COULDNT BE ANSWERED] }. 
    Put the reason why you couldnt answer the unanswered questions in their answer field. Reply with the latter json only. """)

def main(args: list[str]):
    pipeline = Pipeline(GPTContext("gpt-3.5-turbo-16k", os.getenv("OPENAI_KEY"), "prompts3.json"))
    pipeline.AddJob(SetupJob) \
            .AddJob(QuestionGen) \
            .AddJob(AnswerJob) \
            .Run()
    
    print(pipeline.Results[-1])
    pipeline.Save()

main(sys.argv[1:])
