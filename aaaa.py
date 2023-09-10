import requests
import re


def search_github_for_pubchempy():
    base_url = "https://api.github.com/search/repositories?q=pubchempy+in:file&sort=stars&order=desc"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # Uncomment and set your GitHub token for a higher rate limit.
        "Authorization": "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"
    }

    r = requests.get(base_url, headers=headers)

    if r.status_code != 200:
        print("Error accessing the GitHub API.")
        return

    repo_items = r.json()['items']

    for repo in repo_items:
        owner = repo['owner']['login']
        repo_name = repo['name']

        search_code_url = f"https://api.github.com/search/code?q=pubchempy+in:file+repo:{owner}/{repo_name}"
        r_code = requests.get(search_code_url, headers=headers)

        if r_code.status_code != 200:
            print(f"Error accessing the code of {owner}/{repo_name}.")
            continue

        code_items = r_code.json().get('items', [])

        for code in code_items:
            file_url = code['html_url']
            print(f"Checking file: {file_url}")

            file_content = requests.get(code['git_url'], headers=headers).json().get('content', '')
            decoded_content = requests.utils.unquote(file_content)

            # Extract comments from the content
            triple_double_quotes_comments = re.findall(r'""".*?"""', decoded_content, re.DOTALL)
            single_comments = re.findall(r'#.*', decoded_content)

            for comment in triple_double_quotes_comments + single_comments:
                print(comment)


if __name__ == "__main__":
    search_github_for_pubchempy()
