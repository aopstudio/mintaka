# 只提供1跳三元组
import openai
import numpy as np
from evaluate import *
import time
openai.api_key="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"
number_dict = {
    "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9,
    "zero":0
}
dataset = load_mintaka_test('data/mintaka_test.json','text','en')
print(dataset)
all = 0
right = 0
with open('current_index.txt','r') as f:
    current_index = f.readline()
    current_index = int(current_index)
len_dataset = len(dataset['answer'])
with open('preds.txt', 'a+') as pred_file:
    for ix in range(current_index,len_dataset):
        all += 1
        id = dataset['id'][ix]
        question = dataset['question'][ix]
        prompt = f'''Please answer the question in one phrase instead of a sentence. When encountering entity prediction question, answer the entity name. When encountering questions about right or wrong judgment, only answer True or False. When encountered a date prediction problem, using the format of YYYY-MM-DD. 
        Question: How many teams has Matthew Stafford played for?
        Answer: 2
        Question: Is Venus Williams older than Serena Williams?
        Answer: True
        Question: Who was the youngest to win an Oscar for Best Actress?
        Answer: Marlee Matlin
        Question: Who was the last Alabama governor that wasn't a Republican?
        Answer: Don Siegelman
        Question: Who was the quarterback of the team that won Super Bowl 40?
        Answer: Matt Hasselbeck
        Question: Which movie was directed by Denis Villeneuve and stars Timothee Chalamet?
        Answer: Dune
        Question: Which Twilight Saga movie did Anna Kendrick not appear in?
        Answer: The Twilight Saga: Breaking Dawn – Part 2
        Question: Has any David Fincher movie won a BAFTA Award without Pitt's involvement?
        Answer: True
        Question: Where was the actor who played Achilles in Troy born?
        Answer: Shawnee
        Question: {question}
        Answer: 
        '''
        try:
            response = openai.ChatCompletion.create( 
                model="gpt-3.5-turbo", 
                messages=[ 
                {"role": "user", "content": prompt}
            ] )
        except Exception as e:
            print(e)
            time.sleep(10)
            try:
                response = openai.ChatCompletion.create( 
                    model="gpt-3.5-turbo", 
                    messages=[ 
                    {"role": "user", "content": prompt}
                ] )
            except Exception as e1:
                with open('current_index.txt', 'w') as index_file:
                    index_file.write(str(ix))
        print('Question: '+question)
        pred = response["choices"][0]["message"]["content"]
        for key in number_dict:
            if key == pred.lower().strip() or f'{key}.' == pred.lower().strip():
                pred = pred.lower().replace(key,str(number_dict[key]))
                break
        print('Pred: '+pred)
        answer = dataset['answer'][ix]
        print('Answer: '+answer)
        if answer.lower() in pred.lower():
            right += 1
        pred = pred.strip('.')
        pred_file.write(f'"{id}": "{pred}",\n')
        print("Acc:",right/all)
print("Acc:",right/all)