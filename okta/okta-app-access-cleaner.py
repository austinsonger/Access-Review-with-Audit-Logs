import pandas as pd
import sys

def convert_to_datetime(df, col):
    """
    Converts a column to datetime, handling invalid entries gracefully.
    Invalid or missing entries will be converted to NaT (Not a Time).
    """
    try:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    except Exception as e:
        print(f"Error converting {col}: {e}")
        df[col] = pd.NaT

def clean_csv(input_file, output_file):
    # Columns to focus on
    columns_of_interest = [
        'user.fullName',
        'application.name',
        'appUser.assigned',
        'appUser.recentlyAccessed',
        'group.name',
        'user.status'
    ]

    # Columns that need to be converted to datetime format
    columns_with_date_time = ['appUser.assigned', 'appUser.recentlyAccessed']

    try:
        # Load the CSV file
        df = pd.read_csv(input_file)

        # Converting specific columns to datetime format
        for col in columns_with_date_time:
            if col in df.columns:
                convert_to_datetime(df, col)

        # Selecting only the columns of interest
        cleaned_df = df[columns_of_interest]

        # Saving the cleaned dataframe to a new CSV file
        cleaned_df.to_csv(output_file, index=False)
        print(f"File cleaned and saved as: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_csv.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        clean_csv(input_file, output_file)
