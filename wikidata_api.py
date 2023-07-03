import requests
import json
id2name = {}
with open('wikidata_mapping/id2name.json') as file:
    data = json.load(file)
    for item in data:
        id2name[item['id']] = item['name']
# 定义SPARQL查询,获取正向相关的三元组
def get_forward_triples_by_id(id:str):
    query = f"""
    SELECT ?subjectLabel ?propertyLabel ?valueLabel WHERE {{
      wd:{id} ?property ?value .
      BIND(wd:{id} AS ?subject)
      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "en" .
        ?subject rdfs:label ?subjectLabel .
        ?property rdfs:label ?propertyLabel .
        ?value rdfs:label ?valueLabel .
      }}
      FILTER(STRSTARTS(STR(?property), "http://www.wikidata.org/prop/direct/P"))
    }}
    """

    # 发送查询请求并解析返回结果
    url = 'https://query.wikidata.org/sparql'
    params = {'format': 'json', 'query': query}
    response = requests.get(url, params=params)
    data = response.json()
    list = []
    # 解析返回结果并输出三元组信息
    for item in data['results']['bindings']:
        property_id = item['propertyLabel']['value'].split('/')[-1]
        # property_query = f"""
        # SELECT ?propertyLabel
        # WHERE {{
        #   wd:{property_id} rdfs:label ?propertyLabel .
        #   FILTER(LANG(?propertyLabel) = 'en')
        # }}
        # """
        # property_params = {
        #     "format": "json",
        #     "query": property_query
        # }
        # try:
        #     property_response = requests.get(url, params=property_params)
        #     property_data = property_response.json()
        # except Exception as e:
        #     print(e)
        #     continue

        # 解析返回的JSON响应
        # property_name = property_data["results"]["bindings"][0]["propertyLabel"]["value"]
        property_name = id2name[property_id]
        list.append({'subject': item['subjectLabel']['value'], 'relation': property_name, 'object': item['valueLabel']['value']})
    return list

# 定义SPARQL查询,获取正向相关的三元组
def get_reverse_triples_by_id(id:str):
    query = f"""
    SELECT ?subjectLabel ?propertyLabel ?valueLabel WHERE {{
      ?subject ?property wd:{id} .
      BIND(wd:{id} AS ?value)
      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "en" .
        ?subject rdfs:label ?subjectLabel .
        ?property rdfs:label ?propertyLabel .
        ?value rdfs:label ?valueLabel .
      }}
      FILTER(STRSTARTS(STR(?property), "http://www.wikidata.org/prop/direct/P"))
    }}
    """

    # 发送查询请求并解析返回结果
    url = 'https://query.wikidata.org/sparql'
    params = {'format': 'json', 'query': query}
    response = requests.get(url, params=params)
    data = response.json()
    list = []
    # 解析返回结果并输出三元组信息
    for item in data['results']['bindings']:
        property_id = item['propertyLabel']['value'].split('/')[-1]
        property_name = id2name[property_id]
        list.append({'subject': item['subjectLabel']['value'], 'relation': property_name, 'object': item['valueLabel']['value']})
    return list
# 组合正向和反向
def get_all_triples_by_id(id:str):
    forward_triples = get_forward_triples_by_id(id)
    reverse_triples = get_reverse_triples_by_id(id)
    triples = forward_triples + reverse_triples
    return triples
print(get_all_triples_by_id('Q41746'))