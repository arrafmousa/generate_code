import requests

def search_stackoverflow_for_pubchempy():
    page = 1
    has_more = True
    base_url = "https://api.stackexchange.com/2.3/search?"
    query_params = {
        "order": "desc",
        "sort": "votes",
        "pagesize": 100,
        "intitle": "numpy",
        "tagged": "python",
        "site": "stackoverflow"
    }
    relevant_questions = []

    while has_more:
        if len(relevant_questions) > 10:
            break
        query_params["page"] = page
        response = requests.get(base_url, params=query_params)
        data = response.json()

        # Check if the response contains the expected data
        if 'items' not in data:
            if 'error_message' in data:
                print(f"Error: {data['error_message']}")
            else:
                print("Unexpected response format. Exiting.")
            break

        for question in data["items"]:
            answers_data = requests.get(f"https://api.stackexchange.com/2.3/questions/{question['question_id']}/answers",
                                        params={"order": "desc", "sort": "votes", "site": "stackoverflow", "filter": "withbody"}).json()
            if 'items' in answers_data and answers_data['items']:
                top_answer = answers_data['items'][0]
                if "pubchempy" in top_answer["body"].lower():
                    relevant_questions.append(question)

        has_more = data.get("has_more", False)
        page += 1

    # Print the relevant question titles and links
    for question in relevant_questions:
        print(f"Question: {question['title']}")
        print(f"Link: {question['link']}")
        print('-' * 80)

if __name__ == "__main__":


    search_stackoverflow_for_pubchempy()
