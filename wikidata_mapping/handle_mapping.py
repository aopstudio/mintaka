import json

# 读取JSON文件
with open('output.json', 'w', encoding='utf-8') as output:
    with open('properties.json') as file:
        data = json.load(file)
        for property in data:
            id = property['property'].split('/')[-1]
            name = property['propertyLabel']
            json.dump({'id':id,'name':name}, output, ensure_ascii=False)
            output.write('\n')  # 在每个JSON对象之后添加换行符