import requests
import logging
import csv
import time
import configparser
import requests
import sys
import json

# Read configuration file
config = configparser.ConfigParser()

if not config.read('config.ini'):
    logging.error("config.ini file not found or could not be read.")
    # Handle the error here, such as exiting the script or using default values.
    sys.exit(1)

# Check if required keys are present
if 'Okta' not in config or 'API_TOKEN' not in config['Okta'] or 'OKTA_DOMAIN' not in config['Okta']:
    logging.error("Required keys not found in config.ini.")
    # Handle the error here, such as exiting the script or using default values.
    sys.exit(1)


API_TOKEN = config.get('Okta', 'API_TOKEN')
OKTA_DOMAIN = config.get('Okta', 'OKTA_DOMAIN')
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

            # Validate response data
            data = response.json()
            if not isinstance(data, list):
                logging.error(f"API response is not a list: {data}")
                return None
            for item in data:
                if 'id' not in item or 'profile' not in item or 'login' not in item['profile']:
                    logging.error(f"API response item is missing required fields: {item}")
                    return None
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"API call failed: {e}")
            retries += 1

    logging.error("API call failed after retries. Halting the script or handle it more gracefully.")
    return None


def get_active_users():
    users = []
    url = f"https://{OKTA_DOMAIN}/api/v1/users?filter=status eq \"ACTIVE\""
    headers = {'Authorization': f'SSWS {API_TOKEN}'}

    while url:
        data = handle_api_call(url, headers)  # Define data variable in the correct scope
        if data is None:
            break
        users.extend(data)

        # Okta uses link headers for pagination
        if 'next' in data.links:
            url = data.links['next']['url']
        else:
            url = None

    return users

def get_user_applications(user_id):
    url = f"https://{OKTA_DOMAIN}/api/v1/users/{user_id}/appLinks"
    headers = {'Authorization': f'SSWS {API_TOKEN}'}
    return handle_api_call(url, headers)

def list_okta_applications(api_token, okta_domain):
    url = f"https://{OKTA_DOMAIN}/api/v1/apps"
    headers = {'Authorization': f'SSWS {API_TOKEN}'}
    applications = handle_api_call(url, headers)
    if applications is not None:
        for app in applications:
            logging.info(f"Application: {app['label']}")

def review_user_accounts(api_token, okta_domain):
    url = f"https://{OKTA_DOMAIN}/api/v1/users"
    headers = {'Authorization': f'SSWS {API_TOKEN}'}
    users = handle_api_call(url, headers)
    if users is not None:
        for user in users:
            logging.info(f"User: {user['profile']['login']}")
            logging.info(f"Status: {user['status']}")
            logging.info("------")

def load_roles_and_functions():
    with open('roles_and_functions.json', 'r') as file:
        data = json.load(file)
    return data['expected_roles'], data['expected_functions']

def analyze_group_memberships(api_token, okta_domain, user_id):
    """
    Analyzes the group memberships of a user in Okta.

    Parameters:
    - api_token (str): The Okta API token.
    - okta_domain (str): The Okta domain.
    - user_id (str): The ID of the user.

    Returns:
    None
    """
    url = f"https://{OKTA_DOMAIN}/api/v1/users/{user_id}/groups"
    headers = {'Authorization': f'SSWS {API_TOKEN}'}
    groups = []

    while url:
        data = handle_api_call(url, headers)
        if data is None:
            break
        groups.extend(data)

        # Okta uses link headers for pagination
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None

    expected_roles, expected_functions = load_roles_and_functions()

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
    url = f"https://{OKTA_DOMAIN}/api/v1/roles"
    headers = {'Authorization': f'SSWS {API_TOKEN}'}
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


def get_role_permissions(api_token, okta_domain, role_id):
    url = f"https://{okta_domain}/api/v1/roles/{role_id}/permissions"
    headers = {'Authorization': f'SSWS {api_token}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        permissions = response.json()
        return permissions
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve role permissions for role ID {role_id}: {e}")
        return None


def main():
    """
    Main function to execute the Okta API pull script.

    This function retrieves active users, lists Okta applications,
    reviews user accounts, analyzes group memberships, and validates
    role assignments. It then exports the data to a CSV file.

    :return: None
    """
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

    except FileNotFoundError:
        logging.error("config.ini file not found.")
        # Handle the error here, such as exiting the script or using default values.

    except KeyError:
        logging.error("Required keys not found in config.ini.")
        # Handle the error here, such as exiting the script or using default values.

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the API call: {str(e)}")
        # Handle the error here, such as retrying the API call or logging the error.

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
