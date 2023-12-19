import requests

def get_active_users(api_token, okta_domain):
    users = []
    url = f"https://{okta_domain}/api/v1/users?filter=status eq \"ACTIVE\""
    headers = {'Authorization': f'SSWS {api_token}'}

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        users.extend(data)

        # Okta uses link headers for pagination
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None

    return users

def get_user_applications(api_token, okta_domain, user_id):
    url = f"https://{okta_domain}/api/v1/users/{user_id}/appLinks"
    headers = {'Authorization': f'SSWS {api_token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    api_token = "your_api_token"  # Replace with your actual API token
    okta_domain = "your_okta_domain"  # Replace with your Okta domain

    active_users = get_active_users(api_token, okta_domain)

    for user in active_users:
        user_id = user['id']
        apps = get_user_applications(api_token, okta_domain, user_id)
        print(f"User: {user['profile']['login']}")
        for app in apps:
            print(f"  App: {app['label']}, Assigned: {app['date']}")  # Adjust based on actual API response format

if __name__ == "__main__":
    main()
