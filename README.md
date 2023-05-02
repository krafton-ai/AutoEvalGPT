# AutoEvalGPT


## What is it?

Inspired by [Vicuna](https://vicuna.lmsys.org/) from lm-sys, we modified their prompts to be more robust and permutation invariable. 

## What is different from Vicuna's Auto-evaluation?
1. GPT-4 also generates "Metrics"
2. Evaluate each metric individually. (Not all metrics at single generation)
3. Set Assistant 1 to GPT-4, and fix the score at specific point as well.
    1. For example, you would assign 7 points to GPT-4 and distribute the scores as 3, 2, 2 for metrics 1, 2, and 3, respectively.
    2. In `autoeval.py`, you may modify the prompt for custom metrics and adjust the score distribution.
4. Set Assistant 2 to your model and evaluate.

## Prompt Format
```
{Task Description}
{Data}
{Answer 1}
{Answer 2}
We would like to request your feedback on the performance of two AI assistants in response to the user question displayed above.
Each assistant receives an overall score on a scale of 0 to 10, where a higher score indicates better overall performance. 
{Detailed metrics when evaluating the Task above}
Let's say the score of Assistant 1 is 3, 2, 2 for {metric 1}, {metric 2}, and {metric 3}, respectively.
Please first provide detailed explanations, specifying at which part of the example you think it is, avoiding any potential bias, and ensuring that the order in which the responses were presented does not affect your judgment. 
Please provide the detailed explanations specifying at which part of the example is better or worse and give the score to assistant 2 compared to the score of Assistant 1.  
At this time, evaluate the {metrics[k]} score only. You may speak in English.
```
You may adjust the score distribution of Assistant 1.

## How can we use this?
1. Clone the git repository, and go to AutoEvalGPT
```bash
git clone https://github.com/krafton-ai/AutoEvalGPT.git
cd AutoEvalGPT
```
2. If your data is ready, run the `autoeval.py` like below
```bash
python autoeval.py --data data_example.json --save --apikey YOUR_OPENAI_API_KEY --organization YOUR_ORGANIZATION_ID
```
Then, you will receive the result in the terminal. 

## Commands 
### Mandatory
`--data` (str): The directory to your data for evaluation. Please check the data format in `data_example.json` and customize this for your own data.  
`--apikey` (str): your OPENAI api key for using GPT-4. If you don't have access to GPT-4, please change the model to GPT-3.5 in `autoeval.py` even though the result will be sub-optimal.  

### Optional
`--save` (void): Once you type `--save`, you will obtain an `eval_results.json` file in your directory, which includes the rationale for the evaluation and the total score of each example (not each model).  
`--organization` (str): Organization ID of OpenAI if you have one.  
`--task` (str): The short task description of your dataset for evaluation. This is not mandatory once you have task description in your data.


## Output
### Translation
If we do the translation task from English to Korean, if you use `data_example.json` as the input, the results should be like the following.
```
Scores:
DeepL: 10.0
ChatGPT3.5: 8.8
Vicuna-13B: 3.8
Korani-v2: 5.4
Korani-v1: 7.9
Koalpaca-13B: 6.7
```

## Alert
**Scoring higher than 7.0 compared to GPT-4 doesn't always mean the model is better than GPT-4.**  
Sometimes, Assistant 2 gets a higher score even when the results from Assistant 1 and 2 are quite similar, and there's no clear reason why. If you want to find out if it's truly better than GPT-4, you should check permutation invariance. In simple terms, just swap the positions of Assistant 1 and 2, run the same test, and see if you still get the same result (your model being better than GPT-4).

## LICENSE
The code is released under the Apache-2.0 License. See `LICENSE` for full terms.
The generated data is subject to [Terms of Use](https://openai.com/policies/terms-of-use) of OpenAI.