import csv
import os

# Define the input and output directories
input_directory = r'...\NFL\PPG and Pythagorean Wins\Points_Per_Year\Scraped data'
output_directory = r'...\NFL\PPG and Pythagorean Wins\Points_Per_Year\Scrubbed data'

# Loop through the years
for year in range(2000, 2023):
    # Define the file paths
    input_file = os.path.join(input_directory, f"{year}.txt")
    output_file = os.path.join(output_directory, f"{year}_scrubbed.csv")

    # Read the content of the file
    with open(input_file, "r") as file:
        content = file.read()

    # Define text block for AFC in years without ties
    AfcNoTies_block = '''AFC Standings 
* - division winner, + - wild card Share & Export
Modify, Export & Share Table
Get as Excel Workbook
Get table as CSV (for Excel)
Get Link to Table
About Sharing Tools
Video: SR Sharing Tools & How-to
Video: Stats Table Tips & Tricks
Data Usage Terms
Glossary
Tm	W	L	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS'''

    # Define text block for NFC in years without ties
    NfcNoTies_block = '''NFC Standings 
* - division winner, + - wild card Share & Export
Modify, Export & Share Table
Get as Excel Workbook
Get table as CSV (for Excel)
Get Link to Table
About Sharing Tools
Video: SR Sharing Tools & How-to
Video: Stats Table Tips & Tricks
Data Usage Terms
Glossary
Tm	W	L	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS'''

    # Remove unwanted text block for AFC in years with ties
    AfcTies_block = '''AFC Standings 
* - division winner, + - wild card Share & Export
Modify, Export & Share Table
Get as Excel Workbook
Get table as CSV (for Excel)
Get Link to Table
About Sharing Tools
Video: SR Sharing Tools & How-to
Video: Stats Table Tips & Tricks
Data Usage Terms
Glossary
Tm	W	L	T	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS'''
    
    # Remove unwanted text block for NFC in years with ties
    NfcTies_block = '''NFC Standings 
* - division winner, + - wild card Share & Export
Modify, Export & Share Table
Get as Excel Workbook
Get table as CSV (for Excel)
Get Link to Table
About Sharing Tools
Video: SR Sharing Tools & How-to
Video: Stats Table Tips & Tricks
Data Usage Terms
Glossary
Tm	W	L	T	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS'''

    # Remove unwanted text blocks
    content = content.replace(AfcNoTies_block, '').replace(NfcNoTies_block, '').replace(AfcTies_block,'').replace(NfcTies_block,'')
    
    # Split the content by lines
    lines = content.split('\n')

    # Initialize variables for division and playoffs
    current_division = ""
    playoffs = ""

    # Prepare the data
    data = []

    # Iterate through the lines
    for line in lines:
        # Check if the line is a division name
        if line.startswith(('AFC', 'NFC')):
            current_division = line.strip()
        else:
            # Check if the line contains team information
            if line:
                team_info = line.split('\t')
                team_name = team_info[0]
                playoffs = ""

                # Determine playoffs status
                if '*' in team_name:
                    playoffs = "divwin"
                elif '+' in team_name:
                    playoffs = "wildcard"
                else:
                    playoffs = "missed"

                # Remove '+' and '*' from team names
                team_name = team_name.replace('+', '').replace('*', '')

                # Add division, playoffs, and year columns
                updated_line = [team_name] + team_info[1:] + [current_division, playoffs, str(year)]
                data.append(updated_line)

    # Add 16th column if there are 15 columns
    if len(data[0]) == 15:
        for i in data:  # Skip the header line
            #row_data = data[i].split('\t')
            i.insert(3, '0')  # Insert '0' in the 4th position
            #lines[i] = '\t'.join(row_data)

    content = '\n'.join(lines)

        
    # Write the data to a CSV file
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
