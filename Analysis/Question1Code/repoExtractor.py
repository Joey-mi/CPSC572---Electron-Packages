import requests
import time

def main():
    access_token = ""

    topic = "electron"
    entries_per_page = 100
    errors = 0
    errorArr = []
    fetched = 0
    with open('electronRepos.txt', 'w') as file:
    # Write data to the file
        for year in range(2013, 2025):
            for month in range(1, 13):
                month = ("0" + str(month)) if month < 10 else month
                next_request_url = f'https://api.github.com/search/repositories?q=topic:{topic}+created:{year}-{month}..{year}-{month}&per_page={entries_per_page}'
        
                while (True):
                    print(f"GET: {next_request_url}")
                    # Wait 1.2 seconds before sending another response
                    time.sleep(1.2)
                    response = requests.get(next_request_url, headers={'Authorization': f'token {access_token}'})
                    if response.status_code == 200:
                        repos = response.json()['items']

                        for repo in repos:
                            repo_name = repo['full_name']
                            print(f"    Fetched: {repo_name}")
                            file.write(f"{repo_name}\n")
                            fetched += 1

                        link = response.headers.get("Link")
                        if link:
                            links = link.split(",")

                            next_link = None
                            for link in links:
                                if 'rel="next"' in link:
                                    next_link = link
                                    break

                            if next_link:
                                print(" Next page")
                                url, params = next_link.split(';')
                                next_request_url = url.strip(' <>')
                            else:
                                # break the loop if there is no next page
                                break
                        else:
                            # break the loop if there is no next page
                            break
                    else:
                        errors += 1
                        print(f"Failed to fetch repositories. {year}-{month} Status code: {response}")
                        errorArr.append(next_request_url)
                        break
    print(f"Finished with Errors: {errors}, Fetched: {fetched}")


if __name__ == "__main__":
    main()