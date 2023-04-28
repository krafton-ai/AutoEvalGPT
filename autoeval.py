import torch
import numpy as np
import re
from transformers import AutoTokenizer, DPRQuestionEncoder, DPRContextEncoder
from typing import List
import argparse
import openai
import requests, json
import ray
import time

parser = argparse.ArgumentParser(description='My FastAPI app')
parser.add_argument('--task', type=str, default='Translation into Korean', help='task description. If not typed, your data must contain the task description in \'task\' field')
parser.add_argument('--data', type=str, default='data_example.json', help='directory of your data file')
parser.add_argument('--apikey', type=str, default=None, help = 'Your OpenAI API KEY')
parser.add_argument('--organization', type=str, default=None, help='Your organization ID in OpenAI')
args = parser.parse_args()

openai.api_key = args.apikey
openai.organization = args.organization
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}",
    "OpenAI-Organization": openai.organization
}



##################################
## Data Loading
##################################

if args.data is not None:
    file_name = args.data

with open(file_name, 'r') as file:
    data_ex = json.load(file)


##################################
## Criteria Generation
##################################

# Task description
if args.task is not None:
    task = args.task
else:
    task = data_ex[0]['task']

print("Generating the criteria")
message = [{"role":"user", "content":f"""What is the 3 key metrics when we evaluate the following Task? 
Task: {task}
Suggest in 3 bullet points.
The name of the metrics should be a single word, but it could be two words sometimes.
Please distribute 10 total points into each metric as well.
Please do not implement the Task since your task is telling the 3 key metrics in English.
Your response should be like - {{metric name}} ({{score}} points): {{metric explanation sentence}}"""}]
data = {
    "model":"gpt-4",
    "messages" : message,
    "temperature" : 0.1,
    "max_tokens" : 512,
    "frequency_penalty" : 0.2
}
response = None
while True:
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            # timeout=15,
        )
        break
    except requests.exceptions.Timeout:
        print(f"Request timed out after 15")
print("Generated Criteria:\n", response.json()["choices"][0]["message"]["content"])
criteria = response.json()["choices"][0]["message"]["content"]

##################################
## Metric Name Extraction
##################################

pattern = r'[-\d]+\.\s*([A-Za-z]+)|-\s*([A-Za-z]+)'

metric_names = [name[0] or name[1] for name in re.findall(pattern, criteria)]
print(f"metric_names: {metric_names}")

##################################
## Prompt Generation
##################################
print("Generating the prompts")

metrics_in_string = ", ".join(metric_names)
# How to evaluate the task
system_list = []
for i in range(len(metric_names)):
    system_list.append(f"""We would like to request your feedback on the performance of two AI assistants in response to the user question displayed above.
Each assistant receives an overall score on a scale of 0 to 10, where a higher score indicates better overall performance. 
The detailed guideline for the scoring is the following:
{criteria}
Let's say the score of Assistant 1 is 3, 2, 2 for {metrics_in_string}, respectively.
Please first provide detailed explanations, specifying at which part of the example you think it is, avoiding any potential bias, and ensuring that the order in which the responses were presented does not affect your judgment. 
Please provide one criteria per each paragraph and give the score to assistant 2 compared to the score of Assistant 1.
At this time, evaluate the {metric_names[i]} score only. You may speak in English.""")

### 1-shot template of user-assistant pair 
# just for showing the desirable template that we want to generate
# This template does not contain the specific example here but we only give the general categorical names by braces {~~}
user_template=f"""[Question]
{task}
{{task_data}}
[The Start of Assistant 1's Answer]
{{Answer1}}
[The End of Assistant 1's Answer]
[The Start of Assistant 2's Answer]
{{Answer2}}
[The End of Assistant 2's Answer]
[System]
{system_list[0]}"""

assist_template = f"""For {metric_names[0]}, {{At which part does Assistant 2 cover more/less than Assistant 1 in 3 sentences}}."""

# Gather the prompts in a list "prompts" by metrics -> examples -> models.
# So in prompts, we have [Example1_metric1, Example1_metric2, Example2_metric1, Example2_metric2] if we have 2 examples and 2 metrics
prompts = []
for i in range(len(data_ex[0]['model'])):
    for inputs, answer1, answer2 in zip(data_ex[0]['inputs'], data_ex[0]['GPT-4'], data_ex[0]['model'][i]['outputs']):
        for k in range(len(metric_names)):
            prompts.append(
f"""[Question]
{task}
{inputs}
[The Start of Assistant 1's Answer]
{answer1}
[The End of Assistant 1's Answer]
[The Start of Assistant 2's Answer]
{answer2}
[The End of Assistant 2's Answer]
[System]
{system_list[k]}"""
)

##################################
## Evaluate
##################################
ray.init()
num_workers = 15

print("Evaluate!")

@ray.remote(num_cpus=num_workers)
def get_eval(message):
    for i in range(4):
        data = {
            "model":"gpt-4",
            "messages" : message,
            "temperature" : 0.1,
            "max_tokens" : 512,
            "frequency_penalty" : 0.2,
            "stop": ["\n\n", "\nFor"]
        }
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=60,
            )
            content = response.json()["choices"][0]["message"]["content"]
            print(content)
            return content
        except Exception as e:
                logger.error(e)
                time.sleep(2)
    logger.error(f'Failed after 2 retries.')
    return 'error'

# Evaluate each metrics per each example for each model.
results = []
for i in range(0, len(prompts), num_workers): # Batching. num_workers = num_batch in this code
    messages = []
    for j in range(min(num_workers, len(prompts)-i) ):
        messages.append( [{"role":"user", "content":user_template}, 
        {"role":"assistant", "content":assist_template}, 
        {"role":"user", "content":prompts[i+j]}])
     # Call the api_call function remotely for each example in the batch
    futures = [get_eval.remote(message) for message in messages]

    # Wait for the results to be ready
    ready_futures, remaining_futures = ray.wait(futures, num_returns=len(futures))

    # Get the results
    batch_results = ray.get(ready_futures)
    results.extend(batch_results)

    # Wait
    print(f'Waiting for 2 seconds before sending the next request.')
    time.sleep(2)

# Gather the result texts per each example
print("Gathering the result texts")
results_per_ex = []
for i in range(0, len(results), len(metric_names)):
    results_example=""
    for item in results[i:i+len(metric_names)]:
        results_example += (item+"\n")
    results_per_ex.append(results_example)

# Get the scores per each example
print("Extracting the Scores per each example")
scores=[]
total_score_pattern = r'Total Score:.+=\s*([\d.]+)'
for item in results_per_ex:
    message = [{"role":"user", "content": item + """\nSo in total, What's the total score of Assistant 2? Your response should be like 
Total Score: {score1(number only)} + {score2(number only)} + {score3(number only)} = {total_score (number only)}"""}]
    futures = get_eval.remote(message)
    
    text = ray.get(futures)
    total_score = re.search(total_score_pattern, text)
    total_score_value = float(total_score.group(1))
    scores.append(total_score_value)

# Get the total average score per each model
print("Scores:")
for i, item in enumerate(data_ex[0]['model']):
    model_score = np.mean(scores[len(item['outputs'])*i:len(item['outputs'])*(i+1)])
    print(f"{item['name']}: {model_score}")