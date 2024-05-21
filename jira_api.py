import requests

jira_base_url = "https://cypresstestexample.atlassian.net"
username = "email"
password = "Jira token"

search_summary = "Test issue"

search_url = f"{jira_base_url}/rest/api/2/search"
search_payload = {
    "jql": f'summary ~ "{search_summary}"',
    "fieldsByKeys": False
}

def issue_exists():
    response = requests.post(
        search_url,
        auth=(username, password),
        headers={"Content-Type": "application/json"},
        json=search_payload
    )

    if response.status_code == 200:
        search_results = response.json()
        if search_results['total'] > 0:
            return True
        else:
            return False

def jira_issue(description):
    response = requests.post(
        search_url,
        auth=(username, password),
        headers={"Content-Type": "application/json"},
        json=search_payload
    )

    if response.status_code == 200:
        search_results = response.json()
        if search_results['total'] > 0:
            existing_issue = search_results['issues'][0]
            issue_key = existing_issue['key']
            existing_description = existing_issue['fields'].get('description', '')

            new_description = description
            if new_description not in existing_description:
                new_description = f"{existing_description}, {new_description}"

                update_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}"
                update_payload = {
                    "fields": {
                        "description": new_description
                    }
                }

                response = requests.put(
                    update_url,
                    auth=(username, password),
                    headers={"Content-Type": "application/json"},
                    json=update_payload
                )
            else:
                print("Description is in existing description")

            if response.status_code == 204:
                return description
            else:
                print(f"Error updating description: {response.text}")
        else:
            issue_data = {
                "fields": {
                    "project": {"key": "CT"},
                    "summary": search_summary,
                    "description": description,
                    "priority": {"name": "Highest"},
                    "issuetype": {"name": "Bug"}
                }
            }

            response = requests.post(
                f"{jira_base_url}/rest/api/2/issue",
                auth=(username, password),
                headers={"Content-Type": "application/json"},
                json=issue_data
            )

            if response.status_code == 201:
                return description
            else:
                print(f"Error creating issue: {response.text}")
    else:
        print(f"Error searching for existing issues: {response.text}")

