import requests

def get_entity_name(entity_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={entity_id}&format=json"
    response = requests.get(url)
    data = response.json()

    if "entities" in data:
        entity = data["entities"].get(entity_id)
        if entity and "labels" in entity:
            labels = entity["labels"]
            if "en" in labels:
                return labels["en"]["value"]

    return None

# Example usage
entity_id = "Q45"  # Replace with the ID of the entity you want to retrieve
entity_name = get_entity_name(entity_id)
if entity_name:
    print(f"The name of {entity_id} is: {entity_name}")
else:
    print(f"Could not retrieve the name for entity ID: {entity_id}")


