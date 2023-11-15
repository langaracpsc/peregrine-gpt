import os
import sys
import json

def ExtractID(file: str):
    i: int = 0
    while (not(file[i].isnumeric())):
        i += 1
    return file[i:-5]

def ToGPTPromptPair(prompt: dict[str]) ->  tuple[dict[str, str]]:
    return tuple((dict({
        "role": "user",
        "message": prompt["question"]
    }), dict({
        "role": "assistant",
        "message": prompt["answer"]
    })))

def GetSortedFiles(path: str) -> list[str]:
    dirList = os.listdir(path)

    fileMap: dict = {}

    for file in dirList:
        fileMap[int(ExtractID(file))] = file

    return [fileMap[key] for key in sorted(fileMap.keys())]

def ExtractQuestions(prompt: dict[str, str]) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = json.loads(prompt["content"])["answered"]
    prompts: list[dict[str, str]] = []

    for question in questions:
        for prompt in ToGPTPromptPair(question): 
            prompts.append(prompt)

    return prompts

def CombinePrompts(path: str) -> (list[dict[str, str]], list[str]):
    combinedPrompts: list[dict[str, str]] = []

    failedFiles: list[str] = []

    for file in GetSortedFiles(path):
        with open(f"{path}/{file}", 'r') as fp:
            try:
                prompts: list[dict[str, str]] = json.load(fp)[2:]
                questions: list[dict[str, str]] = ExtractQuestions(prompts[-1])

                for prompt in prompts:
                    combinedPrompts.append(prompt)

                for question in questions:
                    combinedPrompts.append(question)

            except Exception as e:
                print(f"Exception occured while parsing {file}. {e}")
                failedFiles.append(file)
           
    return combinedPrompts, failedFiles

combined, failed = CombinePrompts(sys.argv[1])

if (len(failed) >= 0):
    with open(sys.argv[3], 'w') as fp:
        json.dump(failed, fp)
else:
    with open(sys.argv[2], 'w') as fp:
        json.dump(failed, fp)
