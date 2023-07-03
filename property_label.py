import requests

def get_property_label(property_id):
    url = "https://query.wikidata.org/sparql"

    query = f"""
    SELECT ?propertyLabel
    WHERE {{
      wd:{property_id} rdfs:label ?propertyLabel .
      FILTER(LANG(?propertyLabel) = 'en')
    }}
    """

    params = {
        "format": "json",
        "query": query
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 解析返回的JSON响应
    label = data["results"]["bindings"][0]["propertyLabel"]["value"]
    print(label)

# 调用函数获取属性的名称
get_property_label("P106")
