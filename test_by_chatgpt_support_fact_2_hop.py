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
        questionEntityList = dataset['questionEntity'][ix]
        for entity in questionEntityList:
            name = str(entity['name'])
            if not name.startswith('Q'): # 跳过不是知识库中的实体
                continue
            
        # entity = 
        prompt = f'''Please answer the question in one phrase instead of a sentence. When encountering entity prediction question, answer the entity name. When encountering questions about right or wrong judgment, only answer True or False. When encountered a date prediction problem, using the format of YYYY-MM-DD. 
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
        break
print("Acc:",right/all)