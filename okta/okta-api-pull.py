import requests
import logging
import csv
import time

API_TOKEN = "your_api_token"  # Replace with your actual API token
OKTA_DOMAIN = "your_okta_domain"  # Replace with your Okta domain
OUTPUT_FILE = "okta_user_applications.csv"

# Configure logging
logging.basicConfig(filename='okta_api.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_RETRIES = 3
RATE_LIMIT_STATUS_CODE = 429
RATE_LIMIT_DELAY = 60  # seconds

def handle_api_call(url, headers):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == RATE_LIMIT_STATUS_CODE:
                logging.warning("Rate limit reached. Retrying after delay...")
                time.sleep(RATE_LIMIT_DELAY)
                retries += 1
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API call failed: {e}")
            return None
    logging.error("Max retries exceeded. API call failed.")
    return None
def get_active_users():
    users = []
    url = f"https://{OKTA_DOMAIN}/api/v1/users?filter=status eq \"ACTIVE\""
    headers = {'Authorization': f'SSWS {API_TOKEN}'}

    while url:
        data = handle_api_call(url, headers)
        if data is None:
            break
        users.extend(data)

        # Okta uses link headers for pagination
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None

    return users

def get_user_applications(user_id):
    url = f"https://{OKTA_DOMAIN}/api/v1/users/{user_id}/appLinks"
    headers = {'Authorization': f'SSWS {API_TOKEN}'}
    return handle_api_call(url, headers)

def list_okta_applications(api_token, okta_domain):
    url = f"https://{okta_domain}/api/v1/apps"
    headers = {'Authorization': f'SSWS {api_token}'}
    applications = handle_api_call(url, headers)
    if applications is not None:
        for app in applications:
            logging.info(f"Application: {app['label']}")

def review_user_accounts(api_token, okta_domain):
    url = f"https://{okta_domain}/api/v1/users"
    headers = {'Authorization': f'SSWS {api_token}'}
    users = handle_api_call(url, headers)
    if users is not None:
        for user in users:
            logging.info(f"User: {user['profile']['login']}")
            logging.info(f"Status: {user['status']}")
            logging.info("------")

def analyze_group_memberships(api_token, okta_domain, user_id):
    url = f"https://{okta_domain}/api/v1/users/{user_id}/groups"
    headers = {'Authorization': f'SSWS {api_token}'}
    groups = handle_api_call(url, headers)

    expected_roles = ['Role1', 'Role2', 'Role3']  # Replace with your expected set of roles
    expected_functions = ['Function1', 'Function2', 'Function3']  # Replace with your expected set of functions

    if groups is not None:
        for group in groups:
            group_name = group['profile']['name']
            group_roles = group.get('roles', [])
            group_functions = group.get('functions', [])

            logging.info(f"User: {user_id}")
            logging.info(f"Group: {group_name}")

            # Compare roles
            for role in expected_roles:
                if role in group_roles:
                    logging.info(f"Role: {role} - Membership is valid.")
                else:
                    logging.warning(f"Role: {role} - Membership is invalid.")

            # Compare functions
            for function in expected_functions:
                if function in group_functions:
                    logging.info(f"Function: {function} - Membership is valid.")
                else:
                    logging.warning(f"Function: {function} - Membership is invalid.")

            logging.info("------")

def validate_role_assignments(api_token, okta_domain):
    url = f"https://{okta_domain}/api/v1/roles"
    headers = {'Authorization': f'SSWS {api_token}'}
    roles = handle_api_call(url, headers)

    expected_roles = ['Role1', 'Role2', 'Role3']  # Replace with your expected set of roles

    if roles is not None:
        for role in roles:
            role_id = role['id']
            role_name = role['displayName']

            if role_name in expected_roles:
                logging.info(f"Role: {role_name}")
                logging.info(f"Role ID: {role_id}")
                logging.info("Role assignment is valid.")
            else:
                logging.warning(f"Role: {role_name}")
                logging.warning(f"Role ID: {role_id}")
                logging.warning("Role assignment is invalid.")
            logging.info("------")


def main():
    api_token = "your_api_token"  # Replace with your actual API token
    okta_domain = "your_okta_domain"  # Replace with your Okta domain
    output_file = "okta_user_applications.csv"

    try:
        active_users = get_active_users(api_token, okta_domain)
        list_okta_applications(api_token, okta_domain)
        review_user_accounts(api_token, okta_domain)
        analyze_group_memberships(api_token, okta_domain)
        validate_role_assignments(api_token, okta_domain)

        data_to_export = []
        for user in active_users:
            user_id = user['id']
            apps = get_user_applications(api_token, okta_domain, user_id)
            if apps is not None:
                for app in apps:
                    data_to_export.append({
                        "User Login": user['profile']['login'],
                        "App Name": app['label'],
                        "Assigned Date": app.get('date', 'N/A')  # Replace 'date' with the actual key if different
                    })

        # Writing data to a CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["User Login", "App Name", "Assigned Date"], quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(data_to_export)

        logging.info(f"Data exported to {output_file}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
