import requests

def get_entity_relationship_path(start_entity_id, end_entity_id, max_hops):
    url = "https://query.wikidata.org/sparql"

    query = f"""
    SELECT ?path
    WHERE {{
      wd:{start_entity_id} (<>|!<>)* ?path .
      ?path (<>|!<>)* wd:{end_entity_id} .
    }}
    LIMIT {max_hops}
    """

    params = {
        "format": "json",
        "query": query
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 解析返回的JSON响应
    for item in data["results"]["bindings"]:
        path = item["path"]["value"]
        print(f"Path: {path}")

# 调用函数查询两个实体之间的关系路径，并限制路径的跳数为3
get_entity_relationship_path("Q42", "Q937", 3)
