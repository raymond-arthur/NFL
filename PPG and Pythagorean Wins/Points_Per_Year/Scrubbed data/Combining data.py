import pandas as pd
import glob

# Step 1: Get a list of all CSV files in the directory
csv_files = glob.glob('C:\\Users\\Arthur Raymond\\Desktop\\NFL\\PPG and Pythagorean Wins\\Points_Per_Year\\Scrubbed data\\*.csv')

# Step 2: Create an empty list to store the DataFrames
dfs = []

# Step 3: Loop through the CSV files and read them into DataFrames
for csv_file in csv_files:
    df = pd.read_csv(csv_file, header=None)  # Set header to None to ignore existing headers
    dfs.append(df)

# Step 4: Concatenate the DataFrames into one large DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Set column names
combined_df.columns = [
    'Team', 'Win', 'Loss', 'Tie', 'Win%', 'PF', 'PA', 'PD', 
    'MoV', 'SoS', 'SRS', 'OSRS', 'DSRS', 'Div', 'PlayoffRes', 'Year'
]

# Print the combined DataFrame
print(combined_df)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_data.csv', index=False)
