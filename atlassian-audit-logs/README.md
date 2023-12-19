# Access Review with Atlassian Audit Logs

## Description
`analyze.py` is a Python script that allows you to analyze Atlassian audit logs. It provides functionality to parse and extract useful information from the logs.

## Features
- Parse Atlassian audit logs
- Extract relevant information from the logs
- Perform custom analysis on the data

## Prerequisites
- Python 3.x
- Atlassian audit logs in a supported format

## Installation
1. Clone the repository: `git clone https://github.com/your-username/analyze-atlassian-audit-logs.git`
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage
1. Place your Atlassian audit logs in the same directory as `analyze.py`.
2. Run the script: `python analyze.py`
3. Follow the prompts to select the log file and specify the analysis options.
4. The script will generate the analysis results or reports based on your selections.

## User Activity CSV Columns
The `user-activity.csv` file should include the following columns:
- `Timestamp`: The timestamp of the activity
- `User`: The username of the user performing the activity
- `Action`: The action performed by the user
- `Object`: The object or resource involved in the activity
- `Details`: Additional details or information about the activity

## Event Actions
- `jira_issue_viewed`
- `jira_issue_updated`
- `jira_issue_created`
- `confluence_page_viewed`
- `confluence_page_updated`
- `confluence_page_created`

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
