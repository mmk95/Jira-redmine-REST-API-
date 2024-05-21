import requests
import json

redmine_base_url = 'https://redmine.vidanet.hu'
api_key = 'Token'

search_subject = 'API test'
search_url = f"{redmine_base_url}/issues.json"
search_payload = {
    'subject': search_subject
}

def issue_exists():
    response = requests.get(
        search_url,
        headers={
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': api_key
        },
        params=search_payload
    )

    if response.status_code == 200:
        search_results = response.json()
        if search_results['total_count'] > 0:
            return True
        else:
            return False

def redmine_issue(description):
    if issue_exists():
        search_payload['limit'] = 1
        response = requests.get(
            search_url,
            headers={
                'Content-Type': 'application/json',
                'X-Redmine-API-Key': api_key
            },
            params=search_payload
        )
        existing_issue = response.json()['issues'][0]
        issue_id = existing_issue['id']
        existing_description = existing_issue['description']

        new_description = description
        if new_description not in existing_description:
            new_description = f"{existing_description}\n{new_description}"

            update_url = f"{redmine_base_url}/issues/{issue_id}.json"
            update_payload = {
                'issue': {
                    'description': new_description
                }
            }

            response = requests.put(
                update_url,
                headers={
                    'Content-Type': 'application/json',
                    'X-Redmine-API-Key': api_key
                },
                data=json.dumps(update_payload)
            )

        if response.status_code == 200:
            return description
    else:
        issue_data = {
            'issue': {
                'project_id': 'cypress-tests',
                'subject': search_subject,
                'description': description,
                'tracker_id': 'Bud',
                'status_id': 'New',
                'priority_id': 4
            }
        }

        response = requests.post(
            f"{redmine_base_url}/issues.json",
            headers={
                'Content-Type': 'application/json',
                'X-Redmine-API-Key': api_key
            },
            data=json.dumps(issue_data)
        )

        if response.status_code == 201:
            return description

description = 'asd'

result = redmine_issue(description)
