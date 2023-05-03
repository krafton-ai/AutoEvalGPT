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
If we do the translation task from English to Korean and you use `data_example.json` as the input, then the results should be like the following.
```
Scores:
DeepL: 10.0
ChatGPT3.5: 8.8
Vicuna-13B: 3.8
Korani-v2: 5.4
Korani-v1: 7.9
Koalpaca-13B: 6.7
```
```
input = ""Hey! I have some Kissflow Legal Review requests that are blocked by Tax and Accounting, can this be looked at?""
```
| Model | Score (averaged over 5 examples) | Output Example |
| --- | :---: | ---: | 
| GPT-4 | - | 헤이! 제가 Tax and Accounting에 의해 차단된 몇 가지 Kissflow 법률 검토 요청이 있는데, 이것을 확인해 주실 수 있나요? |
| DeepL | 9.4 | 안녕하세요! 세무 및 회계에서 차단된 Kissflow 법률 검토 요청이 몇 개 있는데요, 이 요청을 살펴볼 수 있나요?  |
| GPT-3.5-turbo | 8.6 | 안녕하세요! 세무 및 회계 부서에서 차단된 몇 가지 Kissflow Legal Review 요청이 있습니다. 확인해 주실 수 있나요? |
| Vicuna-13B | 3.8 | 안녕하세요! 세금계산과 회계부서가 차단해 있는 Kissflow Legal Review 요청이 몇 개가 있습니까? 이것을 살펴보시겠습니까? |
| KoAlpaca-13B | 5.6 | 야! 세금과 회계에 막힌 키싱플로우 법적 검토 요청이 있는데, 이거 검토해줄 수 있어? |
| KORani-v1 | 7.5 | 안녕하세요! 세금과 회계로 인해 막혀 있는 키스플로우 법률 검토 요청이 몇 개 있는데, 검토해 주실 수 있나요? |
| KORani-v2 | 5.4 | 안녕하세요! 제가 Kissflow Legal Review 요청을 목격했는데, 세무 및 회계 부서에서 차단하고 있는데 이 문제를 조사해 주시겠어요? |
| KORani-v3 | 7.1 | 안녕하세요! 저는 Kissflow Legal Review 요청이 세금과 회계에 의해 차단되고 있는데, 이 문제가 살펴볼 수 있을까요? |

### QA(Korean)
```
prompt = "우리는 아래와 같은 정보를 갖고 있습니다.
---------------------
헨리 구스타프 몰래슨(영어: Henry Gustav Molaison, 1926년 2월 26일 ~ 2008년 12월 2일)은 뇌전증을 치료하기 위해서 수술적으로 해마를 포함한 내측측두엽이 제거된 미국의 기억장애 환자 H.M으로 전부터 이미 알려져 있었다. 그는 1957년 말부터 그가 죽을 때 까지 그는 광범위하게 연구가 되었다. 그의 경우는 뇌 기능과 기억 사이의 링크를 설명하는 이론 발달과 뇌인지심리학의 발달, 뇌의 구조와 기능이 특정 심리적 과정과 관한 이해를 목표로 하는 심리학의 한 지점에 매우 중요한 역할을 하였다. 그가 죽기 전에, 그는 코네티컷 주 윈저 락스에 위치한 관리기관에 살면서 지속적으로 조사가 되었다. 그의 뇌는 지금 2009년 12월 4일에 조직학적으로 슬라이스되어 미국 샌디에이고에 있다.---------------------
### 주어진 정보에 따라, 질문에 답해주세요.: '헨리 구스타프의 뇌는 현재 어디에 위치해 있는가?'
### Assistant:"
```
| Model | Score (averaged over 5 examples) | Output Example |
| --- | :---: | ---: | 
| GPT-4 | - | 헨리 구스타프의 뇌는 현재 미국 샌디에이고에 위치해 있다. |
| GPT-3.5-turbo | 7.1 | 헨리 구스타프의 뇌는 지금 2009년 12월 4일에 조직학적으로 슬라이스되어 미국 샌디에이고에 있다. |
| Vicuna-13B | 7.2 | 헨리 구스타프의 뇌는 2009년 12월 4일에 조직학적으로 슬라이스되어 미국 샌디에이고에 있습니다. |
| KoAlpaca-13B | 2.6 | Henry Gustav Molaison의 뇌는 2008년에 사망하였습니다. 그의 뇌는 코네티컷 주 윈저 락스에 위치한 기관에 보관되어 있으며, 현재도 계속 조사중입니다. |
| KORani-v1 | 6.6 | 헨리 구스타프 몰레이슨의 뇌는 현재 미국 샌디에이고에 있습니다. 그의 뇌는 1957년 수술로 제거된 그의 내측 측두엽의 자리를 확인하기 위해 조직학적으로 절단되었습니다. 이 연구는 뇌의 구조와 기능이 특정 심리적 과정과 관련된 이해를 목표로 하는 심리학의 한 분야인 인지 신경과학에 대한 그의 공헌을 기리기 위한 것입니다." |
| KORani-v2 | 8.0 | 헨리 구스타프의 뇌는 현재 캘리포니아 샌디에이고에 있는 샌디에이고 대학교 웨스트 캠퍼스의 신경과학 실험실에 보관되어 있습니다. |
| KORani-v3 | 6.4 | 헨리 구스타프의 뇌는 현재 코네티컷 주 윈저 락스에 있는 관리 기관에 있습니다. |

### Summarization (Korean)
```
prompt = "# Document
전년도 대비 79명 늘어 1019명, 행정수요 대처 이성훈 sinawi@hanmail.net 광양시의 공무원 정원이 크게 늘어나 행정서비스 향상이 기대된다. 시는 행정안전부에서 발표한 2018년도 자치단체 기준인건비에서 광양시의 일반직 정원이 지난해보다 79명이 늘어난 1019명으로 산정됐다고 밝혔다. 지난 1995년 도농통합 당시 991명이었던 광양시 공무원 정원은 IMF시절에 혹독한 구조조정을 거치면서 2002년에는 788명으로 200여명이 가까이 줄어들었으나 이번 정원 확보로 공무원 정원 1000명 시대를 맞게 됐다. 그동안 광양시는 포스코를 중심으로 한 산업단지와 컨테이너부두, 경제자유구역, 택지 개발, 다양한 복지 정책 등 시민의 삶의 질 향상을 위한 행정수요가 날로 증폭하는 데에 비해 한정된 공무원 정원으로 많은 어려움을 겪어 왔었다. 시의 이번 정원 충원은 지금까지 격무에 시달려온 공무원들에게 더욱 열심히 일할 수 있도록 활력을 불어넣으면서 지역과 나라 발전을 뒷받침 하는 경제도시로서의 위상을 드높이는 시너지 효과로 이어질 것으로 기대된다. 한편, 광양시는 한시기구인‘기업유치추진단’이 2017년 연말로 폐지됨에 따라 전라남도로부터 4급 상설기구인‘산단녹지관리센터’를 승인 받아 올해 1월부터 운영하게 됨으로써 도시 개발에 한층 탄력을 받을 것으로 전망하고 있다. 정홍기 총무과장은“참으로 어렵게 가져온 공무원 정원과 4급 상설기구는 격무에 시달려온 직원들의 숨통을 트이게 해 15만 시민을 위한 행정서비스 질을 향상시킬 것으로 기대된다”며“이달 안에 정원 조례를 개정하고, 직무분석을 통해 부서별 정원을 조정할 계획이다”고 말했다.

한국어 3문장으로 위의 Document를 요약해줘.
### Assistant: 1)"
```
| Model | Score (averaged over 5 examples) | Output Example |
| --- | :---: | ---: | 
| GPT-4 | - | 1) 광양시의 공무원 정원이 전년도 대비 79명 늘어난 1019명으로 증가했다. 2) 이로 인해 행정서비스 향상이 기대되며, 지역과 나라 발전을 뒷받침하는 경제도시로서의 위상이 상승할 것으로 전망된다. 3) 한편, 광양시는 전라남도로부터 4급 상설기구인 '산단녹지관리센터'를 승인받아 도시 개발에 탄력을 받을 것으로 예상된다. |
| GPT-3.5-turbo | 8.5 | 1) 광양시 공무원 정원이 79명 늘어 1019명으로 늘어나 행정서비스 향상이 기대된다고 밝혔다.2) 광양시는 이번 정원 충원으로 지역과 나라 발전을 뒷받침 하는 경제도시 위상을 드높일 것으로 기대된다. 3) 정원 조례를 개정하고, 직무분석을 통해 부서별 정원을 조정할 계획이다. |
| Vicuna-13B | 7.4 | 1) 2018년도 광양시의 공무원 정원 1019명, 지난해 79명 증가. 2) 이번 정원 충원은 지금까지 격무에 시달려온 공무원들에게 더욱 열심히 일할 수 있도록 활력을 불어넣으면서 지역과 나라 발전을 뒷받침 하는 경제도시로서의 위상을 드높이는 시너지 효과로 이어질 것으로 기대된다. 3) 광양시는 전라남도로부터 4급 상설기구인‘산단녹지관리센터’를 승인 받아 운영하게 됨으로써 도시 개발에 한층 탄력을 받을 것으로 전망하고 있다. |
| KoAlpaca-13B | 5.7 | 1) 광양시는 작년보다 79명 늘어난 1019명의 공무원을 둘 수 있게 되었습니다. 2) 이는 행정안전부의 지침에 따른 것입니다. 3) 이로써 광양시는 한정된 예산으로 인해 발생했던 공무원들의 초과 근무 수당 지급 등의 문제를 해결 할 수 있게 되었습니다. |
| KORani-v1 | 7.0 | 1) 광양시는 작년보다 79명이 늘어난 1019명의 일반직 공무원 정원을 행안부로부터 승인받았습니다. 2) 이는 광양시의 행정 수요 증가를 수용하기 위한 것입니다. 3) 이 정원 증가는 광양시 공무원들에게 더 많은 기회를 제공할 것입니다. |
| KORani-v2 | 6.2 | 1)광양시의 공무원 정원은 이번 정원 확보로 1000명 주당 공무원 정원을 달성했습니다. 2) 이러한 충원은 지금까지 격무에 시달려온 공무원들에게 더욱 열심히 일할 수 있도록 활력을 불어넣으면서 지역사회와 국가의 발전을 지원하는 시너지 효과로 이어질 것으로 기대됩니다. 3) 광양시는 '기업유치추진단'을 폐지하고 '산단녹지관리센터'를 승인했으며, 이는 도시 개발에 한층 탄력을 받을 것으로 기대됩니다. |
| KORani-v3 | 6.9 | 1)광양시의 공무원 정원은 지난해보다 79명이 늘어난 1019명으로 산정되었습니다.2) 이러한 충원은 지역사회와 국가 발전을 지원하는 행정서비스의 향상으로 이어질 것으로 기대됩니다.3) 시는 '이달 내에 정원 조례를 개정하고 직무분석을 통해 부서별로 정원을 조정할 계획'이며 행정서비스 향상을 위해 노력할 것이라고 밝혔습니다. |

## Alert (Limitations)
**Scoring higher than 7.0 compared to GPT-4 doesn't always mean the model is better than GPT-4.**  
Sometimes, Assistant 2 gets a higher score even when the results from Assistant 1 and 2 are quite similar, and there's no clear reason why. If you want to find out if it's truly better than GPT-4, you should check permutation invariance. In simple terms, just swap the positions of Assistant 1 and 2, run the same test, and see if you still get the same result (your model being better than GPT-4).
## LICENSE
The code is released under the Apache-2.0 License. See `LICENSE` for full terms.
The generated data is subject to [Terms of Use](https://openai.com/policies/terms-of-use) of OpenAI.