# This program extractss the package.json from GitHub

# Token: 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

import requests
import time

def main():
    access_token = "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"

    errors = 0
    fetched = 0
    file_path = "package.json"
    with open('electronRepos.txt', 'r') as file, open('repoPackagesDev.txt', 'w') as packages, open('errors.txt', 'w') as errorsFile:
    
        line = file.readline()
        while line:
            repo_name = line.strip()

            url = f'https://api.github.com/repos/{repo_name}/contents/{file_path}'
            headers = {'Authorization': f'token {access_token}'}
            time.sleep(1.2)
            try:
                print(f"GET: {url}")
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    download_url = response.json()['download_url']
                    time.sleep(1.2)
                    downloaded_response = requests.get(download_url, headers=headers)
                    if downloaded_response.status_code == 200:
                        downloaded_json = downloaded_response.json()
                        fetched += 1
                        if "devDependencies" in downloaded_json:
                            dependencies = downloaded_json["devDependencies"]
                            packages.write(f"{repo_name}, {dependencies}\n")
                            print(f"    Fetched {repo_name}, {len(dependencies)}. Errors: {errors}, Fetched: {fetched}")
                        else:
                            packages.write(f"{repo_name}, 0\n")
                    else:
                        errors += 1
                        print(f"    Failed to download: {repo_name}. Errors: {errors}, Fetched: {fetched}")
                        errorsFile.write(f"download, {repo_name}\n")
                else:
                    errors += 1
                    print(f"    Failed to find package.json: {repo_name}. Errors: {errors}, Fetched: {fetched}")
                    errorsFile.write(f"find, {repo_name}\n")
            except Exception as e:
                errors += 1
                print(f"    Exception: {e} --- {repo_name}. Errors: {errors}, Fetched: {fetched}")
                errorsFile.write(f"exception, {repo_name}\n")
            line = file.readline()
    print(f"Finished with Errors: {errors}, Fetched: {fetched}")


if __name__ == "__main__":
    main()