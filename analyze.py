import pandas as pd

def analyze_user_activity(activity_file, output_file, relevant_actions=None):
    """
    Analyzes user activity from the activity file and saves the summary to the output file.
    
    Args:
        activity_file (str): Path to the CSV file containing activity data.
        output_file (str): Path to the output CSV file where the summary will be saved.
        relevant_actions (list, optional): List of relevant actions to filter. Defaults to a predefined list.

    Returns:
        None
    """
    try:
        # Define default actions if not provided
        if relevant_actions is None:
            relevant_actions = [
                'jira_issue_viewed',
                'jira_issue_updated',
                'jira_issue_created',
                'confluence_page_viewed',
                'confluence_page_updated',
                'confluence_page_created'
            ]

        # Load the activity data
        activity_df = pd.read_csv(activity_file)

        # Filter the activity dataframe based on relevant actions
        filtered_activity_df = activity_df[activity_df['Action'].isin(relevant_actions)]

        # Select relevant columns
        relevant_columns = ['Actor', 'Action']
        filtered_activity_df = filtered_activity_df[relevant_columns]

        # Grouping and counting occurrences
        activity_summary = filtered_activity_df.groupby(['Actor', 'Action']).size().unstack(fill_value=0)

        # Ensure all required actions are present as columns
        for action in relevant_actions:
            if action not in activity_summary.columns:
                activity_summary[action] = 0

        # Reorder columns as per the required format
        activity_summary = activity_summary[relevant_actions]

        # Reset index to get 'Actor' as a column and rename columns
        activity_summary.reset_index(inplace=True)
        column_names = {
            'Actor': 'User',
            # Add mappings for other columns as required
        }
        activity_summary.rename(columns=column_names, inplace=True)

        # Save the summary to a CSV file
        activity_summary.to_csv(output_file, index=False)
        print(f"Analysis complete. Summary saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
analyze_user_activity('user-activity.csv', 'activity_summary.csv')
