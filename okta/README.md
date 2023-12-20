# Access Review using Okta API

## Overview
This script interacts with the Okta API to fetch and analyze user data, application assignments, group memberships, and role assignments. It also exports relevant data to a CSV file for reporting and analysis purposes.

## Features
- Retrieve active users from Okta.
- List all applications integrated with Okta.
- Review user account status.
- Analyze group memberships and validate against expected roles and functions.
- Validate role assignments for users.
- Export gathered data to a CSV file.

## Configuration
The script requires a configuration file (`config.ini`) with the following structure:

```ini
[Okta]
API_TOKEN = Your_Okta_API_Token
OKTA_DOMAIN = Your_Okta_Domain
```

## Usage

1. Ensure Python 3.x is installed on your system.
2. Install required Python libraries: `requests` and `configparser`.
3. Place `config.ini` in the same directory as the script with appropriate Okta credentials.
4. Run the script: `python okta_api.py`

## Function Descriptions

- `handle_api_call`: Manages API calls to Okta, handles rate limiting and errors.
- `get_active_users`: Retrieves a list of active users from Okta.
- `get_user_applications`: Fetches applications assigned to a specific user.
- `list_okta_applications`: Lists all applications in Okta.
- `review_user_accounts`: Reviews and logs user account details.
- `analyze_group_memberships`: Analyzes and validates group memberships of users.
- `validate_role_assignments`: Validates role assignments against expected roles.
- `get_role_permissions`: Retrieves permissions for a specified role in Okta.
- `main`: Main function that orchestrates the execution of the script.


## Structure of roles_and_functions.json

- `expected_roles` is an array listing the roles that the script will check for in Okta groups or user assignments. These roles are likely predetermined by your organization's policies or the specific requirements of the script.
- `expected_functions` lists the functions or permissions associated with these roles. These could be actions that users with the specified roles are expected to perform or have permissions for in the Okta environment.

The primary purpose of roles_and_functions.json in the context of the script is to provide a reference for validating user group memberships and role assignments in Okta.

- `Analyze Group Memberships`: It uses the roles and functions defined in this file to check if users are correctly assigned to groups in Okta. For example, it could verify that a user in an "Admin" group has the expected "Admin" role.
- `Validate Role Assignments`: It uses this file to ensure that users have appropriate roles and that these roles align with their expected functions or permissions.
- `Reporting and Logging`: It can log information about whether users' roles and functions in Okta match those listed in the roles_and_functions.json file, highlighting any discrepancies.
- `Customization`: This file allows for easy customization to fit different organizational structures or role definitions without needing to alter the  source code.

Since `roles_and_functions.json` is a separate file, it can be updated independently of the script. This allows for flexibility in managing role and function definitions as organizational needs change, without the need to modify the script itself.

In summary, `roles_and_functions.json` serves as a crucial data source for the Okta API Pull Script, providing the necessary context for validating user roles and functions in an Okta environment.


## Logging

Logs are written to `okta_api.log` in the same directory as the script. The log includes details about script operations, API interactions, and any errors or warnings encountered.

## CSV Export

The script exports data to `okta_user_applications.csv` in the script's directory. The CSV file contains columns for user login, application name, and assigned date.

## Error Handling

The script includes comprehensive error handling to manage API rate limits, invalid responses, and network issues.

## Security Notes

- Store `config.ini` securely as it contains sensitive API tokens.
- Regularly rotate your Okta API tokens and update `config.ini` accordingly.

## Disclaimer

This script is provided as-is, and its operation should be thoroughly tested in a controlled environment before use in production.

