import json

import requests

def search_stackoverflow_questions(keyword, page_size=10):
    base_url = "https://api.stackexchange.com/2.3/search"
    params = {
        "order": "desc",
        "sort": "activity",
        "site": "stackoverflow",
        "pagesize": page_size,
        "intitle": keyword
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return None


import json
import os

def read_or_create_json(file_name, default_data=None):
    if default_data is None:
        default_data = {}

    # Check if file exists
    if os.path.exists(file_name):
        with open(file_name, 'r') as json_file:
            try:
                data = json.load(json_file)
                return data
            except json.JSONDecodeError:
                # If there's a decoding error, return the default data
                return default_data
    else:
        # If file doesn't exist, create it with default data
        with open(file_name, 'w') as json_file:
            json.dump(default_data, json_file, indent=4)
        return default_data

file_name = 'package_queries_sof.json'
data = read_or_create_json(file_name)

# Usage
keyword = "pubchempy"
results = search_stackoverflow_questions(keyword)

new_data = []

if results:
    for item in results:
        if 'error' in item['title'].lower():
            continue
        new_data.append(item['title'])
        print(f"Question ID: {item['question_id']}")
        print(f"Title: {item['title']}")
        print(f"Link: https://stackoverflow.com/q/{item['question_id']}")
        print('-----')
else:
    print("No results found or an error occurred.")

data[keyword] = new_data
with open(file_name, 'w') as json_file:
    json.dump(data, json_file, indent=4)



