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

