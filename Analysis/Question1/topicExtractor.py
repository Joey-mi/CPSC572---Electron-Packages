# This program extractss the package.json from GitHub

# Token: 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

import requests
import time
import re

def main():
    access_token = "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"

    errors = 0
    fetched = 0
    with open('undone.txt', 'r') as file, open('repoTopics.txt', 'w') as topics, open('repoDescriptions.txt', 'w') as descriptions, open('errors.txt', 'w') as errorsFile:
    
        line = file.readline()
        while line:
            repo_name = line.strip()

            url = f'https://api.github.com/repos/{repo_name}'
            headers = {'Authorization': f'token {access_token}'}
            time.sleep(1.2)
            try:
                print(f"GET: {url}")
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    topic = response.json()['topics']
                    description = response.json()['description']
                    description = re.sub(r'[^\x00-\x7F]+', '', description)
                    time.sleep(1.2)
                    topics.write(f"{repo_name}\t\t{topic}\n")
                    descriptions.write(f"{repo_name}\t\t{description}\n")
                    fetched += 1
                    print(f"    Fetched {repo_name}, {len(topic)}. Errors: {errors}, Fetched: {fetched}")
                else:
                    errors += 1
                    print(f"    Failure: {repo_name}. Errors: {errors}, Fetched: {fetched}")
                    errorsFile.write(f"get, {repo_name}\n")
            except Exception as e:
                errors += 1
                print(f"    Exception: {e} --- {repo_name}. Errors: {errors}, Fetched: {fetched}")
                errorsFile.write(f"exception, {repo_name} {e}\n")
            line = file.readline()
    print(f"Finished with Errors: {errors}, Fetched: {fetched}")


if __name__ == "__main__":
    main()