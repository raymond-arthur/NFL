Note: PFR no longer allows for webpage scraping. The data was obtained via scraping prior to this change being enacted by PFR.

While some parts of the code may talk about scraping, please note that if you attempt to scrape from PFR, you will get a 403 error. 

It is recommended to use R or python libraries (CRAN's NFLreadr, nfl-data-py). The stats and information will all be the same, only the method of obtaining them will differ.

# NFL and Pythagorean wins

## Project Main Goal

Using python (and optionally R for analysis), fetch historical team data of wins, losses, ties, points scored, points against, and other relevant stats teams from 2000 to 2022.
Using that data, calculate the Pythagorean wins (pWins) for each team and then analyze and potentially optimize the formula for pWins (current pWins exponent = 2) to better estimate 'deserved' wins.

## General Notes and Information


### What are Pythagorean wins?
The Wikipedia link for Pythagorean wins [can be found here](https://en.wikipedia.org/wiki/Pythagorean_expectation).

The goal of the formula is to determine, based solely on points scored and points allowed, what the 'deserved' winning percentage should be.

Given the following
- dWins = deserved wins
- PF = points for (also referred to as points scored)
- PA = points against (also referred to as points given up, or points allowed)
- GP = Games played during that season

The formula is as follows:

```math
dWins = \frac{PF^2}{PF^2 + PA^2} * GP
```

Notes:
- The exponent value comes from the concept of a better team having a higher 'quality' of games, and a higher 'quality' will equate, in the long term, to winning more games. Essentially, a better team scores more often and gives up less points than a worse team.
- The exponent value is taken directly from previous derivations in baseball. Decades of work have gone into understanding this value and what it means in the context of baseball, starting in the early 80s with Bill James.  
- The exponent value of 2 is what we are trying to optimize -- Pro Football Outsiders has already done work on this and has obtained their own value of 2.37.
- The value of the exponent can potentially be equated to how much 'luck' or variance is present in the sport: a game with more variance may reward 'better' teams less often than a game with much less variance.


Essentially we are asking the question: "based on data from 2000 to 2022, what is the best estimation of the dWins exponent" 

We can expand this to certain questions such as :
- What does that say about certain team's performances in specific years?
- How much variance is present in football compared to other sports?



### Ties
In the regular season, there are three game outcomes: wins, losses, and ties. For the purposes of Pythagorean wins (and Win% to some extent), ties are counted as 0.5 wins *and* 0.5 losses for both teams, which keeps the result of 1 total win and 1 total loss per game on aggregate.

### Scraping

All NFL stats were scraped from [Pro Football Reference](https://pro-football-reference.com/).

Scraping was done on pages ```/years/<YEAR>``` from 2000 to 2022.

Several interesting notes:
- From 1995 to 2002 there were 31 teams. The Texans were added in 2002.
- There was a division realignment in 2002, going from 5-team divisions to 8 4-team divisions. 

These do not necessarily affect any of our analyses about pWins, however they are interesting to note (and the old division names will pop up in the 2000 and 2001 data). It is worth considering removing years 2000 and 2001.

##### Why 2000-2022?
There have been many rule changes in the past 20-30 years that have affected our primary variables of interest (points scored and points against). Total points scored per game have gone up in a fairly linear and consistent manner over that time frame. More thought can be put into what year cutoff to use while keeping in mind that large sample size may be more beneficial for higher confidence in our pWins exponent.


##### Scraping in years with ties
PFR generates tables for yearly results in the following manner:
- if there are no ties that year, the listed stats are 

		Tm	W	L		W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS

- if there is at least 1 tie in any game that year, the listed stats are

		Tm	W	L	T	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS

Notice that there is simply one less column generated in tables for years without ties, something that we rectify by simply adding a column that contains all 0s in years without ties.





## Code breakdown

Let's start off with an example from two different years of the year-end results from the regular season.

A few important background things to know:
- From 2000 until 2020, teams played 16 games per season. In 2021 and 2022, teams played 17 games. We can easily track how many games a team played in a year (in the regular season) but summing their wins, losses, and ties.





#### Scraping, tackling the ties vs no ties years, and scrubbing the data

As noted at the start, PFR no longer allows for scraping data directly from their website.
While a combination of `BeautifulSoup` and `pandas` was used in our case, the code will no longer work and therefore will not be discussed. A good breakdown similar to how it was achieved can be found [here](https://stmorse.github.io/journal/pfr-scrape-python.html).


As noted above, PFR generates tables differently in years with and without ties. Let's take a look:

<details>
<summary> A year with no ties (2000) </summary>
```
AFC Standings 
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
Tm	W	L	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS
AFC East
Miami Dolphins*	11	5	.688	323	226	97	6.1	1.0	7.1	0.0	7.1
Indianapolis Colts+	10	6	.625	429	326	103	6.4	1.5	7.9	7.1	0.8
New York Jets	9	7	.563	321	321	0	0.0	3.5	3.5	1.4	2.2
Buffalo Bills	8	8	.500	315	350	-35	-2.2	2.2	0.0	0.5	-0.5
New England Patriots	5	11	.313	276	338	-62	-3.9	1.4	-2.5	-2.7	0.2
AFC Central
Tennessee Titans*	13	3	.813	346	191	155	9.7	-1.3	8.3	1.5	6.8
Baltimore Ravens+	12	4	.750	333	165	168	10.5	-2.5	8.0	0.0	8.0
Pittsburgh Steelers	9	7	.563	321	255	66	4.1	-0.2	3.9	0.6	3.3
Jacksonville Jaguars	7	9	.438	367	327	40	2.5	-1.4	1.1	3.2	-2.1
Cincinnati Bengals	4	12	.250	185	359	-174	-10.9	0.4	-10.5	-8.1	-2.4
Cleveland Browns	3	13	.188	161	419	-258	-16.1	1.5	-14.6	-9.1	-5.5
AFC West
Oakland Raiders*	12	4	.750	479	299	180	11.3	-1.5	9.7	8.0	1.8
Denver Broncos+	11	5	.688	485	369	116	7.3	-2.2	5.0	7.8	-2.7
Kansas City Chiefs	7	9	.438	355	354	1	0.1	0.6	0.6	0.1	0.6
Seattle Seahawks	6	10	.375	320	405	-85	-5.3	1.6	-3.7	-1.4	-2.3
San Diego Chargers	1	15	.063	269	440	-171	-10.7	2.6	-8.1	-3.7	-4.4
NFC Standings 
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
Tm	W	L	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS
NFC East
New York Giants*	12	4	.750	328	246	82	5.1	-2.7	2.4	-1.3	3.8
Philadelphia Eagles+	11	5	.688	351	245	106	6.6	-3.6	3.1	1.0	2.1
Washington Redskins	8	8	.500	281	269	12	0.8	0.2	1.0	-2.9	3.8
Dallas Cowboys	5	11	.313	294	361	-67	-4.2	-0.4	-4.6	-1.5	-3.0
Arizona Cardinals	3	13	.188	210	443	-233	-14.6	-0.7	-15.2	-7.2	-8.1
NFC Central
Minnesota Vikings*	11	5	.688	397	371	26	1.6	0.3	1.9	4.3	-2.3
Tampa Bay Buccaneers+	10	6	.625	388	269	119	7.4	-0.1	7.3	3.4	3.9
Green Bay Packers	9	7	.563	353	323	30	1.9	0.6	2.5	1.8	0.7
Detroit Lions	9	7	.563	307	307	0	0.0	1.4	1.4	-0.1	1.5
Chicago Bears	5	11	.313	216	355	-139	-8.7	2.4	-6.3	-6.4	0.1
NFC West
New Orleans Saints*	10	6	.625	354	305	49	3.1	-2.2	0.9	-1.2	2.1
St. Louis Rams+	10	6	.625	540	471	69	4.3	-1.2	3.1	12.6	-9.5
Carolina Panthers	7	9	.438	310	310	0	0.0	-1.1	-1.1	-3.6	2.5
San Francisco 49ers	6	10	.375	388	422	-34	-2.1	-1.7	-3.8	1.7	-5.5
Atlanta Falcons	4	12	.250	252	413	-161	-10.1	1.5	-8.6	-5.7	-2.9
```
</details>

<details>
<summary> A year with ties (2008) </summary>
```
AFC Standings 
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
Tm	W	L	T	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS
AFC East
Miami Dolphins*	11	5	0	.688	345	317	28	1.8	-2.3	-0.5	-2.4	1.8
New England Patriots	11	5	0	.688	410	309	101	6.3	-2.4	3.9	2.3	1.6
New York Jets	9	7	0	.563	405	356	49	3.1	-2.8	0.2	2.2	-1.9
Buffalo Bills	7	9	0	.438	336	342	-6	-0.4	-3.0	-3.3	-2.8	-0.6
AFC North
Pittsburgh Steelers*	12	4	0	.750	347	223	124	7.8	2.0	9.8	1.6	8.2
Baltimore Ravens+	11	5	0	.688	385	244	141	8.8	1.0	9.8	4.2	5.6
Cincinnati Bengals	4	11	1	.281	204	364	-160	-10.0	3.0	-7.0	-6.9	-0.1
Cleveland Browns	4	12	0	.250	232	350	-118	-7.4	2.7	-4.6	-5.2	0.6
AFC South
Tennessee Titans*	13	3	0	.813	375	234	141	8.8	0.1	8.9	1.5	7.5
Indianapolis Colts+	12	4	0	.750	377	298	79	4.9	1.6	6.5	2.6	3.9
Houston Texans	8	8	0	.500	366	394	-28	-1.8	1.4	-0.4	2.8	-3.2
Jacksonville Jaguars	5	11	0	.313	302	367	-65	-4.1	1.6	-2.5	-2.1	-0.4
AFC West
San Diego Chargers*	8	8	0	.500	439	347	92	5.8	-0.8	5.0	5.0	0.0
Denver Broncos	8	8	0	.500	370	448	-78	-4.9	-0.9	-5.8	0.7	-6.5
Oakland Raiders	5	11	0	.313	263	388	-125	-7.8	0.3	-7.5	-6.5	-1.0
Kansas City Chiefs	2	14	0	.125	291	440	-149	-9.3	0.1	-9.2	-3.9	-5.3
NFC Standings 
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
Tm	W	L	T	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS
NFC East
New York Giants*	12	4	0	.750	427	294	133	8.3	0.1	8.4	5.5	2.8
Philadelphia Eagles+	9	6	1	.594	416	289	127	7.9	-0.1	7.8	4.7	3.2
Dallas Cowboys	9	7	0	.563	362	365	-3	-0.2	0.8	0.6	1.7	-1.2
Washington Redskins	8	8	0	.500	265	296	-31	-1.9	0.2	-1.8	-5.8	4.1
NFC North
Minnesota Vikings*	10	6	0	.625	379	333	46	2.9	1.2	4.0	1.1	2.9
Chicago Bears	9	7	0	.563	375	350	25	1.6	0.5	2.1	1.1	1.0
Green Bay Packers	6	10	0	.375	419	380	39	2.4	0.5	2.9	4.1	-1.2
Detroit Lions	0	16	0	.000	268	517	-249	-15.6	2.5	-13.1	-4.0	-9.1
NFC South
Carolina Panthers*	12	4	0	.750	414	329	85	5.3	0.3	5.6	2.8	2.9
Atlanta Falcons+	11	5	0	.688	391	325	66	4.1	-0.3	3.8	1.3	2.5
Tampa Bay Buccaneers	9	7	0	.563	361	323	38	2.4	-0.1	2.3	-0.6	2.9
New Orleans Saints	8	8	0	.500	463	393	70	4.4	-0.3	4.0	6.8	-2.8
NFC West
Arizona Cardinals*	9	7	0	.563	427	426	1	0.1	-1.9	-1.9	4.1	-6.0
San Francisco 49ers	7	9	0	.438	339	381	-42	-2.6	-2.7	-5.3	-2.9	-2.4
Seattle Seahawks	4	12	0	.250	294	392	-98	-6.1	-1.5	-7.6	-4.9	-2.8
St. Louis Rams	2	14	0	.125	232	465	-233	-14.6	-0.5	-15.1	-8.1	-7.0
```
</details>


We need to clean this up in a major way before we can transform this into a useable data frame.
Let's start by doing the following:


```python
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
```
We define our input and output directories, and since we've named all of our scraped data `<YEAR>.txt` (eg: 2000.txt) we can simply loop from 2000 to 2022 in one large loop in range (2000,2023).

We'll delete the text blocks by first defining the text blocks (there are 4 variations: AFC or NFC, and Ties or No Ties) and using `replace()` to replace the text with an empty string.

<details>
<summary> Removing the text blocks</summary>
```python
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
    
```
</details>

We want to preserve the division, playoff outcome, and year information but we also want the team names to be shared year-to-year (ie: the Miami Dolphins in 2001 are still the Miami Dolphins in 2014).
So let's remove the playoff outcome symbols (* and +) from the team names, associate them with a new column `PlayoffRes`, move the year from the file name to a new column called `Year`, and remove the division name from above the teams in that division into its own column `Div`:


```python
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

```


Finally, to address the small inconsistency in the number of columns, let's count the columns in years with ties, and compare that to the current number of columns. If the number is different, we're simply going to add a column and fill it with 0s:
```python
    # Add 16th column if there are 15 columns
    if len(data[0]) == 15:
        for i in data:  # Skip the header line
            #row_data = data[i].split('\t')
            i.insert(3, '0')  # Insert '0' in the 4th position
            #lines[i] = '\t'.join(row_data)
```


Get everything in a csv format with `csv.writer()` and we're done!

We now have some scrubbed data that shows the things we're interested in! Let's take a look at the difference:

<details>
<summary> Scraped 2000</summary>
```
AFC Standings 
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
Tm	W	L	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS
AFC East
Miami Dolphins*	11	5	.688	323	226	97	6.1	1.0	7.1	0.0	7.1
Indianapolis Colts+	10	6	.625	429	326	103	6.4	1.5	7.9	7.1	0.8
New York Jets	9	7	.563	321	321	0	0.0	3.5	3.5	1.4	2.2
Buffalo Bills	8	8	.500	315	350	-35	-2.2	2.2	0.0	0.5	-0.5
New England Patriots	5	11	.313	276	338	-62	-3.9	1.4	-2.5	-2.7	0.2
AFC Central
Tennessee Titans*	13	3	.813	346	191	155	9.7	-1.3	8.3	1.5	6.8
Baltimore Ravens+	12	4	.750	333	165	168	10.5	-2.5	8.0	0.0	8.0
Pittsburgh Steelers	9	7	.563	321	255	66	4.1	-0.2	3.9	0.6	3.3
Jacksonville Jaguars	7	9	.438	367	327	40	2.5	-1.4	1.1	3.2	-2.1
Cincinnati Bengals	4	12	.250	185	359	-174	-10.9	0.4	-10.5	-8.1	-2.4
Cleveland Browns	3	13	.188	161	419	-258	-16.1	1.5	-14.6	-9.1	-5.5
AFC West
Oakland Raiders*	12	4	.750	479	299	180	11.3	-1.5	9.7	8.0	1.8
Denver Broncos+	11	5	.688	485	369	116	7.3	-2.2	5.0	7.8	-2.7
Kansas City Chiefs	7	9	.438	355	354	1	0.1	0.6	0.6	0.1	0.6
Seattle Seahawks	6	10	.375	320	405	-85	-5.3	1.6	-3.7	-1.4	-2.3
San Diego Chargers	1	15	.063	269	440	-171	-10.7	2.6	-8.1	-3.7	-4.4
NFC Standings 
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
Tm	W	L	W-L%	PF	PA	PD	MoV	SoS	SRS	OSRS	DSRS
NFC East
New York Giants*	12	4	.750	328	246	82	5.1	-2.7	2.4	-1.3	3.8
Philadelphia Eagles+	11	5	.688	351	245	106	6.6	-3.6	3.1	1.0	2.1
Washington Redskins	8	8	.500	281	269	12	0.8	0.2	1.0	-2.9	3.8
Dallas Cowboys	5	11	.313	294	361	-67	-4.2	-0.4	-4.6	-1.5	-3.0
Arizona Cardinals	3	13	.188	210	443	-233	-14.6	-0.7	-15.2	-7.2	-8.1
NFC Central
Minnesota Vikings*	11	5	.688	397	371	26	1.6	0.3	1.9	4.3	-2.3
Tampa Bay Buccaneers+	10	6	.625	388	269	119	7.4	-0.1	7.3	3.4	3.9
Green Bay Packers	9	7	.563	353	323	30	1.9	0.6	2.5	1.8	0.7
Detroit Lions	9	7	.563	307	307	0	0.0	1.4	1.4	-0.1	1.5
Chicago Bears	5	11	.313	216	355	-139	-8.7	2.4	-6.3	-6.4	0.1
NFC West
New Orleans Saints*	10	6	.625	354	305	49	3.1	-2.2	0.9	-1.2	2.1
St. Louis Rams+	10	6	.625	540	471	69	4.3	-1.2	3.1	12.6	-9.5
Carolina Panthers	7	9	.438	310	310	0	0.0	-1.1	-1.1	-3.6	2.5
San Francisco 49ers	6	10	.375	388	422	-34	-2.1	-1.7	-3.8	1.7	-5.5
Atlanta Falcons	4	12	.250	252	413	-161	-10.1	1.5	-8.6	-5.7	-2.9
```
</details>

<details>
<summary> Scrubbed 2000</summary>
```
Miami Dolphins,11,5,0,.688,323,226,97,6.1,1.0,7.1,0.0,7.1,AFC East,divwin,2000
Indianapolis Colts,10,6,0,.625,429,326,103,6.4,1.5,7.9,7.1,0.8,AFC East,wildcard,2000
New York Jets,9,7,0,.563,321,321,0,0.0,3.5,3.5,1.4,2.2,AFC East,missed,2000
Buffalo Bills,8,8,0,.500,315,350,-35,-2.2,2.2,0.0,0.5,-0.5,AFC East,missed,2000
New England Patriots,5,11,0,.313,276,338,-62,-3.9,1.4,-2.5,-2.7,0.2,AFC East,missed,2000
Tennessee Titans,13,3,0,.813,346,191,155,9.7,-1.3,8.3,1.5,6.8,AFC Central,divwin,2000
Baltimore Ravens,12,4,0,.750,333,165,168,10.5,-2.5,8.0,0.0,8.0,AFC Central,wildcard,2000
Pittsburgh Steelers,9,7,0,.563,321,255,66,4.1,-0.2,3.9,0.6,3.3,AFC Central,missed,2000
Jacksonville Jaguars,7,9,0,.438,367,327,40,2.5,-1.4,1.1,3.2,-2.1,AFC Central,missed,2000
Cincinnati Bengals,4,12,0,.250,185,359,-174,-10.9,0.4,-10.5,-8.1,-2.4,AFC Central,missed,2000
Cleveland Browns,3,13,0,.188,161,419,-258,-16.1,1.5,-14.6,-9.1,-5.5,AFC Central,missed,2000
Oakland Raiders,12,4,0,.750,479,299,180,11.3,-1.5,9.7,8.0,1.8,AFC West,divwin,2000
Denver Broncos,11,5,0,.688,485,369,116,7.3,-2.2,5.0,7.8,-2.7,AFC West,wildcard,2000
Kansas City Chiefs,7,9,0,.438,355,354,1,0.1,0.6,0.6,0.1,0.6,AFC West,missed,2000
Seattle Seahawks,6,10,0,.375,320,405,-85,-5.3,1.6,-3.7,-1.4,-2.3,AFC West,missed,2000
San Diego Chargers,1,15,0,.063,269,440,-171,-10.7,2.6,-8.1,-3.7,-4.4,AFC West,missed,2000
New York Giants,12,4,0,.750,328,246,82,5.1,-2.7,2.4,-1.3,3.8,NFC East,divwin,2000
Philadelphia Eagles,11,5,0,.688,351,245,106,6.6,-3.6,3.1,1.0,2.1,NFC East,wildcard,2000
Washington Redskins,8,8,0,.500,281,269,12,0.8,0.2,1.0,-2.9,3.8,NFC East,missed,2000
Dallas Cowboys,5,11,0,.313,294,361,-67,-4.2,-0.4,-4.6,-1.5,-3.0,NFC East,missed,2000
Arizona Cardinals,3,13,0,.188,210,443,-233,-14.6,-0.7,-15.2,-7.2,-8.1,NFC East,missed,2000
Minnesota Vikings,11,5,0,.688,397,371,26,1.6,0.3,1.9,4.3,-2.3,NFC Central,divwin,2000
Tampa Bay Buccaneers,10,6,0,.625,388,269,119,7.4,-0.1,7.3,3.4,3.9,NFC Central,wildcard,2000
Green Bay Packers,9,7,0,.563,353,323,30,1.9,0.6,2.5,1.8,0.7,NFC Central,missed,2000
Detroit Lions,9,7,0,.563,307,307,0,0.0,1.4,1.4,-0.1,1.5,NFC Central,missed,2000
Chicago Bears,5,11,0,.313,216,355,-139,-8.7,2.4,-6.3,-6.4,0.1,NFC Central,missed,2000
New Orleans Saints,10,6,0,.625,354,305,49,3.1,-2.2,0.9,-1.2,2.1,NFC West,divwin,2000
St. Louis Rams,10,6,0,.625,540,471,69,4.3,-1.2,3.1,12.6,-9.5,NFC West,wildcard,2000
Carolina Panthers,7,9,0,.438,310,310,0,0.0,-1.1,-1.1,-3.6,2.5,NFC West,missed,2000
San Francisco 49ers,6,10,0,.375,388,422,-34,-2.1,-1.7,-3.8,1.7,-5.5,NFC West,missed,2000
Atlanta Falcons,4,12,0,.250,252,413,-161,-10.1,1.5,-8.6,-5.7,-2.9,NFC West,missed,2000
```
</details>

Note that we never inserted headers for the column names, we'll do that once they're all combined.

#### Combining years into one df

Let's combine all of our output .csv files into a single data frame that we can look at more easily in python (or R, or Excel,...).

Since we've already made sure that every .csv is going to have the same number of columns, we can combine them all quite easily.

```python
import pandas as pd
import glob

# Step 1: Get a list of all CSV files in the directory
csv_files = glob.glob('...\\NFL\\PPG and Pythagorean Wins\\Points_Per_Year\\Scrubbed data\\*.csv')

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

```

One `pd.concat()` and a row of column names later we're all set with our combined df!
<details>
<summary>The final data frame</summary>

|                          |     |      |     |       |     |     |      |       |      |       |       |      |             |            |      | 
|--------------------------|-----|------|-----|-------|-----|-----|------|-------|------|-------|-------|------|-------------|------------|------| 
| Team                     | Win | Loss | Tie | Win%  | PF  | PA  | PD   | MoV   | SoS  | SRS   | OSRS  | DSRS | Div         | PlayoffRes | Year | 
| Miami Dolphins           | 11  | 5    | 0   | 0.688 | 323 | 226 | 97   | 6.1   | 1.0  | 7.1   | 0.0   | 7.1  | AFC East    | divwin     | 2000 | 
| Indianapolis Colts       | 10  | 6    | 0   | 0.625 | 429 | 326 | 103  | 6.4   | 1.5  | 7.9   | 7.1   | 0.8  | AFC East    | wildcard   | 2000 | 
| New York Jets            | 9   | 7    | 0   | 0.563 | 321 | 321 | 0    | 0.0   | 3.5  | 3.5   | 1.4   | 2.2  | AFC East    | missed     | 2000 | 
| Buffalo Bills            | 8   | 8    | 0   | 0.5   | 315 | 350 | -35  | -2.2  | 2.2  | 0.0   | 0.5   | -0.5 | AFC East    | missed     | 2000 | 
| New England Patriots     | 5   | 11   | 0   | 0.313 | 276 | 338 | -62  | -3.9  | 1.4  | -2.5  | -2.7  | 0.2  | AFC East    | missed     | 2000 | 
| Tennessee Titans         | 13  | 3    | 0   | 0.813 | 346 | 191 | 155  | 9.7   | -1.3 | 8.3   | 1.5   | 6.8  | AFC Central | divwin     | 2000 | 
| Baltimore Ravens         | 12  | 4    | 0   | 0.75  | 333 | 165 | 168  | 10.5  | -2.5 | 8.0   | 0.0   | 8.0  | AFC Central | wildcard   | 2000 | 
| Pittsburgh Steelers      | 9   | 7    | 0   | 0.563 | 321 | 255 | 66   | 4.1   | -0.2 | 3.9   | 0.6   | 3.3  | AFC Central | missed     | 2000 | 
| Jacksonville Jaguars     | 7   | 9    | 0   | 0.438 | 367 | 327 | 40   | 2.5   | -1.4 | 1.1   | 3.2   | -2.1 | AFC Central | missed     | 2000 | 
| Cincinnati Bengals       | 4   | 12   | 0   | 0.25  | 185 | 359 | -174 | -10.9 | 0.4  | -10.5 | -8.1  | -2.4 | AFC Central | missed     | 2000 | 
| Cleveland Browns         | 3   | 13   | 0   | 0.188 | 161 | 419 | -258 | -16.1 | 1.5  | -14.6 | -9.1  | -5.5 | AFC Central | missed     | 2000 | 
| Oakland Raiders          | 12  | 4    | 0   | 0.75  | 479 | 299 | 180  | 11.3  | -1.5 | 9.7   | 8.0   | 1.8  | AFC West    | divwin     | 2000 | 
| Denver Broncos           | 11  | 5    | 0   | 0.688 | 485 | 369 | 116  | 7.3   | -2.2 | 5.0   | 7.8   | -2.7 | AFC West    | wildcard   | 2000 | 
| Kansas City Chiefs       | 7   | 9    | 0   | 0.438 | 355 | 354 | 1    | 0.1   | 0.6  | 0.6   | 0.1   | 0.6  | AFC West    | missed     | 2000 | 
| Seattle Seahawks         | 6   | 10   | 0   | 0.375 | 320 | 405 | -85  | -5.3  | 1.6  | -3.7  | -1.4  | -2.3 | AFC West    | missed     | 2000 | 
| San Diego Chargers       | 1   | 15   | 0   | 0.063 | 269 | 440 | -171 | -10.7 | 2.6  | -8.1  | -3.7  | -4.4 | AFC West    | missed     | 2000 | 
| New York Giants          | 12  | 4    | 0   | 0.75  | 328 | 246 | 82   | 5.1   | -2.7 | 2.4   | -1.3  | 3.8  | NFC East    | divwin     | 2000 | 
| Philadelphia Eagles      | 11  | 5    | 0   | 0.688 | 351 | 245 | 106  | 6.6   | -3.6 | 3.1   | 1.0   | 2.1  | NFC East    | wildcard   | 2000 | 
| Washington Redskins      | 8   | 8    | 0   | 0.5   | 281 | 269 | 12   | 0.8   | 0.2  | 1.0   | -2.9  | 3.8  | NFC East    | missed     | 2000 | 
| Dallas Cowboys           | 5   | 11   | 0   | 0.313 | 294 | 361 | -67  | -4.2  | -0.4 | -4.6  | -1.5  | -3.0 | NFC East    | missed     | 2000 | 
| Arizona Cardinals        | 3   | 13   | 0   | 0.188 | 210 | 443 | -233 | -14.6 | -0.7 | -15.2 | -7.2  | -8.1 | NFC East    | missed     | 2000 | 
| Minnesota Vikings        | 11  | 5    | 0   | 0.688 | 397 | 371 | 26   | 1.6   | 0.3  | 1.9   | 4.3   | -2.3 | NFC Central | divwin     | 2000 | 
| Tampa Bay Buccaneers     | 10  | 6    | 0   | 0.625 | 388 | 269 | 119  | 7.4   | -0.1 | 7.3   | 3.4   | 3.9  | NFC Central | wildcard   | 2000 | 
| Green Bay Packers        | 9   | 7    | 0   | 0.563 | 353 | 323 | 30   | 1.9   | 0.6  | 2.5   | 1.8   | 0.7  | NFC Central | missed     | 2000 | 
| Detroit Lions            | 9   | 7    | 0   | 0.563 | 307 | 307 | 0    | 0.0   | 1.4  | 1.4   | -0.1  | 1.5  | NFC Central | missed     | 2000 | 
| Chicago Bears            | 5   | 11   | 0   | 0.313 | 216 | 355 | -139 | -8.7  | 2.4  | -6.3  | -6.4  | 0.1  | NFC Central | missed     | 2000 | 
| New Orleans Saints       | 10  | 6    | 0   | 0.625 | 354 | 305 | 49   | 3.1   | -2.2 | 0.9   | -1.2  | 2.1  | NFC West    | divwin     | 2000 | 
| St. Louis Rams           | 10  | 6    | 0   | 0.625 | 540 | 471 | 69   | 4.3   | -1.2 | 3.1   | 12.6  | -9.5 | NFC West    | wildcard   | 2000 | 
| Carolina Panthers        | 7   | 9    | 0   | 0.438 | 310 | 310 | 0    | 0.0   | -1.1 | -1.1  | -3.6  | 2.5  | NFC West    | missed     | 2000 | 
| San Francisco 49ers      | 6   | 10   | 0   | 0.375 | 388 | 422 | -34  | -2.1  | -1.7 | -3.8  | 1.7   | -5.5 | NFC West    | missed     | 2000 | 
| Atlanta Falcons          | 4   | 12   | 0   | 0.25  | 252 | 413 | -161 | -10.1 | 1.5  | -8.6  | -5.7  | -2.9 | NFC West    | missed     | 2000 | 
| New England Patriots     | 11  | 5    | 0   | 0.688 | 371 | 272 | 99   | 6.2   | -1.9 | 4.3   | 1.2   | 3.1  | AFC East    | divwin     | 2001 | 
| Miami Dolphins           | 11  | 5    | 0   | 0.688 | 344 | 290 | 54   | 3.4   | -0.7 | 2.7   | -0.3  | 3.1  | AFC East    | wildcard   | 2001 | 
| New York Jets            | 10  | 6    | 0   | 0.625 | 308 | 295 | 13   | 0.8   | 0.0  | 0.8   | -2.0  | 2.8  | AFC East    | wildcard   | 2001 | 
| Indianapolis Colts       | 6   | 10   | 0   | 0.375 | 413 | 486 | -73  | -4.6  | 0.8  | -3.8  | 6.1   | -9.8 | AFC East    | missed     | 2001 | 
| Buffalo Bills            | 3   | 13   | 0   | 0.188 | 265 | 420 | -155 | -9.7  | 0.2  | -9.5  | -3.9  | -5.7 | AFC East    | missed     | 2001 | 
| Pittsburgh Steelers      | 13  | 3    | 0   | 0.813 | 352 | 212 | 140  | 8.8   | -1.4 | 7.4   | 1.5   | 5.8  | AFC Central | divwin     | 2001 | 
| Baltimore Ravens         | 10  | 6    | 0   | 0.625 | 303 | 265 | 38   | 2.4   | 0.8  | 3.2   | -0.8  | 4.0  | AFC Central | wildcard   | 2001 | 
| Cleveland Browns         | 7   | 9    | 0   | 0.438 | 285 | 319 | -34  | -2.1  | 1.3  | -0.8  | -0.9  | 0.1  | AFC Central | missed     | 2001 | 
| Tennessee Titans         | 7   | 9    | 0   | 0.438 | 336 | 388 | -52  | -3.3  | 1.2  | -2.0  | 2.4   | -4.4 | AFC Central | missed     | 2001 | 
| Jacksonville Jaguars     | 6   | 10   | 0   | 0.375 | 294 | 286 | 8    | 0.5   | 0.4  | 0.9   | -1.1  | 2.0  | AFC Central | missed     | 2001 | 
| Cincinnati Bengals       | 6   | 10   | 0   | 0.375 | 226 | 309 | -83  | -5.2  | 1.7  | -3.5  | -4.5  | 1.0  | AFC Central | missed     | 2001 | 
| Oakland Raiders          | 10  | 6    | 0   | 0.625 | 399 | 327 | 72   | 4.5   | -0.9 | 3.6   | 4.0   | -0.4 | AFC West    | divwin     | 2001 | 
| Seattle Seahawks         | 9   | 7    | 0   | 0.563 | 301 | 324 | -23  | -1.4  | -0.4 | -1.9  | -1.4  | -0.4 | AFC West    | missed     | 2001 | 
| Denver Broncos           | 8   | 8    | 0   | 0.5   | 340 | 339 | 1    | 0.1   | -0.5 | -0.5  | 0.5   | -1.0 | AFC West    | missed     | 2001 | 
| Kansas City Chiefs       | 6   | 10   | 0   | 0.375 | 320 | 344 | -24  | -1.5  | 0.3  | -1.2  | -0.2  | -1.0 | AFC West    | missed     | 2001 | 
| San Diego Chargers       | 5   | 11   | 0   | 0.313 | 332 | 321 | 11   | 0.7   | -1.0 | -0.3  | 0.3   | -0.6 | AFC West    | missed     | 2001 | 
| Philadelphia Eagles      | 11  | 5    | 0   | 0.688 | 343 | 208 | 135  | 8.4   | -0.7 | 7.7   | 0.9   | 6.8  | NFC East    | divwin     | 2001 | 
| Washington Redskins      | 8   | 8    | 0   | 0.5   | 256 | 303 | -47  | -2.9  | -0.7 | -3.7  | -4.0  | 0.4  | NFC East    | missed     | 2001 | 
| New York Giants          | 7   | 9    | 0   | 0.438 | 294 | 321 | -27  | -1.7  | -0.1 | -1.8  | -1.8  | 0.0  | NFC East    | missed     | 2001 | 
| Arizona Cardinals        | 7   | 9    | 0   | 0.438 | 295 | 343 | -48  | -3.0  | -1.2 | -4.2  | -1.5  | -2.6 | NFC East    | missed     | 2001 | 
| Dallas Cowboys           | 5   | 11   | 0   | 0.313 | 246 | 338 | -92  | -5.8  | -0.2 | -6.0  | -4.5  | -1.5 | NFC East    | missed     | 2001 | 
| Chicago Bears            | 13  | 3    | 0   | 0.813 | 338 | 203 | 135  | 8.4   | -0.5 | 7.9   | 0.9   | 7.1  | NFC Central | divwin     | 2001 | 
| Green Bay Packers        | 12  | 4    | 0   | 0.75  | 390 | 266 | 124  | 7.8   | -1.1 | 6.6   | 4.0   | 2.6  | NFC Central | wildcard   | 2001 | 
| Tampa Bay Buccaneers     | 9   | 7    | 0   | 0.563 | 324 | 280 | 44   | 2.8   | 1.3  | 4.0   | 0.7   | 3.3  | NFC Central | wildcard   | 2001 | 
| Minnesota Vikings        | 5   | 11   | 0   | 0.313 | 290 | 390 | -100 | -6.3  | 1.5  | -4.7  | -0.8  | -3.9 | NFC Central | missed     | 2001 | 
| Detroit Lions            | 2   | 14   | 0   | 0.125 | 270 | 424 | -154 | -9.6  | 2.4  | -7.2  | -2.0  | -5.2 | NFC Central | missed     | 2001 | 
| St. Louis Rams           | 14  | 2    | 0   | 0.875 | 503 | 273 | 230  | 14.4  | -1.0 | 13.4  | 10.4  | 2.9  | NFC West    | divwin     | 2001 | 
| San Francisco 49ers      | 12  | 4    | 0   | 0.75  | 409 | 282 | 127  | 7.9   | -1.1 | 6.8   | 4.2   | 2.7  | NFC West    | wildcard   | 2001 | 
| New Orleans Saints       | 7   | 9    | 0   | 0.438 | 333 | 409 | -76  | -4.8  | -0.1 | -4.8  | -0.1  | -4.7 | NFC West    | missed     | 2001 | 
| Atlanta Falcons          | 7   | 9    | 0   | 0.438 | 291 | 377 | -86  | -5.4  | 0.7  | -4.7  | -2.7  | -2.0 | NFC West    | missed     | 2001 | 
| Carolina Panthers        | 1   | 15   | 0   | 0.063 | 253 | 410 | -157 | -9.8  | 0.9  | -8.9  | -4.6  | -4.4 | NFC West    | missed     | 2001 | 
| New York Jets            | 9   | 7    | 0   | 0.563 | 359 | 336 | 23   | 1.4   | 1.7  | 3.2   | 0.9   | 2.3  | AFC East    | divwin     | 2002 | 
| New England Patriots     | 9   | 7    | 0   | 0.563 | 381 | 346 | 35   | 2.2   | 1.8  | 4.0   | 2.1   | 1.9  | AFC East    | missed     | 2002 | 
| Miami Dolphins           | 9   | 7    | 0   | 0.563 | 378 | 301 | 77   | 4.8   | 1.2  | 6.1   | 1.7   | 4.4  | AFC East    | missed     | 2002 | 
| Buffalo Bills            | 8   | 8    | 0   | 0.5   | 379 | 397 | -18  | -1.1  | 0.9  | -0.3  | 2.1   | -2.3 | AFC East    | missed     | 2002 | 
| Pittsburgh Steelers      | 10  | 5    | 1   | 0.656 | 390 | 345 | 45   | 2.8   | -0.1 | 2.7   | 3.1   | -0.4 | AFC North   | divwin     | 2002 | 
| Cleveland Browns         | 9   | 7    | 0   | 0.563 | 344 | 320 | 24   | 1.5   | -0.3 | 1.2   | -0.4  | 1.7  | AFC North   | wildcard   | 2002 | 
| Baltimore Ravens         | 7   | 9    | 0   | 0.438 | 316 | 354 | -38  | -2.4  | 0.3  | -2.1  | -1.5  | -0.6 | AFC North   | missed     | 2002 | 
| Cincinnati Bengals       | 2   | 14   | 0   | 0.125 | 279 | 456 | -177 | -11.1 | 0.6  | -10.5 | -3.6  | -6.9 | AFC North   | missed     | 2002 | 
| Tennessee Titans         | 11  | 5    | 0   | 0.688 | 367 | 324 | 43   | 2.7   | -0.9 | 1.8   | 1.6   | 0.1  | AFC South   | divwin     | 2002 | 
| Indianapolis Colts       | 10  | 6    | 0   | 0.625 | 349 | 313 | 36   | 2.3   | -1.1 | 1.2   | 0.4   | 0.7  | AFC South   | wildcard   | 2002 | 
| Jacksonville Jaguars     | 6   | 10   | 0   | 0.375 | 328 | 315 | 13   | 0.8   | -1.0 | -0.2  | -1.3  | 1.1  | AFC South   | missed     | 2002 | 
| Houston Texans           | 4   | 12   | 0   | 0.25  | 213 | 356 | -143 | -8.9  | -0.5 | -9.4  | -8.4  | -1.1 | AFC South   | missed     | 2002 | 
| Oakland Raiders          | 11  | 5    | 0   | 0.688 | 450 | 304 | 146  | 9.1   | 1.5  | 10.6  | 6.3   | 4.3  | AFC West    | divwin     | 2002 | 
| Denver Broncos           | 9   | 7    | 0   | 0.563 | 392 | 344 | 48   | 3.0   | 1.9  | 4.9   | 3.0   | 1.9  | AFC West    | missed     | 2002 | 
| San Diego Chargers       | 8   | 8    | 0   | 0.5   | 333 | 367 | -34  | -2.1  | 1.4  | -0.7  | -1.0  | 0.2  | AFC West    | missed     | 2002 | 
| Kansas City Chiefs       | 8   | 8    | 0   | 0.5   | 467 | 399 | 68   | 4.3   | 1.9  | 6.1   | 8.4   | -2.3 | AFC West    | missed     | 2002 | 
| Philadelphia Eagles      | 12  | 4    | 0   | 0.75  | 415 | 241 | 174  | 10.9  | -2.6 | 8.3   | 4.5   | 3.8  | NFC East    | divwin     | 2002 | 
| New York Giants          | 10  | 6    | 0   | 0.625 | 320 | 279 | 41   | 2.6   | -1.7 | 0.8   | -2.2  | 3.0  | NFC East    | wildcard   | 2002 | 
| Washington Redskins      | 7   | 9    | 0   | 0.438 | 307 | 365 | -58  | -3.6  | -0.8 | -4.5  | -2.2  | -2.2 | NFC East    | missed     | 2002 | 
| Dallas Cowboys           | 5   | 11   | 0   | 0.313 | 217 | 329 | -112 | -7.0  | -1.5 | -8.5  | -8.2  | -0.3 | NFC East    | missed     | 2002 | 
| Green Bay Packers        | 12  | 4    | 0   | 0.75  | 398 | 328 | 70   | 4.4   | -0.8 | 3.6   | 2.4   | 1.2  | NFC North   | divwin     | 2002 | 
| Minnesota Vikings        | 6   | 10   | 0   | 0.375 | 390 | 442 | -52  | -3.3  | 0.2  | -3.0  | 3.1   | -6.1 | NFC North   | missed     | 2002 | 
| Chicago Bears            | 4   | 12   | 0   | 0.25  | 281 | 379 | -98  | -6.1  | 0.9  | -5.3  | -4.4  | -0.9 | NFC North   | missed     | 2002 | 
| Detroit Lions            | 3   | 13   | 0   | 0.188 | 306 | 451 | -145 | -9.1  | -0.1 | -9.2  | -2.5  | -6.7 | NFC North   | missed     | 2002 | 
| Tampa Bay Buccaneers     | 12  | 4    | 0   | 0.75  | 346 | 196 | 150  | 9.4   | -0.6 | 8.8   | -1.0  | 9.8  | NFC South   | divwin     | 2002 | 
| Atlanta Falcons          | 9   | 6    | 1   | 0.594 | 402 | 314 | 88   | 5.5   | -0.4 | 5.1   | 3.5   | 1.5  | NFC South   | wildcard   | 2002 | 
| New Orleans Saints       | 9   | 7    | 0   | 0.563 | 432 | 388 | 44   | 2.8   | -0.3 | 2.4   | 5.8   | -3.3 | NFC South   | missed     | 2002 | 
| Carolina Panthers        | 7   | 9    | 0   | 0.438 | 258 | 302 | -44  | -2.8  | -0.5 | -3.3  | -6.0  | 2.8  | NFC South   | missed     | 2002 | 
| San Francisco 49ers      | 10  | 6    | 0   | 0.625 | 367 | 351 | 16   | 1.0   | -0.4 | 0.6   | 0.7   | -0.1 | NFC West    | divwin     | 2002 | 
| St. Louis Rams           | 7   | 9    | 0   | 0.438 | 316 | 369 | -53  | -3.3  | 0.0  | -3.3  | -1.6  | -1.8 | NFC West    | missed     | 2002 | 
| Seattle Seahawks         | 7   | 9    | 0   | 0.438 | 355 | 369 | -14  | -0.9  | -0.4 | -1.3  | 0.0   | -1.2 | NFC West    | missed     | 2002 | 
| Arizona Cardinals        | 5   | 11   | 0   | 0.313 | 262 | 417 | -155 | -9.7  | -0.2 | -9.9  | -5.4  | -4.5 | NFC West    | missed     | 2002 | 
| New England Patriots     | 14  | 2    | 0   | 0.875 | 348 | 238 | 110  | 6.9   | 0.1  | 6.9   | 2.1   | 4.9  | AFC East    | divwin     | 2003 | 
| Miami Dolphins           | 10  | 6    | 0   | 0.625 | 311 | 261 | 50   | 3.1   | 0.3  | 3.4   | -0.7  | 4.1  | AFC East    | missed     | 2003 | 
| Buffalo Bills            | 6   | 10   | 0   | 0.375 | 243 | 279 | -36  | -2.3  | 1.3  | -1.0  | -5.0  | 4.0  | AFC East    | missed     | 2003 | 
| New York Jets            | 6   | 10   | 0   | 0.375 | 283 | 299 | -16  | -1.0  | 0.4  | -0.6  | -1.9  | 1.3  | AFC East    | missed     | 2003 | 
| Baltimore Ravens         | 10  | 6    | 0   | 0.625 | 391 | 281 | 110  | 6.9   | -0.6 | 6.3   | 3.3   | 3.0  | AFC North   | divwin     | 2003 | 
| Cincinnati Bengals       | 8   | 8    | 0   | 0.5   | 346 | 384 | -38  | -2.4  | 0.0  | -2.4  | 1.1   | -3.5 | AFC North   | missed     | 2003 | 
| Pittsburgh Steelers      | 6   | 10   | 0   | 0.375 | 300 | 327 | -27  | -1.7  | 0.6  | -1.1  | -2.5  | 1.4  | AFC North   | missed     | 2003 | 
| Cleveland Browns         | 5   | 11   | 0   | 0.313 | 254 | 322 | -68  | -4.3  | 1.3  | -2.9  | -5.3  | 2.4  | AFC North   | missed     | 2003 | 
| Indianapolis Colts       | 12  | 4    | 0   | 0.75  | 447 | 336 | 111  | 6.9   | 0.0  | 7.0   | 8.2   | -1.2 | AFC South   | divwin     | 2003 | 
| Tennessee Titans         | 12  | 4    | 0   | 0.75  | 435 | 324 | 111  | 6.9   | -0.5 | 6.5   | 7.0   | -0.5 | AFC South   | wildcard   | 2003 | 
| Jacksonville Jaguars     | 5   | 11   | 0   | 0.313 | 276 | 331 | -55  | -3.4  | 1.0  | -2.4  | -3.3  | 0.9  | AFC South   | missed     | 2003 | 
| Houston Texans           | 5   | 11   | 0   | 0.313 | 255 | 380 | -125 | -7.8  | 1.9  | -6.0  | -4.4  | -1.5 | AFC South   | missed     | 2003 | 
| Kansas City Chiefs       | 13  | 3    | 0   | 0.813 | 484 | 332 | 152  | 9.5   | -1.2 | 8.3   | 9.2   | -0.9 | AFC West    | divwin     | 2003 | 
| Denver Broncos           | 10  | 6    | 0   | 0.625 | 381 | 301 | 80   | 5.0   | 0.5  | 5.5   | 2.4   | 3.1  | AFC West    | wildcard   | 2003 | 
| Oakland Raiders          | 4   | 12   | 0   | 0.25  | 270 | 379 | -109 | -6.8  | 1.3  | -5.5  | -4.2  | -1.3 | AFC West    | missed     | 2003 | 
| San Diego Chargers       | 4   | 12   | 0   | 0.25  | 313 | 441 | -128 | -8.0  | 1.2  | -6.8  | -0.6  | -6.2 | AFC West    | missed     | 2003 | 
| Philadelphia Eagles      | 12  | 4    | 0   | 0.75  | 374 | 287 | 87   | 5.4   | -1.0 | 4.4   | 2.9   | 1.5  | NFC East    | divwin     | 2003 | 
| Dallas Cowboys           | 10  | 6    | 0   | 0.625 | 289 | 260 | 29   | 1.8   | -2.3 | -0.5  | -3.2  | 2.7  | NFC East    | wildcard   | 2003 | 
| Washington Redskins      | 5   | 11   | 0   | 0.313 | 287 | 372 | -85  | -5.3  | -0.4 | -5.7  | -1.9  | -3.8 | NFC East    | missed     | 2003 | 
| New York Giants          | 4   | 12   | 0   | 0.25  | 243 | 387 | -144 | -9.0  | 0.4  | -8.6  | -4.8  | -3.7 | NFC East    | missed     | 2003 | 
| Green Bay Packers        | 10  | 6    | 0   | 0.625 | 442 | 307 | 135  | 8.4   | -0.3 | 8.1   | 6.2   | 1.9  | NFC North   | divwin     | 2003 | 
| Minnesota Vikings        | 9   | 7    | 0   | 0.563 | 416 | 353 | 63   | 3.9   | -1.0 | 2.9   | 4.0   | -1.1 | NFC North   | missed     | 2003 | 
| Chicago Bears            | 7   | 9    | 0   | 0.438 | 283 | 346 | -63  | -3.9  | 0.4  | -3.5  | -4.2  | 0.7  | NFC North   | missed     | 2003 | 
| Detroit Lions            | 5   | 11   | 0   | 0.313 | 270 | 379 | -109 | -6.8  | 1.0  | -5.8  | -4.3  | -1.6 | NFC North   | missed     | 2003 | 
| Carolina Panthers        | 11  | 5    | 0   | 0.688 | 325 | 304 | 21   | 1.3   | -2.2 | -0.9  | -1.5  | 0.6  | NFC South   | divwin     | 2003 | 
| New Orleans Saints       | 8   | 8    | 0   | 0.5   | 340 | 326 | 14   | 0.9   | -1.1 | -0.3  | 0.1   | -0.4 | NFC South   | missed     | 2003 | 
| Tampa Bay Buccaneers     | 7   | 9    | 0   | 0.438 | 301 | 264 | 37   | 2.3   | -0.7 | 1.6   | -2.9  | 4.5  | NFC South   | missed     | 2003 | 
| Atlanta Falcons          | 5   | 11   | 0   | 0.313 | 299 | 422 | -123 | -7.7  | 0.3  | -7.4  | -2.0  | -5.4 | NFC South   | missed     | 2003 | 
| St. Louis Rams           | 12  | 4    | 0   | 0.75  | 447 | 328 | 119  | 7.4   | -1.6 | 5.9   | 6.0   | -0.2 | NFC West    | divwin     | 2003 | 
| Seattle Seahawks         | 10  | 6    | 0   | 0.625 | 404 | 327 | 77   | 4.8   | -0.7 | 4.1   | 3.6   | 0.5  | NFC West    | wildcard   | 2003 | 
| San Francisco 49ers      | 7   | 9    | 0   | 0.438 | 384 | 337 | 47   | 2.9   | 0.1  | 3.1   | 3.0   | 0.1  | NFC West    | missed     | 2003 | 
| Arizona Cardinals        | 4   | 12   | 0   | 0.25  | 225 | 452 | -227 | -14.2 | 1.6  | -12.6 | -6.3  | -6.2 | NFC West    | missed     | 2003 | 
| New England Patriots     | 14  | 2    | 0   | 0.875 | 437 | 260 | 177  | 11.1  | 1.8  | 12.8  | 6.4   | 6.5  | AFC East    | divwin     | 2004 | 
| New York Jets            | 10  | 6    | 0   | 0.625 | 333 | 261 | 72   | 4.5   | 2.1  | 6.6   | 0.5   | 6.0  | AFC East    | wildcard   | 2004 | 
| Buffalo Bills            | 9   | 7    | 0   | 0.563 | 395 | 284 | 111  | 6.9   | 1.1  | 8.1   | 4.6   | 3.5  | AFC East    | missed     | 2004 | 
| Miami Dolphins           | 4   | 12   | 0   | 0.25  | 275 | 354 | -79  | -4.9  | 2.7  | -2.2  | -2.7  | 0.5  | AFC East    | missed     | 2004 | 
| Pittsburgh Steelers      | 15  | 1    | 0   | 0.938 | 372 | 251 | 121  | 7.6   | 1.4  | 9.0   | 3.4   | 5.6  | AFC North   | divwin     | 2004 | 
| Baltimore Ravens         | 9   | 7    | 0   | 0.563 | 317 | 268 | 49   | 3.1   | 3.1  | 6.1   | -0.6  | 6.8  | AFC North   | missed     | 2004 | 
| Cincinnati Bengals       | 8   | 8    | 0   | 0.5   | 374 | 372 | 2    | 0.1   | 2.5  | 2.7   | 4.3   | -1.6 | AFC North   | missed     | 2004 | 
| Cleveland Browns         | 4   | 12   | 0   | 0.25  | 276 | 390 | -114 | -7.1  | 3.7  | -3.4  | -1.5  | -1.9 | AFC North   | missed     | 2004 | 
| Indianapolis Colts       | 12  | 4    | 0   | 0.75  | 522 | 351 | 171  | 10.7  | 0.7  | 11.4  | 11.7  | -0.3 | AFC South   | divwin     | 2004 | 
| Jacksonville Jaguars     | 9   | 7    | 0   | 0.563 | 261 | 280 | -19  | -1.2  | 1.9  | 0.8   | -5.7  | 6.4  | AFC South   | missed     | 2004 | 
| Houston Texans           | 7   | 9    | 0   | 0.438 | 309 | 339 | -30  | -1.9  | 1.2  | -0.6  | -2.4  | 1.8  | AFC South   | missed     | 2004 | 
| Tennessee Titans         | 5   | 11   | 0   | 0.313 | 344 | 439 | -95  | -5.9  | 1.5  | -4.4  | 0.3   | -4.6 | AFC South   | missed     | 2004 | 
| San Diego Chargers       | 12  | 4    | 0   | 0.75  | 446 | 313 | 133  | 8.3   | 0.8  | 9.1   | 6.1   | 3.0  | AFC West    | divwin     | 2004 | 
| Denver Broncos           | 10  | 6    | 0   | 0.625 | 381 | 304 | 77   | 4.8   | 1.0  | 5.9   | 1.6   | 4.3  | AFC West    | wildcard   | 2004 | 
| Kansas City Chiefs       | 7   | 9    | 0   | 0.438 | 483 | 435 | 48   | 3.0   | 2.3  | 5.3   | 10.0  | -4.7 | AFC West    | missed     | 2004 | 
| Oakland Raiders          | 5   | 11   | 0   | 0.313 | 320 | 442 | -122 | -7.6  | 3.4  | -4.3  | -0.6  | -3.7 | AFC West    | missed     | 2004 | 
| Philadelphia Eagles      | 13  | 3    | 0   | 0.813 | 386 | 260 | 126  | 7.9   | -2.3 | 5.6   | 2.0   | 3.5  | NFC East    | divwin     | 2004 | 
| New York Giants          | 6   | 10   | 0   | 0.375 | 303 | 347 | -44  | -2.8  | -1.2 | -3.9  | -2.3  | -1.6 | NFC East    | missed     | 2004 | 
| Dallas Cowboys           | 6   | 10   | 0   | 0.375 | 293 | 405 | -112 | -7.0  | -0.8 | -7.8  | -3.0  | -4.8 | NFC East    | missed     | 2004 | 
| Washington Redskins      | 6   | 10   | 0   | 0.375 | 240 | 265 | -25  | -1.6  | -1.8 | -3.4  | -7.4  | 4.0  | NFC East    | missed     | 2004 | 
| Green Bay Packers        | 10  | 6    | 0   | 0.625 | 424 | 380 | 44   | 2.8   | -2.4 | 0.3   | 4.3   | -4.0 | NFC North   | divwin     | 2004 | 
| Minnesota Vikings        | 8   | 8    | 0   | 0.5   | 405 | 395 | 10   | 0.6   | -2.3 | -1.7  | 3.0   | -4.7 | NFC North   | wildcard   | 2004 | 
| Detroit Lions            | 6   | 10   | 0   | 0.375 | 296 | 350 | -54  | -3.4  | -1.8 | -5.2  | -3.8  | -1.4 | NFC North   | missed     | 2004 | 
| Chicago Bears            | 5   | 11   | 0   | 0.313 | 231 | 331 | -100 | -6.3  | -2.0 | -8.2  | -8.5  | 0.3  | NFC North   | missed     | 2004 | 
| Atlanta Falcons          | 11  | 5    | 0   | 0.688 | 340 | 337 | 3    | 0.2   | -2.4 | -2.2  | -1.8  | -0.4 | NFC South   | divwin     | 2004 | 
| New Orleans Saints       | 8   | 8    | 0   | 0.5   | 348 | 405 | -57  | -3.6  | -2.0 | -5.6  | -1.2  | -4.3 | NFC South   | missed     | 2004 | 
| Carolina Panthers        | 7   | 9    | 0   | 0.438 | 355 | 339 | 16   | 1.0   | -1.7 | -0.7  | -0.8  | 0.1  | NFC South   | missed     | 2004 | 
| Tampa Bay Buccaneers     | 5   | 11   | 0   | 0.313 | 301 | 304 | -3   | -0.2  | -2.5 | -2.7  | -4.0  | 1.3  | NFC South   | missed     | 2004 | 
| Seattle Seahawks         | 9   | 7    | 0   | 0.563 | 371 | 373 | -2   | -0.1  | -2.8 | -2.9  | 0.4   | -3.3 | NFC West    | divwin     | 2004 | 
| St. Louis Rams           | 8   | 8    | 0   | 0.5   | 319 | 392 | -73  | -4.6  | -1.4 | -6.0  | -2.2  | -3.8 | NFC West    | wildcard   | 2004 | 
| Arizona Cardinals        | 6   | 10   | 0   | 0.375 | 284 | 322 | -38  | -2.4  | -2.5 | -4.9  | -5.1  | 0.2  | NFC West    | missed     | 2004 | 
| San Francisco 49ers      | 2   | 14   | 0   | 0.125 | 259 | 452 | -193 | -12.1 | -1.6 | -13.6 | -5.1  | -8.6 | NFC West    | missed     | 2004 | 
| New England Patriots     | 10  | 6    | 0   | 0.625 | 379 | 338 | 41   | 2.6   | 0.6  | 3.1   | 3.7   | -0.5 | AFC East    | divwin     | 2005 | 
| Miami Dolphins           | 9   | 7    | 0   | 0.563 | 318 | 317 | 1    | 0.1   | -0.8 | -0.8  | -1.1  | 0.3  | AFC East    | missed     | 2005 | 
| Buffalo Bills            | 5   | 11   | 0   | 0.313 | 271 | 367 | -96  | -6.0  | 0.2  | -5.8  | -4.0  | -1.8 | AFC East    | missed     | 2005 | 
| New York Jets            | 4   | 12   | 0   | 0.25  | 240 | 355 | -115 | -7.2  | 0.8  | -6.4  | -5.2  | -1.2 | AFC East    | missed     | 2005 | 
| Cincinnati Bengals       | 11  | 5    | 0   | 0.688 | 421 | 350 | 71   | 4.4   | -0.6 | 3.8   | 6.5   | -2.7 | AFC North   | divwin     | 2005 | 
| Pittsburgh Steelers      | 11  | 5    | 0   | 0.688 | 389 | 258 | 131  | 8.2   | -0.4 | 7.8   | 3.8   | 4.0  | AFC North   | wildcard   | 2005 | 
| Baltimore Ravens         | 6   | 10   | 0   | 0.375 | 265 | 299 | -34  | -2.1  | 0.3  | -1.8  | -3.5  | 1.7  | AFC North   | missed     | 2005 | 
| Cleveland Browns         | 6   | 10   | 0   | 0.375 | 232 | 301 | -69  | -4.3  | 0.1  | -4.2  | -6.0  | 1.7  | AFC North   | missed     | 2005 | 
| Indianapolis Colts       | 14  | 2    | 0   | 0.875 | 439 | 247 | 192  | 12.0  | -1.2 | 10.8  | 5.6   | 5.2  | AFC South   | divwin     | 2005 | 
| Jacksonville Jaguars     | 12  | 4    | 0   | 0.75  | 361 | 269 | 92   | 5.8   | -1.0 | 4.8   | 1.1   | 3.7  | AFC South   | wildcard   | 2005 | 
| Tennessee Titans         | 4   | 12   | 0   | 0.25  | 299 | 421 | -122 | -7.6  | 0.1  | -7.6  | -2.0  | -5.5 | AFC South   | missed     | 2005 | 
| Houston Texans           | 2   | 14   | 0   | 0.125 | 260 | 431 | -171 | -10.7 | 0.7  | -10.0 | -4.4  | -5.7 | AFC South   | missed     | 2005 | 
| Denver Broncos           | 13  | 3    | 0   | 0.813 | 395 | 258 | 137  | 8.6   | 2.2  | 10.8  | 5.0   | 5.8  | AFC West    | divwin     | 2005 | 
| Kansas City Chiefs       | 10  | 6    | 0   | 0.625 | 403 | 325 | 78   | 4.9   | 2.1  | 7.0   | 5.1   | 1.9  | AFC West    | missed     | 2005 | 
| San Diego Chargers       | 9   | 7    | 0   | 0.563 | 418 | 312 | 106  | 6.6   | 3.3  | 9.9   | 7.1   | 2.9  | AFC West    | missed     | 2005 | 
| Oakland Raiders          | 4   | 12   | 0   | 0.25  | 290 | 383 | -93  | -5.8  | 3.0  | -2.8  | -1.2  | -1.6 | AFC West    | missed     | 2005 | 
| New York Giants          | 11  | 5    | 0   | 0.688 | 422 | 314 | 108  | 6.8   | 0.7  | 7.5   | 5.8   | 1.7  | NFC East    | divwin     | 2005 | 
| Washington Redskins      | 10  | 6    | 0   | 0.625 | 359 | 293 | 66   | 4.1   | 1.9  | 6.0   | 2.6   | 3.4  | NFC East    | wildcard   | 2005 | 
| Dallas Cowboys           | 9   | 7    | 0   | 0.563 | 325 | 308 | 17   | 1.1   | 2.1  | 3.2   | -0.1  | 3.2  | NFC East    | missed     | 2005 | 
| Philadelphia Eagles      | 6   | 10   | 0   | 0.375 | 310 | 388 | -78  | -4.9  | 2.6  | -2.3  | -0.7  | -1.7 | NFC East    | missed     | 2005 | 
| Chicago Bears            | 11  | 5    | 0   | 0.688 | 260 | 202 | 58   | 3.6   | -2.2 | 1.4   | -5.2  | 6.6  | NFC North   | divwin     | 2005 | 
| Minnesota Vikings        | 9   | 7    | 0   | 0.563 | 306 | 344 | -38  | -2.4  | -1.1 | -3.5  | -1.4  | -2.1 | NFC North   | missed     | 2005 | 
| Detroit Lions            | 5   | 11   | 0   | 0.313 | 254 | 345 | -91  | -5.7  | -1.0 | -6.7  | -4.3  | -2.4 | NFC North   | missed     | 2005 | 
| Green Bay Packers        | 4   | 12   | 0   | 0.25  | 298 | 344 | -46  | -2.9  | -0.8 | -3.7  | -1.5  | -2.2 | NFC North   | missed     | 2005 | 
| Tampa Bay Buccaneers     | 11  | 5    | 0   | 0.688 | 300 | 274 | 26   | 1.6   | -2.6 | -1.0  | -2.8  | 1.8  | NFC South   | divwin     | 2005 | 
| Carolina Panthers        | 11  | 5    | 0   | 0.688 | 391 | 259 | 132  | 8.3   | -3.2 | 5.1   | 3.0   | 2.1  | NFC South   | wildcard   | 2005 | 
| Atlanta Falcons          | 8   | 8    | 0   | 0.5   | 351 | 341 | 10   | 0.6   | -1.9 | -1.2  | 1.1   | -2.3 | NFC South   | missed     | 2005 | 
| New Orleans Saints       | 3   | 13   | 0   | 0.188 | 235 | 398 | -163 | -10.2 | -0.9 | -11.1 | -6.2  | -4.9 | NFC South   | missed     | 2005 | 
| Seattle Seahawks         | 13  | 3    | 0   | 0.813 | 452 | 271 | 181  | 11.3  | -2.2 | 9.1   | 5.8   | 3.4  | NFC West    | divwin     | 2005 | 
| St. Louis Rams           | 6   | 10   | 0   | 0.375 | 363 | 429 | -66  | -4.1  | -1.0 | -5.1  | 1.3   | -6.4 | NFC West    | missed     | 2005 | 
| Arizona Cardinals        | 5   | 11   | 0   | 0.313 | 311 | 387 | -76  | -4.8  | -0.2 | -5.0  | -2.0  | -3.0 | NFC West    | missed     | 2005 | 
| San Francisco 49ers      | 4   | 12   | 0   | 0.25  | 239 | 428 | -189 | -11.8 | 0.7  | -11.1 | -5.6  | -5.5 | NFC West    | missed     | 2005 | 
| New England Patriots     | 12  | 4    | 0   | 0.75  | 385 | 237 | 148  | 9.3   | 1.0  | 10.2  | 4.3   | 5.9  | AFC East    | divwin     | 2006 | 
| New York Jets            | 10  | 6    | 0   | 0.625 | 316 | 295 | 21   | 1.3   | 0.7  | 2.0   | 0.4   | 1.7  | AFC East    | wildcard   | 2006 | 
| Buffalo Bills            | 7   | 9    | 0   | 0.438 | 300 | 311 | -11  | -0.7  | 2.9  | 2.2   | -0.2  | 2.4  | AFC East    | missed     | 2006 | 
| Miami Dolphins           | 6   | 10   | 0   | 0.375 | 260 | 283 | -23  | -1.4  | 2.1  | 0.7   | -3.3  | 4.0  | AFC East    | missed     | 2006 | 
| Baltimore Ravens         | 13  | 3    | 0   | 0.813 | 353 | 201 | 152  | 9.5   | -0.2 | 9.3   | 1.5   | 7.8  | AFC North   | divwin     | 2006 | 
| Cincinnati Bengals       | 8   | 8    | 0   | 0.5   | 373 | 331 | 42   | 2.6   | 1.5  | 4.1   | 4.0   | 0.0  | AFC North   | missed     | 2006 | 
| Pittsburgh Steelers      | 8   | 8    | 0   | 0.5   | 353 | 315 | 38   | 2.4   | 1.0  | 3.4   | 3.0   | 0.4  | AFC North   | missed     | 2006 | 
| Cleveland Browns         | 4   | 12   | 0   | 0.25  | 238 | 356 | -118 | -7.4  | 1.5  | -5.8  | -4.5  | -1.3 | AFC North   | missed     | 2006 | 
| Indianapolis Colts       | 12  | 4    | 0   | 0.75  | 427 | 360 | 67   | 4.2   | 1.7  | 5.9   | 6.9   | -1.1 | AFC South   | divwin     | 2006 | 
| Tennessee Titans         | 8   | 8    | 0   | 0.5   | 324 | 400 | -76  | -4.8  | 3.5  | -1.3  | 1.0   | -2.3 | AFC South   | missed     | 2006 | 
| Jacksonville Jaguars     | 8   | 8    | 0   | 0.5   | 371 | 274 | 97   | 6.1   | 1.4  | 7.5   | 2.6   | 4.9  | AFC South   | missed     | 2006 | 
| Houston Texans           | 6   | 10   | 0   | 0.375 | 267 | 366 | -99  | -6.2  | 1.7  | -4.5  | -3.2  | -1.3 | AFC South   | missed     | 2006 | 
| San Diego Chargers       | 14  | 2    | 0   | 0.875 | 492 | 303 | 189  | 11.8  | -1.6 | 10.2  | 10.0  | 0.2  | AFC West    | divwin     | 2006 | 
| Kansas City Chiefs       | 9   | 7    | 0   | 0.563 | 331 | 315 | 16   | 1.0   | 0.0  | 1.0   | 0.4   | 0.6  | AFC West    | wildcard   | 2006 | 
| Denver Broncos           | 9   | 7    | 0   | 0.563 | 319 | 305 | 14   | 0.9   | 0.4  | 1.3   | -0.8  | 2.1  | AFC West    | missed     | 2006 | 
| Oakland Raiders          | 2   | 14   | 0   | 0.125 | 168 | 332 | -164 | -10.3 | 0.6  | -9.6  | -10.3 | 0.7  | AFC West    | missed     | 2006 | 
| Philadelphia Eagles      | 10  | 6    | 0   | 0.625 | 398 | 328 | 70   | 4.4   | -1.0 | 3.4   | 3.2   | 0.2  | NFC East    | divwin     | 2006 | 
| Dallas Cowboys           | 9   | 7    | 0   | 0.563 | 425 | 350 | 75   | 4.7   | -1.0 | 3.7   | 5.0   | -1.3 | NFC East    | wildcard   | 2006 | 
| New York Giants          | 8   | 8    | 0   | 0.5   | 355 | 362 | -7   | -0.4  | 0.5  | 0.1   | 1.2   | -1.1 | NFC East    | wildcard   | 2006 | 
| Washington Redskins      | 5   | 11   | 0   | 0.313 | 307 | 376 | -69  | -4.3  | 0.3  | -4.0  | -2.1  | -2.0 | NFC East    | missed     | 2006 | 
| Chicago Bears            | 13  | 3    | 0   | 0.813 | 427 | 255 | 172  | 10.8  | -2.9 | 7.9   | 4.9   | 3.0  | NFC North   | divwin     | 2006 | 
| Green Bay Packers        | 8   | 8    | 0   | 0.5   | 301 | 366 | -65  | -4.1  | -0.4 | -4.4  | -2.3  | -2.1 | NFC North   | missed     | 2006 | 
| Minnesota Vikings        | 6   | 10   | 0   | 0.375 | 282 | 327 | -45  | -2.8  | -1.3 | -4.1  | -3.7  | -0.4 | NFC North   | missed     | 2006 | 
| Detroit Lions            | 3   | 13   | 0   | 0.188 | 305 | 398 | -93  | -5.8  | -0.5 | -6.4  | -1.8  | -4.6 | NFC North   | missed     | 2006 | 
| New Orleans Saints       | 10  | 6    | 0   | 0.625 | 413 | 322 | 91   | 5.7   | -1.6 | 4.0   | 4.9   | -0.9 | NFC South   | divwin     | 2006 | 
| Carolina Panthers        | 8   | 8    | 0   | 0.5   | 270 | 305 | -35  | -2.2  | -0.5 | -2.7  | -4.2  | 1.5  | NFC South   | missed     | 2006 | 
| Atlanta Falcons          | 7   | 9    | 0   | 0.438 | 292 | 328 | -36  | -2.3  | -0.8 | -3.0  | -2.8  | -0.2 | NFC South   | missed     | 2006 | 
| Tampa Bay Buccaneers     | 4   | 12   | 0   | 0.25  | 211 | 353 | -142 | -8.9  | 0.9  | -7.9  | -7.2  | -0.8 | NFC South   | missed     | 2006 | 
| Seattle Seahawks         | 9   | 7    | 0   | 0.563 | 335 | 341 | -6   | -0.4  | -3.2 | -3.6  | -1.7  | -1.9 | NFC West    | divwin     | 2006 | 
| St. Louis Rams           | 8   | 8    | 0   | 0.5   | 367 | 381 | -14  | -0.9  | -3.1 | -4.0  | 0.8   | -4.7 | NFC West    | missed     | 2006 | 
| San Francisco 49ers      | 7   | 9    | 0   | 0.438 | 298 | 412 | -114 | -7.1  | -1.6 | -8.7  | -3.5  | -5.2 | NFC West    | missed     | 2006 | 
| Arizona Cardinals        | 5   | 11   | 0   | 0.313 | 314 | 389 | -75  | -4.7  | -2.2 | -6.9  | -2.6  | -4.3 | NFC West    | missed     | 2006 | 
| New England Patriots     | 16  | 0    | 0   | 1.0   | 589 | 274 | 315  | 19.7  | 0.4  | 20.1  | 15.9  | 4.2  | AFC East    | divwin     | 2007 | 
| Buffalo Bills            | 7   | 9    | 0   | 0.438 | 252 | 354 | -102 | -6.4  | 2.3  | -4.1  | -5.6  | 1.5  | AFC East    | missed     | 2007 | 
| New York Jets            | 4   | 12   | 0   | 0.25  | 268 | 355 | -87  | -5.4  | 1.7  | -3.7  | -4.0  | 0.3  | AFC East    | missed     | 2007 | 
| Miami Dolphins           | 1   | 15   | 0   | 0.063 | 267 | 437 | -170 | -10.6 | 2.3  | -8.4  | -4.1  | -4.2 | AFC East    | missed     | 2007 | 
| Pittsburgh Steelers      | 10  | 6    | 0   | 0.625 | 393 | 269 | 124  | 7.8   | -2.5 | 5.2   | 0.9   | 4.3  | AFC North   | divwin     | 2007 | 
| Cleveland Browns         | 10  | 6    | 0   | 0.625 | 402 | 382 | 20   | 1.3   | -2.3 | -1.1  | 2.2   | -3.3 | AFC North   | missed     | 2007 | 
| Cincinnati Bengals       | 7   | 9    | 0   | 0.438 | 380 | 385 | -5   | -0.3  | -2.1 | -2.4  | 1.6   | -4.0 | AFC North   | missed     | 2007 | 
| Baltimore Ravens         | 5   | 11   | 0   | 0.313 | 275 | 384 | -109 | -6.8  | 0.1  | -6.7  | -5.0  | -1.8 | AFC North   | missed     | 2007 | 
| Indianapolis Colts       | 13  | 3    | 0   | 0.813 | 450 | 262 | 188  | 11.8  | 0.3  | 12.0  | 6.6   | 5.4  | AFC South   | divwin     | 2007 | 
| Jacksonville Jaguars     | 11  | 5    | 0   | 0.688 | 411 | 304 | 107  | 6.7   | 0.1  | 6.8   | 4.8   | 2.0  | AFC South   | wildcard   | 2007 | 
| Tennessee Titans         | 10  | 6    | 0   | 0.625 | 301 | 297 | 4    | 0.3   | 0.5  | 0.7   | -2.9  | 3.6  | AFC South   | wildcard   | 2007 | 
| Houston Texans           | 8   | 8    | 0   | 0.5   | 379 | 384 | -5   | -0.3  | 0.3  | 0.0   | 2.5   | -2.5 | AFC South   | missed     | 2007 | 
| San Diego Chargers       | 11  | 5    | 0   | 0.688 | 412 | 284 | 128  | 8.0   | 0.8  | 8.8   | 4.3   | 4.5  | AFC West    | divwin     | 2007 | 
| Denver Broncos           | 7   | 9    | 0   | 0.438 | 320 | 409 | -89  | -5.6  | 1.6  | -3.9  | -0.2  | -3.8 | AFC West    | missed     | 2007 | 
| Kansas City Chiefs       | 4   | 12   | 0   | 0.25  | 226 | 335 | -109 | -6.8  | 1.4  | -5.5  | -7.4  | 1.9  | AFC West    | missed     | 2007 | 
| Oakland Raiders          | 4   | 12   | 0   | 0.25  | 283 | 398 | -115 | -7.2  | 1.2  | -6.0  | -3.5  | -2.5 | AFC West    | missed     | 2007 | 
| Dallas Cowboys           | 13  | 3    | 0   | 0.813 | 455 | 325 | 130  | 8.1   | 1.3  | 9.5   | 7.8   | 1.7  | NFC East    | divwin     | 2007 | 
| New York Giants          | 10  | 6    | 0   | 0.625 | 373 | 351 | 22   | 1.4   | 1.9  | 3.3   | 2.8   | 0.4  | NFC East    | wildcard   | 2007 | 
| Washington Redskins      | 9   | 7    | 0   | 0.563 | 334 | 310 | 24   | 1.5   | 3.0  | 4.5   | 0.2   | 4.3  | NFC East    | wildcard   | 2007 | 
| Philadelphia Eagles      | 8   | 8    | 0   | 0.5   | 336 | 300 | 36   | 2.3   | 3.0  | 5.3   | 0.1   | 5.1  | NFC East    | missed     | 2007 | 
| Green Bay Packers        | 13  | 3    | 0   | 0.813 | 435 | 291 | 144  | 9.0   | 0.0  | 9.0   | 5.7   | 3.3  | NFC North   | divwin     | 2007 | 
| Minnesota Vikings        | 8   | 8    | 0   | 0.5   | 365 | 311 | 54   | 3.4   | 0.4  | 3.8   | 1.4   | 2.4  | NFC North   | missed     | 2007 | 
| Detroit Lions            | 7   | 9    | 0   | 0.438 | 346 | 444 | -98  | -6.1  | 2.6  | -3.6  | 1.4   | -5.0 | NFC North   | missed     | 2007 | 
| Chicago Bears            | 7   | 9    | 0   | 0.438 | 334 | 348 | -14  | -0.9  | 2.1  | 1.2   | -0.2  | 1.4  | NFC North   | missed     | 2007 | 
| Tampa Bay Buccaneers     | 9   | 7    | 0   | 0.563 | 334 | 270 | 64   | 4.0   | -2.8 | 1.2   | -2.3  | 3.6  | NFC South   | divwin     | 2007 | 
| Carolina Panthers        | 7   | 9    | 0   | 0.438 | 267 | 347 | -80  | -5.0  | -0.8 | -5.8  | -5.7  | -0.1 | NFC South   | missed     | 2007 | 
| New Orleans Saints       | 7   | 9    | 0   | 0.438 | 379 | 388 | -9   | -0.6  | -2.0 | -2.5  | 1.9   | -4.5 | NFC South   | missed     | 2007 | 
| Atlanta Falcons          | 4   | 12   | 0   | 0.25  | 259 | 414 | -155 | -9.7  | -0.9 | -10.6 | -5.8  | -4.8 | NFC South   | missed     | 2007 | 
| Seattle Seahawks         | 10  | 6    | 0   | 0.625 | 393 | 291 | 102  | 6.4   | -4.6 | 1.8   | 0.8   | 0.9  | NFC West    | divwin     | 2007 | 
| Arizona Cardinals        | 8   | 8    | 0   | 0.5   | 404 | 399 | 5    | 0.3   | -4.3 | -3.9  | 1.9   | -5.9 | NFC West    | missed     | 2007 | 
| San Francisco 49ers      | 5   | 11   | 0   | 0.313 | 219 | 364 | -145 | -9.1  | -2.9 | -11.9 | -9.9  | -2.0 | NFC West    | missed     | 2007 | 
| St. Louis Rams           | 3   | 13   | 0   | 0.188 | 263 | 438 | -175 | -10.9 | -2.0 | -13.0 | -6.5  | -6.5 | NFC West    | missed     | 2007 | 
| Miami Dolphins           | 11  | 5    | 0   | 0.688 | 345 | 317 | 28   | 1.8   | -2.3 | -0.5  | -2.4  | 1.8  | AFC East    | divwin     | 2008 | 
| New England Patriots     | 11  | 5    | 0   | 0.688 | 410 | 309 | 101  | 6.3   | -2.4 | 3.9   | 2.3   | 1.6  | AFC East    | missed     | 2008 | 
| New York Jets            | 9   | 7    | 0   | 0.563 | 405 | 356 | 49   | 3.1   | -2.8 | 0.2   | 2.2   | -1.9 | AFC East    | missed     | 2008 | 
| Buffalo Bills            | 7   | 9    | 0   | 0.438 | 336 | 342 | -6   | -0.4  | -3.0 | -3.3  | -2.8  | -0.6 | AFC East    | missed     | 2008 | 
| Pittsburgh Steelers      | 12  | 4    | 0   | 0.75  | 347 | 223 | 124  | 7.8   | 2.0  | 9.8   | 1.6   | 8.2  | AFC North   | divwin     | 2008 | 
| Baltimore Ravens         | 11  | 5    | 0   | 0.688 | 385 | 244 | 141  | 8.8   | 1.0  | 9.8   | 4.2   | 5.6  | AFC North   | wildcard   | 2008 | 
| Cincinnati Bengals       | 4   | 11   | 1   | 0.281 | 204 | 364 | -160 | -10.0 | 3.0  | -7.0  | -6.9  | -0.1 | AFC North   | missed     | 2008 | 
| Cleveland Browns         | 4   | 12   | 0   | 0.25  | 232 | 350 | -118 | -7.4  | 2.7  | -4.6  | -5.2  | 0.6  | AFC North   | missed     | 2008 | 
| Tennessee Titans         | 13  | 3    | 0   | 0.813 | 375 | 234 | 141  | 8.8   | 0.1  | 8.9   | 1.5   | 7.5  | AFC South   | divwin     | 2008 | 
| Indianapolis Colts       | 12  | 4    | 0   | 0.75  | 377 | 298 | 79   | 4.9   | 1.6  | 6.5   | 2.6   | 3.9  | AFC South   | wildcard   | 2008 | 
| Houston Texans           | 8   | 8    | 0   | 0.5   | 366 | 394 | -28  | -1.8  | 1.4  | -0.4  | 2.8   | -3.2 | AFC South   | missed     | 2008 | 
| Jacksonville Jaguars     | 5   | 11   | 0   | 0.313 | 302 | 367 | -65  | -4.1  | 1.6  | -2.5  | -2.1  | -0.4 | AFC South   | missed     | 2008 | 
| San Diego Chargers       | 8   | 8    | 0   | 0.5   | 439 | 347 | 92   | 5.8   | -0.8 | 5.0   | 5.0   | 0.0  | AFC West    | divwin     | 2008 | 
| Denver Broncos           | 8   | 8    | 0   | 0.5   | 370 | 448 | -78  | -4.9  | -0.9 | -5.8  | 0.7   | -6.5 | AFC West    | missed     | 2008 | 
| Oakland Raiders          | 5   | 11   | 0   | 0.313 | 263 | 388 | -125 | -7.8  | 0.3  | -7.5  | -6.5  | -1.0 | AFC West    | missed     | 2008 | 
| Kansas City Chiefs       | 2   | 14   | 0   | 0.125 | 291 | 440 | -149 | -9.3  | 0.1  | -9.2  | -3.9  | -5.3 | AFC West    | missed     | 2008 | 
| New York Giants          | 12  | 4    | 0   | 0.75  | 427 | 294 | 133  | 8.3   | 0.1  | 8.4   | 5.5   | 2.8  | NFC East    | divwin     | 2008 | 
| Philadelphia Eagles      | 9   | 6    | 1   | 0.594 | 416 | 289 | 127  | 7.9   | -0.1 | 7.8   | 4.7   | 3.2  | NFC East    | wildcard   | 2008 | 
| Dallas Cowboys           | 9   | 7    | 0   | 0.563 | 362 | 365 | -3   | -0.2  | 0.8  | 0.6   | 1.7   | -1.2 | NFC East    | missed     | 2008 | 
| Washington Redskins      | 8   | 8    | 0   | 0.5   | 265 | 296 | -31  | -1.9  | 0.2  | -1.8  | -5.8  | 4.1  | NFC East    | missed     | 2008 | 
| Minnesota Vikings        | 10  | 6    | 0   | 0.625 | 379 | 333 | 46   | 2.9   | 1.2  | 4.0   | 1.1   | 2.9  | NFC North   | divwin     | 2008 | 
| Chicago Bears            | 9   | 7    | 0   | 0.563 | 375 | 350 | 25   | 1.6   | 0.5  | 2.1   | 1.1   | 1.0  | NFC North   | missed     | 2008 | 
| Green Bay Packers        | 6   | 10   | 0   | 0.375 | 419 | 380 | 39   | 2.4   | 0.5  | 2.9   | 4.1   | -1.2 | NFC North   | missed     | 2008 | 
| Detroit Lions            | 0   | 16   | 0   | 0.0   | 268 | 517 | -249 | -15.6 | 2.5  | -13.1 | -4.0  | -9.1 | NFC North   | missed     | 2008 | 
| Carolina Panthers        | 12  | 4    | 0   | 0.75  | 414 | 329 | 85   | 5.3   | 0.3  | 5.6   | 2.8   | 2.9  | NFC South   | divwin     | 2008 | 
| Atlanta Falcons          | 11  | 5    | 0   | 0.688 | 391 | 325 | 66   | 4.1   | -0.3 | 3.8   | 1.3   | 2.5  | NFC South   | wildcard   | 2008 | 
| Tampa Bay Buccaneers     | 9   | 7    | 0   | 0.563 | 361 | 323 | 38   | 2.4   | -0.1 | 2.3   | -0.6  | 2.9  | NFC South   | missed     | 2008 | 
| New Orleans Saints       | 8   | 8    | 0   | 0.5   | 463 | 393 | 70   | 4.4   | -0.3 | 4.0   | 6.8   | -2.8 | NFC South   | missed     | 2008 | 
| Arizona Cardinals        | 9   | 7    | 0   | 0.563 | 427 | 426 | 1    | 0.1   | -1.9 | -1.9  | 4.1   | -6.0 | NFC West    | divwin     | 2008 | 
| San Francisco 49ers      | 7   | 9    | 0   | 0.438 | 339 | 381 | -42  | -2.6  | -2.7 | -5.3  | -2.9  | -2.4 | NFC West    | missed     | 2008 | 
| Seattle Seahawks         | 4   | 12   | 0   | 0.25  | 294 | 392 | -98  | -6.1  | -1.5 | -7.6  | -4.9  | -2.8 | NFC West    | missed     | 2008 | 
| St. Louis Rams           | 2   | 14   | 0   | 0.125 | 232 | 465 | -233 | -14.6 | -0.5 | -15.1 | -8.1  | -7.0 | NFC West    | missed     | 2008 | 
| New England Patriots     | 10  | 6    | 0   | 0.625 | 427 | 285 | 142  | 8.9   | 2.3  | 11.2  | 6.7   | 4.5  | AFC East    | divwin     | 2009 | 
| New York Jets            | 9   | 7    | 0   | 0.563 | 348 | 236 | 112  | 7.0   | 1.6  | 8.6   | 1.1   | 7.5  | AFC East    | wildcard   | 2009 | 
| Miami Dolphins           | 7   | 9    | 0   | 0.438 | 360 | 390 | -30  | -1.9  | 3.6  | 1.7   | 2.9   | -1.2 | AFC East    | missed     | 2009 | 
| Buffalo Bills            | 6   | 10   | 0   | 0.375 | 258 | 326 | -68  | -4.3  | 2.4  | -1.8  | -4.5  | 2.7  | AFC East    | missed     | 2009 | 
| Cincinnati Bengals       | 10  | 6    | 0   | 0.625 | 305 | 291 | 14   | 0.9   | -0.2 | 0.7   | -2.5  | 3.2  | AFC North   | divwin     | 2009 | 
| Baltimore Ravens         | 9   | 7    | 0   | 0.563 | 391 | 261 | 130  | 8.1   | -0.7 | 7.5   | 2.6   | 4.9  | AFC North   | wildcard   | 2009 | 
| Pittsburgh Steelers      | 9   | 7    | 0   | 0.563 | 368 | 324 | 44   | 2.8   | -1.1 | 1.7   | 1.0   | 0.7  | AFC North   | missed     | 2009 | 
| Cleveland Browns         | 5   | 11   | 0   | 0.313 | 245 | 375 | -130 | -8.1  | -0.3 | -8.4  | -6.0  | -2.4 | AFC North   | missed     | 2009 | 
| Indianapolis Colts       | 14  | 2    | 0   | 0.875 | 416 | 307 | 109  | 6.8   | -0.9 | 5.9   | 4.4   | 1.5  | AFC South   | divwin     | 2009 | 
| Houston Texans           | 9   | 7    | 0   | 0.563 | 388 | 333 | 55   | 3.4   | -1.5 | 2.0   | 2.7   | -0.7 | AFC South   | missed     | 2009 | 
| Tennessee Titans         | 8   | 8    | 0   | 0.5   | 354 | 402 | -48  | -3.0  | 0.2  | -2.8  | 0.9   | -3.6 | AFC South   | missed     | 2009 | 
| Jacksonville Jaguars     | 7   | 9    | 0   | 0.438 | 290 | 380 | -90  | -5.6  | -0.9 | -6.5  | -3.8  | -2.6 | AFC South   | missed     | 2009 | 
| San Diego Chargers       | 13  | 3    | 0   | 0.813 | 454 | 320 | 134  | 8.4   | -1.7 | 6.6   | 6.4   | 0.2  | AFC West    | divwin     | 2009 | 
| Denver Broncos           | 8   | 8    | 0   | 0.5   | 326 | 324 | 2    | 0.1   | 0.2  | 0.3   | -1.0  | 1.3  | AFC West    | missed     | 2009 | 
| Oakland Raiders          | 5   | 11   | 0   | 0.313 | 197 | 379 | -182 | -11.4 | 1.1  | -10.3 | -8.7  | -1.6 | AFC West    | missed     | 2009 | 
| Kansas City Chiefs       | 4   | 12   | 0   | 0.25  | 294 | 424 | -130 | -8.1  | -0.3 | -8.4  | -2.5  | -5.9 | AFC West    | missed     | 2009 | 
| Dallas Cowboys           | 11  | 5    | 0   | 0.688 | 361 | 250 | 111  | 6.9   | 0.2  | 7.1   | 0.4   | 6.7  | NFC East    | divwin     | 2009 | 
| Philadelphia Eagles      | 11  | 5    | 0   | 0.688 | 429 | 337 | 92   | 5.8   | 0.2  | 6.0   | 5.8   | 0.2  | NFC East    | wildcard   | 2009 | 
| New York Giants          | 8   | 8    | 0   | 0.5   | 402 | 427 | -25  | -1.6  | 1.6  | 0.1   | 4.6   | -4.5 | NFC East    | missed     | 2009 | 
| Washington Redskins      | 4   | 12   | 0   | 0.25  | 266 | 336 | -70  | -4.4  | -0.2 | -4.6  | -5.5  | 1.0  | NFC East    | missed     | 2009 | 
| Minnesota Vikings        | 12  | 4    | 0   | 0.75  | 470 | 312 | 158  | 9.9   | -2.7 | 7.2   | 6.6   | 0.6  | NFC North   | divwin     | 2009 | 
| Green Bay Packers        | 11  | 5    | 0   | 0.688 | 461 | 297 | 164  | 10.3  | -2.9 | 7.4   | 6.3   | 1.1  | NFC North   | wildcard   | 2009 | 
| Chicago Bears            | 7   | 9    | 0   | 0.438 | 327 | 375 | -48  | -3.0  | -0.9 | -3.9  | -1.9  | -2.0 | NFC North   | missed     | 2009 | 
| Detroit Lions            | 2   | 14   | 0   | 0.125 | 262 | 494 | -232 | -14.5 | 0.1  | -14.4 | -5.2  | -9.2 | NFC North   | missed     | 2009 | 
| New Orleans Saints       | 13  | 3    | 0   | 0.813 | 510 | 341 | 169  | 10.6  | 0.2  | 10.8  | 11.2  | -0.5 | NFC South   | divwin     | 2009 | 
| Atlanta Falcons          | 9   | 7    | 0   | 0.563 | 363 | 325 | 38   | 2.4   | 2.7  | 5.0   | 2.7   | 2.3  | NFC South   | missed     | 2009 | 
| Carolina Panthers        | 8   | 8    | 0   | 0.5   | 315 | 308 | 7    | 0.4   | 3.5  | 3.9   | -0.6  | 4.5  | NFC South   | missed     | 2009 | 
| Tampa Bay Buccaneers     | 3   | 13   | 0   | 0.188 | 244 | 400 | -156 | -9.8  | 4.1  | -5.6  | -4.6  | -1.1 | NFC South   | missed     | 2009 | 
| Arizona Cardinals        | 10  | 6    | 0   | 0.625 | 375 | 325 | 50   | 3.1   | -3.4 | -0.3  | 0.1   | -0.4 | NFC West    | divwin     | 2009 | 
| San Francisco 49ers      | 8   | 8    | 0   | 0.5   | 330 | 281 | 49   | 3.1   | -3.0 | 0.1   | -2.9  | 3.0  | NFC West    | missed     | 2009 | 
| Seattle Seahawks         | 5   | 11   | 0   | 0.313 | 280 | 390 | -110 | -6.9  | -2.4 | -9.3  | -5.0  | -4.4 | NFC West    | missed     | 2009 | 
| St. Louis Rams           | 1   | 15   | 0   | 0.063 | 175 | 436 | -261 | -16.3 | -1.1 | -17.4 | -11.7 | -5.8 | NFC West    | missed     | 2009 | 
| New England Patriots     | 14  | 2    | 0   | 0.875 | 518 | 313 | 205  | 12.8  | 2.6  | 15.4  | 12.6  | 2.8  | AFC East    | divwin     | 2010 | 
| New York Jets            | 11  | 5    | 0   | 0.688 | 367 | 304 | 63   | 3.9   | 2.5  | 6.5   | 2.2   | 4.2  | AFC East    | wildcard   | 2010 | 
| Miami Dolphins           | 7   | 9    | 0   | 0.438 | 273 | 333 | -60  | -3.8  | 4.1  | 0.3   | -2.8  | 3.1  | AFC East    | missed     | 2010 | 
| Buffalo Bills            | 4   | 12   | 0   | 0.25  | 283 | 425 | -142 | -8.9  | 4.3  | -4.6  | -1.5  | -3.1 | AFC East    | missed     | 2010 | 
| Pittsburgh Steelers      | 12  | 4    | 0   | 0.75  | 375 | 232 | 143  | 8.9   | 1.3  | 10.2  | 2.5   | 7.7  | AFC North   | divwin     | 2010 | 
| Baltimore Ravens         | 12  | 4    | 0   | 0.75  | 357 | 270 | 87   | 5.4   | 1.0  | 6.4   | 0.9   | 5.5  | AFC North   | wildcard   | 2010 | 
| Cleveland Browns         | 5   | 11   | 0   | 0.313 | 271 | 332 | -61  | -3.8  | 2.3  | -1.5  | -3.4  | 2.0  | AFC North   | missed     | 2010 | 
| Cincinnati Bengals       | 4   | 12   | 0   | 0.25  | 322 | 395 | -73  | -4.6  | 3.1  | -1.4  | 0.4   | -1.9 | AFC North   | missed     | 2010 | 
| Indianapolis Colts       | 10  | 6    | 0   | 0.625 | 435 | 388 | 47   | 2.9   | -0.1 | 2.9   | 3.7   | -0.9 | AFC South   | divwin     | 2010 | 
| Jacksonville Jaguars     | 8   | 8    | 0   | 0.5   | 353 | 419 | -66  | -4.1  | -0.4 | -4.5  | -1.2  | -3.3 | AFC South   | missed     | 2010 | 
| Houston Texans           | 6   | 10   | 0   | 0.375 | 390 | 427 | -37  | -2.3  | 0.5  | -1.8  | 1.8   | -3.7 | AFC South   | missed     | 2010 | 
| Tennessee Titans         | 6   | 10   | 0   | 0.375 | 356 | 339 | 17   | 1.1   | 0.0  | 1.0   | -0.9  | 1.9  | AFC South   | missed     | 2010 | 
| Kansas City Chiefs       | 10  | 6    | 0   | 0.625 | 366 | 326 | 40   | 2.5   | -3.2 | -0.7  | -1.5  | 0.8  | AFC West    | divwin     | 2010 | 
| San Diego Chargers       | 9   | 7    | 0   | 0.563 | 441 | 322 | 119  | 7.4   | -2.6 | 4.8   | 3.2   | 1.6  | AFC West    | missed     | 2010 | 
| Oakland Raiders          | 8   | 8    | 0   | 0.5   | 410 | 371 | 39   | 2.4   | -2.3 | 0.2   | 2.3   | -2.2 | AFC West    | missed     | 2010 | 
| Denver Broncos           | 4   | 12   | 0   | 0.25  | 344 | 471 | -127 | -7.9  | -1.0 | -8.9  | -1.1  | -7.8 | AFC West    | missed     | 2010 | 
| Philadelphia Eagles      | 10  | 6    | 0   | 0.625 | 439 | 377 | 62   | 3.9   | 0.3  | 4.2   | 5.4   | -1.2 | NFC East    | divwin     | 2010 | 
| New York Giants          | 10  | 6    | 0   | 0.625 | 394 | 347 | 47   | 2.9   | -0.8 | 2.1   | 1.7   | 0.4  | NFC East    | missed     | 2010 | 
| Dallas Cowboys           | 6   | 10   | 0   | 0.375 | 394 | 436 | -42  | -2.6  | 0.5  | -2.2  | 2.5   | -4.7 | NFC East    | missed     | 2010 | 
| Washington Redskins      | 6   | 10   | 0   | 0.375 | 302 | 377 | -75  | -4.7  | 0.9  | -3.8  | -3.4  | -0.5 | NFC East    | missed     | 2010 | 
| Chicago Bears            | 11  | 5    | 0   | 0.688 | 334 | 286 | 48   | 3.0   | 1.1  | 4.1   | -0.6  | 4.7  | NFC North   | divwin     | 2010 | 
| Green Bay Packers        | 10  | 6    | 0   | 0.625 | 388 | 240 | 148  | 9.3   | 1.7  | 10.9  | 3.1   | 7.9  | NFC North   | wildcard   | 2010 | 
| Detroit Lions            | 6   | 10   | 0   | 0.375 | 362 | 369 | -7   | -0.4  | 2.3  | 1.9   | 2.4   | -0.5 | NFC North   | missed     | 2010 | 
| Minnesota Vikings        | 6   | 10   | 0   | 0.375 | 281 | 348 | -67  | -4.2  | 2.6  | -1.6  | -3.3  | 1.7  | NFC North   | missed     | 2010 | 
| Atlanta Falcons          | 13  | 3    | 0   | 0.813 | 414 | 288 | 126  | 7.9   | -1.8 | 6.1   | 3.8   | 2.2  | NFC South   | divwin     | 2010 | 
| New Orleans Saints       | 11  | 5    | 0   | 0.688 | 384 | 307 | 77   | 4.8   | -2.5 | 2.3   | 1.5   | 0.8  | NFC South   | wildcard   | 2010 | 
| Tampa Bay Buccaneers     | 10  | 6    | 0   | 0.625 | 341 | 318 | 23   | 1.4   | -2.0 | -0.6  | -1.0  | 0.4  | NFC South   | missed     | 2010 | 
| Carolina Panthers        | 2   | 14   | 0   | 0.125 | 196 | 408 | -212 | -13.3 | 0.1  | -13.2 | -9.1  | -4.1 | NFC South   | missed     | 2010 | 
| Seattle Seahawks         | 7   | 9    | 0   | 0.438 | 310 | 407 | -97  | -6.1  | -3.4 | -9.4  | -3.9  | -5.5 | NFC West    | divwin     | 2010 | 
| St. Louis Rams           | 7   | 9    | 0   | 0.438 | 289 | 328 | -39  | -2.4  | -4.2 | -6.7  | -6.3  | -0.4 | NFC West    | missed     | 2010 | 
| San Francisco 49ers      | 6   | 10   | 0   | 0.375 | 305 | 346 | -41  | -2.6  | -3.3 | -5.8  | -4.7  | -1.1 | NFC West    | missed     | 2010 | 
| Arizona Cardinals        | 5   | 11   | 0   | 0.313 | 289 | 434 | -145 | -9.1  | -3.6 | -12.7 | -5.6  | -7.1 | NFC West    | missed     | 2010 | 
| New England Patriots     | 13  | 3    | 0   | 0.813 | 513 | 342 | 171  | 10.7  | -1.4 | 9.3   | 9.4   | -0.1 | AFC East    | divwin     | 2011 | 
| New York Jets            | 8   | 8    | 0   | 0.5   | 377 | 363 | 14   | 0.9   | 0.0  | 0.9   | 1.2   | -0.3 | AFC East    | missed     | 2011 | 
| Miami Dolphins           | 6   | 10   | 0   | 0.375 | 329 | 313 | 16   | 1.0   | -0.1 | 0.9   | -2.2  | 3.2  | AFC East    | missed     | 2011 | 
| Buffalo Bills            | 6   | 10   | 0   | 0.375 | 372 | 434 | -62  | -3.9  | 0.5  | -3.4  | 1.2   | -4.5 | AFC East    | missed     | 2011 | 
| Baltimore Ravens         | 12  | 4    | 0   | 0.75  | 378 | 266 | 112  | 7.0   | -0.9 | 6.1   | 2.6   | 3.5  | AFC North   | divwin     | 2011 | 
| Pittsburgh Steelers      | 12  | 4    | 0   | 0.75  | 325 | 227 | 98   | 6.1   | -0.8 | 5.3   | -0.8  | 6.0  | AFC North   | wildcard   | 2011 | 
| Cincinnati Bengals       | 9   | 7    | 0   | 0.563 | 344 | 323 | 21   | 1.3   | -0.9 | 0.5   | 0.7   | -0.2 | AFC North   | wildcard   | 2011 | 
| Cleveland Browns         | 4   | 12   | 0   | 0.25  | 218 | 307 | -89  | -5.6  | 0.2  | -5.4  | -7.2  | 1.8  | AFC North   | missed     | 2011 | 
| Houston Texans           | 10  | 6    | 0   | 0.625 | 381 | 278 | 103  | 6.4   | -1.9 | 4.5   | 1.4   | 3.2  | AFC South   | divwin     | 2011 | 
| Tennessee Titans         | 9   | 7    | 0   | 0.563 | 325 | 317 | 8    | 0.5   | -1.5 | -1.0  | -2.2  | 1.2  | AFC South   | missed     | 2011 | 
| Jacksonville Jaguars     | 5   | 11   | 0   | 0.313 | 243 | 329 | -86  | -5.4  | -0.3 | -5.6  | -7.1  | 1.4  | AFC South   | missed     | 2011 | 
| Indianapolis Colts       | 2   | 14   | 0   | 0.125 | 243 | 430 | -187 | -11.7 | 0.4  | -11.3 | -6.0  | -5.3 | AFC South   | missed     | 2011 | 
| Denver Broncos           | 8   | 8    | 0   | 0.5   | 309 | 390 | -81  | -5.1  | -0.2 | -5.3  | -3.6  | -1.7 | AFC West    | divwin     | 2011 | 
| San Diego Chargers       | 8   | 8    | 0   | 0.5   | 406 | 377 | 29   | 1.8   | -0.9 | 0.9   | 2.7   | -1.8 | AFC West    | missed     | 2011 | 
| Oakland Raiders          | 8   | 8    | 0   | 0.5   | 359 | 433 | -74  | -4.6  | -0.3 | -4.9  | 0.2   | -5.1 | AFC West    | missed     | 2011 | 
| Kansas City Chiefs       | 7   | 9    | 0   | 0.438 | 212 | 338 | -126 | -7.9  | -0.2 | -8.1  | -10.2 | 2.1  | AFC West    | missed     | 2011 | 
| New York Giants          | 9   | 7    | 0   | 0.563 | 394 | 400 | -6   | -0.4  | 2.0  | 1.6   | 3.1   | -1.5 | NFC East    | divwin     | 2011 | 
| Philadelphia Eagles      | 8   | 8    | 0   | 0.5   | 396 | 328 | 68   | 4.3   | 0.5  | 4.7   | 3.1   | 1.7  | NFC East    | missed     | 2011 | 
| Dallas Cowboys           | 8   | 8    | 0   | 0.5   | 369 | 347 | 22   | 1.4   | 0.3  | 1.6   | 0.7   | 0.9  | NFC East    | missed     | 2011 | 
| Washington Redskins      | 5   | 11   | 0   | 0.313 | 288 | 367 | -79  | -4.9  | 0.8  | -4.1  | -4.3  | 0.2  | NFC East    | missed     | 2011 | 
| Green Bay Packers        | 15  | 1    | 0   | 0.938 | 560 | 359 | 201  | 12.6  | -1.2 | 11.4  | 11.5  | -0.1 | NFC North   | divwin     | 2011 | 
| Detroit Lions            | 10  | 6    | 0   | 0.625 | 474 | 387 | 87   | 5.4   | 0.6  | 6.1   | 6.9   | -0.8 | NFC North   | wildcard   | 2011 | 
| Chicago Bears            | 8   | 8    | 0   | 0.5   | 353 | 341 | 12   | 0.8   | 0.9  | 1.7   | -1.5  | 3.1  | NFC North   | missed     | 2011 | 
| Minnesota Vikings        | 3   | 13   | 0   | 0.188 | 340 | 449 | -109 | -6.8  | 1.1  | -5.7  | -1.6  | -4.1 | NFC North   | missed     | 2011 | 
| New Orleans Saints       | 13  | 3    | 0   | 0.813 | 547 | 339 | 208  | 13.0  | -1.6 | 11.4  | 10.6  | 0.8  | NFC South   | divwin     | 2011 | 
| Atlanta Falcons          | 10  | 6    | 0   | 0.625 | 402 | 350 | 52   | 3.3   | 0.3  | 3.5   | 1.8   | 1.7  | NFC South   | wildcard   | 2011 | 
| Carolina Panthers        | 6   | 10   | 0   | 0.375 | 406 | 429 | -23  | -1.4  | 0.1  | -1.3  | 2.6   | -3.9 | NFC South   | missed     | 2011 | 
| Tampa Bay Buccaneers     | 4   | 12   | 0   | 0.25  | 287 | 494 | -207 | -12.9 | 2.3  | -10.6 | -4.0  | -6.6 | NFC South   | missed     | 2011 | 
| San Francisco 49ers      | 13  | 3    | 0   | 0.813 | 380 | 229 | 151  | 9.4   | -1.1 | 8.3   | 1.7   | 6.6  | NFC West    | divwin     | 2011 | 
| Arizona Cardinals        | 8   | 8    | 0   | 0.5   | 312 | 348 | -36  | -2.3  | 0.0  | -2.2  | -1.7  | -0.5 | NFC West    | missed     | 2011 | 
| Seattle Seahawks         | 7   | 9    | 0   | 0.438 | 321 | 315 | 6    | 0.4   | 0.4  | 0.8   | -0.5  | 1.3  | NFC West    | missed     | 2011 | 
| St. Louis Rams           | 2   | 14   | 0   | 0.125 | 193 | 407 | -214 | -13.4 | 2.9  | -10.4 | -8.4  | -2.1 | NFC West    | missed     | 2011 | 
| New England Patriots     | 12  | 4    | 0   | 0.75  | 557 | 331 | 226  | 14.1  | -1.4 | 12.8  | 12.2  | 0.5  | AFC East    | divwin     | 2012 | 
| Miami Dolphins           | 7   | 9    | 0   | 0.438 | 288 | 317 | -29  | -1.8  | -0.8 | -2.6  | -5.5  | 2.9  | AFC East    | missed     | 2012 | 
| New York Jets            | 6   | 10   | 0   | 0.375 | 281 | 375 | -94  | -5.9  | 0.0  | -5.9  | -5.1  | -0.9 | AFC East    | missed     | 2012 | 
| Buffalo Bills            | 6   | 10   | 0   | 0.375 | 344 | 435 | -91  | -5.7  | -1.0 | -6.7  | -0.9  | -5.8 | AFC East    | missed     | 2012 | 
| Baltimore Ravens         | 10  | 6    | 0   | 0.625 | 398 | 344 | 54   | 3.4   | -0.5 | 2.9   | 1.9   | 1.0  | AFC North   | divwin     | 2012 | 
| Cincinnati Bengals       | 10  | 6    | 0   | 0.625 | 391 | 320 | 71   | 4.4   | -2.4 | 2.1   | 1.2   | 0.9  | AFC North   | wildcard   | 2012 | 
| Pittsburgh Steelers      | 8   | 8    | 0   | 0.5   | 336 | 314 | 22   | 1.4   | -2.0 | -0.7  | -2.8  | 2.1  | AFC North   | missed     | 2012 | 
| Cleveland Browns         | 5   | 11   | 0   | 0.313 | 302 | 368 | -66  | -4.1  | -1.2 | -5.3  | -4.6  | -0.7 | AFC North   | missed     | 2012 | 
| Houston Texans           | 12  | 4    | 0   | 0.75  | 416 | 331 | 85   | 5.3   | -1.8 | 3.5   | 1.8   | 1.7  | AFC South   | divwin     | 2012 | 
| Indianapolis Colts       | 11  | 5    | 0   | 0.688 | 357 | 387 | -30  | -1.9  | -2.8 | -4.7  | -1.9  | -2.8 | AFC South   | wildcard   | 2012 | 
| Tennessee Titans         | 6   | 10   | 0   | 0.375 | 330 | 471 | -141 | -8.8  | -1.2 | -10.0 | -2.6  | -7.4 | AFC South   | missed     | 2012 | 
| Jacksonville Jaguars     | 2   | 14   | 0   | 0.125 | 255 | 444 | -189 | -11.8 | -1.1 | -13.0 | -8.1  | -4.9 | AFC South   | missed     | 2012 | 
| Denver Broncos           | 13  | 3    | 0   | 0.813 | 481 | 289 | 192  | 12.0  | -1.9 | 10.1  | 6.3   | 3.8  | AFC West    | divwin     | 2012 | 
| San Diego Chargers       | 7   | 9    | 0   | 0.438 | 350 | 350 | 0    | 0.0   | -2.3 | -2.3  | -2.0  | -0.4 | AFC West    | missed     | 2012 | 
| Oakland Raiders          | 4   | 12   | 0   | 0.25  | 290 | 443 | -153 | -9.6  | -1.3 | -10.8 | -4.6  | -6.2 | AFC West    | missed     | 2012 | 
| Kansas City Chiefs       | 2   | 14   | 0   | 0.125 | 211 | 425 | -214 | -13.4 | -0.6 | -14.0 | -10.3 | -3.7 | AFC West    | missed     | 2012 | 
| Washington Redskins      | 10  | 6    | 0   | 0.625 | 436 | 388 | 48   | 3.0   | 0.4  | 3.4   | 4.6   | -1.2 | NFC East    | divwin     | 2012 | 
| New York Giants          | 9   | 7    | 0   | 0.563 | 429 | 344 | 85   | 5.3   | 0.9  | 6.2   | 4.0   | 2.2  | NFC East    | missed     | 2012 | 
| Dallas Cowboys           | 8   | 8    | 0   | 0.5   | 376 | 400 | -24  | -1.5  | 1.8  | 0.3   | 1.4   | -1.2 | NFC East    | missed     | 2012 | 
| Philadelphia Eagles      | 4   | 12   | 0   | 0.25  | 280 | 444 | -164 | -10.3 | 1.4  | -8.9  | -5.3  | -3.6 | NFC East    | missed     | 2012 | 
| Green Bay Packers        | 11  | 5    | 0   | 0.688 | 433 | 336 | 97   | 6.1   | 1.2  | 7.3   | 4.9   | 2.4  | NFC North   | divwin     | 2012 | 
| Minnesota Vikings        | 10  | 6    | 0   | 0.625 | 379 | 348 | 31   | 1.9   | 1.4  | 3.4   | 1.6   | 1.8  | NFC North   | wildcard   | 2012 | 
| Chicago Bears            | 10  | 6    | 0   | 0.625 | 375 | 277 | 98   | 6.1   | 0.8  | 6.9   | 1.0   | 6.0  | NFC North   | missed     | 2012 | 
| Detroit Lions            | 4   | 12   | 0   | 0.25  | 372 | 437 | -65  | -4.1  | 1.8  | -2.3  | 2.1   | -4.4 | NFC North   | missed     | 2012 | 
| Atlanta Falcons          | 13  | 3    | 0   | 0.813 | 419 | 299 | 120  | 7.5   | -1.1 | 6.4   | 2.0   | 4.5  | NFC South   | divwin     | 2012 | 
| Carolina Panthers        | 7   | 9    | 0   | 0.438 | 357 | 363 | -6   | -0.4  | 1.2  | 0.8   | -0.5  | 1.3  | NFC South   | missed     | 2012 | 
| New Orleans Saints       | 7   | 9    | 0   | 0.438 | 461 | 454 | 7    | 0.4   | 1.0  | 1.4   | 6.5   | -5.1 | NFC South   | missed     | 2012 | 
| Tampa Bay Buccaneers     | 7   | 9    | 0   | 0.438 | 389 | 394 | -5   | -0.3  | 0.3  | 0.0   | 1.3   | -1.3 | NFC South   | missed     | 2012 | 
| San Francisco 49ers      | 11  | 4    | 1   | 0.719 | 397 | 273 | 124  | 7.8   | 2.5  | 10.2  | 3.5   | 6.7  | NFC West    | divwin     | 2012 | 
| Seattle Seahawks         | 11  | 5    | 0   | 0.688 | 412 | 245 | 167  | 10.4  | 1.8  | 12.2  | 4.5   | 7.7  | NFC West    | wildcard   | 2012 | 
| St. Louis Rams           | 7   | 8    | 1   | 0.469 | 299 | 348 | -49  | -3.1  | 3.4  | 0.4   | -2.1  | 2.4  | NFC West    | missed     | 2012 | 
| Arizona Cardinals        | 5   | 11   | 0   | 0.313 | 250 | 357 | -107 | -6.7  | 3.5  | -3.2  | -4.8  | 1.6  | NFC West    | missed     | 2012 | 
| New England Patriots     | 12  | 4    | 0   | 0.75  | 444 | 338 | 106  | 6.6   | -0.7 | 5.9   | 4.5   | 1.4  | AFC East    | divwin     | 2013 | 
| New York Jets            | 8   | 8    | 0   | 0.5   | 290 | 387 | -97  | -6.1  | 0.0  | -6.1  | -4.7  | -1.4 | AFC East    | missed     | 2013 | 
| Miami Dolphins           | 8   | 8    | 0   | 0.5   | 317 | 335 | -18  | -1.1  | 0.3  | -0.8  | -2.9  | 2.1  | AFC East    | missed     | 2013 | 
| Buffalo Bills            | 6   | 10   | 0   | 0.375 | 339 | 388 | -49  | -3.1  | -0.1 | -3.2  | -1.3  | -1.9 | AFC East    | missed     | 2013 | 
| Cincinnati Bengals       | 11  | 5    | 0   | 0.688 | 430 | 305 | 125  | 7.8   | -2.5 | 5.4   | 2.3   | 3.0  | AFC North   | divwin     | 2013 | 
| Pittsburgh Steelers      | 8   | 8    | 0   | 0.5   | 379 | 370 | 9    | 0.6   | -2.5 | -2.0  | -0.9  | -1.0 | AFC North   | missed     | 2013 | 
| Baltimore Ravens         | 8   | 8    | 0   | 0.5   | 320 | 352 | -32  | -2.0  | -1.5 | -3.5  | -5.0  | 1.4  | AFC North   | missed     | 2013 | 
| Cleveland Browns         | 4   | 12   | 0   | 0.25  | 308 | 406 | -98  | -6.1  | -1.6 | -7.7  | -4.8  | -2.9 | AFC North   | missed     | 2013 | 
| Indianapolis Colts       | 11  | 5    | 0   | 0.688 | 391 | 336 | 55   | 3.4   | 0.6  | 4.0   | 1.7   | 2.3  | AFC South   | divwin     | 2013 | 
| Tennessee Titans         | 7   | 9    | 0   | 0.438 | 362 | 381 | -19  | -1.2  | 0.4  | -0.8  | -0.2  | -0.6 | AFC South   | missed     | 2013 | 
| Jacksonville Jaguars     | 4   | 12   | 0   | 0.25  | 247 | 449 | -202 | -12.6 | 1.5  | -11.1 | -7.1  | -4.0 | AFC South   | missed     | 2013 | 
| Houston Texans           | 2   | 14   | 0   | 0.125 | 276 | 428 | -152 | -9.5  | 1.9  | -7.6  | -5.0  | -2.6 | AFC South   | missed     | 2013 | 
| Denver Broncos           | 13  | 3    | 0   | 0.813 | 606 | 399 | 207  | 12.9  | -1.6 | 11.4  | 14.1  | -2.7 | AFC West    | divwin     | 2013 | 
| Kansas City Chiefs       | 11  | 5    | 0   | 0.688 | 430 | 305 | 125  | 7.8   | -1.7 | 6.1   | 1.7   | 4.3  | AFC West    | wildcard   | 2013 | 
| San Diego Chargers       | 9   | 7    | 0   | 0.563 | 396 | 348 | 48   | 3.0   | -0.3 | 2.7   | 0.5   | 2.1  | AFC West    | wildcard   | 2013 | 
| Oakland Raiders          | 4   | 12   | 0   | 0.25  | 322 | 453 | -131 | -8.2  | 0.2  | -8.0  | -3.8  | -4.2 | AFC West    | missed     | 2013 | 
| Philadelphia Eagles      | 10  | 6    | 0   | 0.625 | 442 | 382 | 60   | 3.8   | -1.9 | 1.9   | 2.3   | -0.5 | NFC East    | divwin     | 2013 | 
| Dallas Cowboys           | 8   | 8    | 0   | 0.5   | 439 | 432 | 7    | 0.4   | -1.1 | -0.7  | 2.7   | -3.4 | NFC East    | missed     | 2013 | 
| New York Giants          | 7   | 9    | 0   | 0.438 | 294 | 383 | -89  | -5.6  | 0.2  | -5.4  | -6.2  | 0.8  | NFC East    | missed     | 2013 | 
| Washington Redskins      | 3   | 13   | 0   | 0.188 | 334 | 478 | -144 | -9.0  | -0.3 | -9.3  | -3.9  | -5.4 | NFC East    | missed     | 2013 | 
| Green Bay Packers        | 8   | 7    | 1   | 0.531 | 417 | 428 | -11  | -0.7  | -2.4 | -3.1  | 0.5   | -3.6 | NFC North   | divwin     | 2013 | 
| Chicago Bears            | 8   | 8    | 0   | 0.5   | 445 | 478 | -33  | -2.1  | -2.1 | -4.1  | 3.0   | -7.1 | NFC North   | missed     | 2013 | 
| Detroit Lions            | 7   | 9    | 0   | 0.438 | 395 | 376 | 19   | 1.2   | -2.8 | -1.6  | -1.2  | -0.5 | NFC North   | missed     | 2013 | 
| Minnesota Vikings        | 5   | 10   | 1   | 0.344 | 391 | 480 | -89  | -5.6  | -1.1 | -6.6  | 0.2   | -6.9 | NFC North   | missed     | 2013 | 
| Carolina Panthers        | 12  | 4    | 0   | 0.75  | 366 | 241 | 125  | 7.8   | 1.4  | 9.2   | 0.6   | 8.6  | NFC South   | divwin     | 2013 | 
| New Orleans Saints       | 11  | 5    | 0   | 0.688 | 414 | 304 | 110  | 6.9   | 1.9  | 8.8   | 3.8   | 5.0  | NFC South   | wildcard   | 2013 | 
| Atlanta Falcons          | 4   | 12   | 0   | 0.25  | 353 | 443 | -90  | -5.6  | 2.9  | -2.8  | 1.2   | -3.9 | NFC South   | missed     | 2013 | 
| Tampa Bay Buccaneers     | 4   | 12   | 0   | 0.25  | 288 | 389 | -101 | -6.3  | 3.6  | -2.7  | -2.9  | 0.3  | NFC South   | missed     | 2013 | 
| Seattle Seahawks         | 13  | 3    | 0   | 0.813 | 417 | 231 | 186  | 11.6  | 1.4  | 13.0  | 4.1   | 8.9  | NFC West    | divwin     | 2013 | 
| San Francisco 49ers      | 12  | 4    | 0   | 0.75  | 406 | 272 | 134  | 8.4   | 1.8  | 10.1  | 3.5   | 6.6  | NFC West    | wildcard   | 2013 | 
| Arizona Cardinals        | 10  | 6    | 0   | 0.625 | 379 | 324 | 55   | 3.4   | 3.0  | 6.4   | 2.7   | 3.7  | NFC West    | missed     | 2013 | 
| St. Louis Rams           | 7   | 9    | 0   | 0.438 | 348 | 364 | -16  | -1.0  | 3.2  | 2.2   | 0.4   | 1.8  | NFC West    | missed     | 2013 | 
| New England Patriots     | 12  | 4    | 0   | 0.75  | 468 | 313 | 155  | 9.7   | 1.3  | 10.9  | 7.5   | 3.5  | AFC East    | divwin     | 2014 | 
| Buffalo Bills            | 9   | 7    | 0   | 0.563 | 343 | 289 | 54   | 3.4   | 1.6  | 4.9   | -0.4  | 5.3  | AFC East    | missed     | 2014 | 
| Miami Dolphins           | 8   | 8    | 0   | 0.5   | 388 | 373 | 15   | 0.9   | 1.6  | 2.6   | 2.9   | -0.4 | AFC East    | missed     | 2014 | 
| New York Jets            | 4   | 12   | 0   | 0.25  | 283 | 401 | -118 | -7.4  | 2.3  | -5.0  | -4.0  | -1.0 | AFC East    | missed     | 2014 | 
| Pittsburgh Steelers      | 11  | 5    | 0   | 0.688 | 436 | 368 | 68   | 4.3   | -2.0 | 2.2   | 4.4   | -2.1 | AFC North   | divwin     | 2014 | 
| Cincinnati Bengals       | 10  | 5    | 1   | 0.656 | 365 | 344 | 21   | 1.3   | -0.6 | 0.7   | -0.5  | 1.3  | AFC North   | wildcard   | 2014 | 
| Baltimore Ravens         | 10  | 6    | 0   | 0.625 | 409 | 302 | 107  | 6.7   | -2.1 | 4.6   | 1.8   | 2.8  | AFC North   | wildcard   | 2014 | 
| Cleveland Browns         | 7   | 9    | 0   | 0.438 | 299 | 337 | -38  | -2.4  | -1.5 | -3.9  | -4.8  | 0.9  | AFC North   | missed     | 2014 | 
| Indianapolis Colts       | 11  | 5    | 0   | 0.688 | 458 | 369 | 89   | 5.6   | -1.1 | 4.4   | 5.2   | -0.8 | AFC South   | divwin     | 2014 | 
| Houston Texans           | 9   | 7    | 0   | 0.563 | 372 | 307 | 65   | 4.1   | -2.3 | 1.7   | -0.8  | 2.5  | AFC South   | missed     | 2014 | 
| Jacksonville Jaguars     | 3   | 13   | 0   | 0.188 | 249 | 412 | -163 | -10.2 | -0.3 | -10.5 | -7.8  | -2.7 | AFC South   | missed     | 2014 | 
| Tennessee Titans         | 2   | 14   | 0   | 0.125 | 254 | 438 | -184 | -11.5 | -0.3 | -11.8 | -7.0  | -4.9 | AFC South   | missed     | 2014 | 
| Denver Broncos           | 12  | 4    | 0   | 0.75  | 482 | 354 | 128  | 8.0   | 1.6  | 9.6   | 9.2   | 0.4  | AFC West    | divwin     | 2014 | 
| Kansas City Chiefs       | 9   | 7    | 0   | 0.563 | 353 | 281 | 72   | 4.5   | 1.2  | 5.7   | 0.0   | 5.7  | AFC West    | missed     | 2014 | 
| San Diego Chargers       | 9   | 7    | 0   | 0.563 | 348 | 348 | 0    | 0.0   | 1.9  | 1.9   | 0.7   | 1.2  | AFC West    | missed     | 2014 | 
| Oakland Raiders          | 3   | 13   | 0   | 0.188 | 253 | 452 | -199 | -12.4 | 3.4  | -9.0  | -4.3  | -4.7 | AFC West    | missed     | 2014 | 
| Dallas Cowboys           | 12  | 4    | 0   | 0.75  | 467 | 352 | 115  | 7.2   | -1.8 | 5.4   | 5.3   | 0.1  | NFC East    | divwin     | 2014 | 
| Philadelphia Eagles      | 10  | 6    | 0   | 0.625 | 474 | 400 | 74   | 4.6   | -0.7 | 3.9   | 6.6   | -2.7 | NFC East    | missed     | 2014 | 
| New York Giants          | 6   | 10   | 0   | 0.375 | 380 | 400 | -20  | -1.3  | -0.4 | -1.7  | 0.8   | -2.5 | NFC East    | missed     | 2014 | 
| Washington Redskins      | 4   | 12   | 0   | 0.25  | 301 | 438 | -137 | -8.6  | -0.2 | -8.7  | -4.0  | -4.7 | NFC East    | missed     | 2014 | 
| Green Bay Packers        | 12  | 4    | 0   | 0.75  | 486 | 348 | 138  | 8.6   | -0.3 | 8.3   | 7.9   | 0.4  | NFC North   | divwin     | 2014 | 
| Detroit Lions            | 11  | 5    | 0   | 0.688 | 321 | 282 | 39   | 2.4   | -0.4 | 2.1   | -3.2  | 5.2  | NFC North   | wildcard   | 2014 | 
| Minnesota Vikings        | 7   | 9    | 0   | 0.438 | 325 | 343 | -18  | -1.1  | -0.5 | -1.7  | -2.8  | 1.1  | NFC North   | missed     | 2014 | 
| Chicago Bears            | 5   | 11   | 0   | 0.313 | 319 | 442 | -123 | -7.7  | 1.0  | -6.7  | -2.0  | -4.7 | NFC North   | missed     | 2014 | 
| Carolina Panthers        | 7   | 8    | 1   | 0.469 | 339 | 374 | -35  | -2.2  | -0.9 | -3.1  | -2.4  | -0.7 | NFC South   | divwin     | 2014 | 
| New Orleans Saints       | 7   | 9    | 0   | 0.438 | 401 | 424 | -23  | -1.4  | -1.5 | -2.9  | 1.9   | -4.8 | NFC South   | missed     | 2014 | 
| Atlanta Falcons          | 6   | 10   | 0   | 0.375 | 381 | 417 | -36  | -2.3  | -1.6 | -3.8  | 0.6   | -4.4 | NFC South   | missed     | 2014 | 
| Tampa Bay Buccaneers     | 2   | 14   | 0   | 0.125 | 277 | 410 | -133 | -8.3  | -1.5 | -9.8  | -6.5  | -3.3 | NFC South   | missed     | 2014 | 
| Seattle Seahawks         | 12  | 4    | 0   | 0.75  | 394 | 254 | 140  | 8.8   | 0.8  | 9.5   | 2.4   | 7.1  | NFC West    | divwin     | 2014 | 
| Arizona Cardinals        | 11  | 5    | 0   | 0.688 | 310 | 299 | 11   | 0.7   | 1.3  | 2.0   | -2.4  | 4.4  | NFC West    | wildcard   | 2014 | 
| San Francisco 49ers      | 8   | 8    | 0   | 0.5   | 306 | 340 | -34  | -2.1  | 1.2  | -1.0  | -3.0  | 2.1  | NFC West    | missed     | 2014 | 
| St. Louis Rams           | 6   | 10   | 0   | 0.375 | 324 | 354 | -30  | -1.9  | 1.0  | -0.8  | -1.2  | 0.4  | NFC West    | missed     | 2014 | 
| New England Patriots     | 12  | 4    | 0   | 0.75  | 465 | 315 | 150  | 9.4   | -2.4 | 7.0   | 5.3   | 1.7  | AFC East    | divwin     | 2015 | 
| New York Jets            | 10  | 6    | 0   | 0.625 | 387 | 314 | 73   | 4.6   | -3.0 | 1.5   | -0.5  | 2.0  | AFC East    | missed     | 2015 | 
| Buffalo Bills            | 8   | 8    | 0   | 0.5   | 379 | 359 | 20   | 1.3   | -1.2 | 0.0   | 0.3   | -0.2 | AFC East    | missed     | 2015 | 
| Miami Dolphins           | 6   | 10   | 0   | 0.375 | 310 | 389 | -79  | -4.9  | -1.9 | -6.8  | -4.7  | -2.2 | AFC East    | missed     | 2015 | 
| Cincinnati Bengals       | 12  | 4    | 0   | 0.75  | 419 | 279 | 140  | 8.8   | 1.9  | 10.6  | 4.8   | 5.8  | AFC North   | divwin     | 2015 | 
| Pittsburgh Steelers      | 10  | 6    | 0   | 0.625 | 423 | 319 | 104  | 6.5   | 2.2  | 8.7   | 5.1   | 3.6  | AFC North   | wildcard   | 2015 | 
| Baltimore Ravens         | 5   | 11   | 0   | 0.313 | 328 | 401 | -73  | -4.6  | 2.6  | -1.9  | -0.7  | -1.2 | AFC North   | missed     | 2015 | 
| Cleveland Browns         | 3   | 13   | 0   | 0.188 | 278 | 432 | -154 | -9.6  | 3.5  | -6.1  | -3.2  | -2.9 | AFC North   | missed     | 2015 | 
| Houston Texans           | 9   | 7    | 0   | 0.563 | 339 | 313 | 26   | 1.6   | -2.4 | -0.8  | -3.3  | 2.6  | AFC South   | divwin     | 2015 | 
| Indianapolis Colts       | 8   | 8    | 0   | 0.5   | 333 | 408 | -75  | -4.7  | -2.0 | -6.7  | -3.1  | -3.6 | AFC South   | missed     | 2015 | 
| Jacksonville Jaguars     | 5   | 11   | 0   | 0.313 | 376 | 448 | -72  | -4.5  | -3.0 | -7.5  | -0.7  | -6.9 | AFC South   | missed     | 2015 | 
| Tennessee Titans         | 3   | 13   | 0   | 0.188 | 299 | 423 | -124 | -7.8  | -2.8 | -10.5 | -5.9  | -4.6 | AFC South   | missed     | 2015 | 
| Denver Broncos           | 12  | 4    | 0   | 0.75  | 355 | 296 | 59   | 3.7   | 2.1  | 5.8   | 0.3   | 5.5  | AFC West    | divwin     | 2015 | 
| Kansas City Chiefs       | 11  | 5    | 0   | 0.688 | 405 | 287 | 118  | 7.4   | 1.6  | 9.0   | 3.7   | 5.3  | AFC West    | wildcard   | 2015 | 
| Oakland Raiders          | 7   | 9    | 0   | 0.438 | 359 | 399 | -40  | -2.5  | 2.3  | -0.2  | 1.4   | -1.6 | AFC West    | missed     | 2015 | 
| San Diego Chargers       | 4   | 12   | 0   | 0.25  | 320 | 398 | -78  | -4.9  | 2.2  | -2.6  | -1.5  | -1.1 | AFC West    | missed     | 2015 | 
| Washington Redskins      | 9   | 7    | 0   | 0.563 | 388 | 379 | 9    | 0.6   | -2.5 | -1.9  | -0.2  | -1.8 | NFC East    | divwin     | 2015 | 
| Philadelphia Eagles      | 7   | 9    | 0   | 0.438 | 377 | 430 | -53  | -3.3  | -1.3 | -4.6  | -0.6  | -4.0 | NFC East    | missed     | 2015 | 
| New York Giants          | 6   | 10   | 0   | 0.375 | 420 | 442 | -22  | -1.4  | -2.2 | -3.6  | 2.5   | -6.1 | NFC East    | missed     | 2015 | 
| Dallas Cowboys           | 4   | 12   | 0   | 0.25  | 275 | 374 | -99  | -6.2  | -0.7 | -6.9  | -7.0  | 0.1  | NFC East    | missed     | 2015 | 
| Minnesota Vikings        | 11  | 5    | 0   | 0.688 | 365 | 302 | 63   | 3.9   | 1.9  | 5.8   | 1.1   | 4.7  | NFC North   | divwin     | 2015 | 
| Green Bay Packers        | 10  | 6    | 0   | 0.625 | 368 | 323 | 45   | 2.8   | 2.5  | 5.3   | 2.0   | 3.3  | NFC North   | wildcard   | 2015 | 
| Detroit Lions            | 7   | 9    | 0   | 0.438 | 358 | 400 | -42  | -2.6  | 2.4  | -0.2  | 1.0   | -1.3 | NFC North   | missed     | 2015 | 
| Chicago Bears            | 6   | 10   | 0   | 0.375 | 335 | 397 | -62  | -3.9  | 2.6  | -1.3  | -0.1  | -1.2 | NFC North   | missed     | 2015 | 
| Carolina Panthers        | 15  | 1    | 0   | 0.938 | 500 | 308 | 192  | 12.0  | -3.9 | 8.1   | 6.0   | 2.1  | NFC South   | divwin     | 2015 | 
| Atlanta Falcons          | 8   | 8    | 0   | 0.5   | 339 | 345 | -6   | -0.4  | -3.4 | -3.8  | -4.0  | 0.3  | NFC South   | missed     | 2015 | 
| New Orleans Saints       | 7   | 9    | 0   | 0.438 | 408 | 476 | -68  | -4.3  | -2.3 | -6.6  | 1.1   | -7.6 | NFC South   | missed     | 2015 | 
| Tampa Bay Buccaneers     | 6   | 10   | 0   | 0.375 | 342 | 417 | -75  | -4.7  | -3.0 | -7.7  | -3.5  | -4.2 | NFC South   | missed     | 2015 | 
| Arizona Cardinals        | 13  | 3    | 0   | 0.813 | 489 | 313 | 176  | 11.0  | 1.3  | 12.3  | 9.0   | 3.4  | NFC West    | divwin     | 2015 | 
| Seattle Seahawks         | 10  | 6    | 0   | 0.625 | 423 | 277 | 146  | 9.1   | 2.2  | 11.3  | 5.4   | 6.0  | NFC West    | wildcard   | 2015 | 
| St. Louis Rams           | 7   | 9    | 0   | 0.438 | 280 | 330 | -50  | -3.1  | 3.0  | -0.2  | -3.8  | 3.6  | NFC West    | missed     | 2015 | 
| San Francisco 49ers      | 5   | 11   | 0   | 0.313 | 238 | 387 | -149 | -9.3  | 3.8  | -5.5  | -6.0  | 0.5  | NFC West    | missed     | 2015 | 
| New England Patriots     | 14  | 2    | 0   | 0.875 | 441 | 250 | 191  | 11.9  | -2.7 | 9.3   | 4.3   | 5.0  | AFC East    | divwin     | 2016 | 
| Miami Dolphins           | 10  | 6    | 0   | 0.625 | 363 | 380 | -17  | -1.1  | -1.3 | -2.4  | -0.6  | -1.8 | AFC East    | wildcard   | 2016 | 
| Buffalo Bills            | 7   | 9    | 0   | 0.438 | 399 | 378 | 21   | 1.3   | -1.6 | -0.3  | 1.8   | -2.2 | AFC East    | missed     | 2016 | 
| New York Jets            | 5   | 11   | 0   | 0.313 | 275 | 409 | -134 | -8.4  | -0.1 | -8.5  | -5.5  | -3.0 | AFC East    | missed     | 2016 | 
| Pittsburgh Steelers      | 11  | 5    | 0   | 0.688 | 399 | 327 | 72   | 4.5   | 0.2  | 4.7   | 2.8   | 2.0  | AFC North   | divwin     | 2016 | 
| Baltimore Ravens         | 8   | 8    | 0   | 0.5   | 343 | 321 | 22   | 1.4   | 0.2  | 1.5   | -1.1  | 2.6  | AFC North   | missed     | 2016 | 
| Cincinnati Bengals       | 6   | 9    | 1   | 0.406 | 325 | 315 | 10   | 0.6   | 0.4  | 1.0   | -1.5  | 2.5  | AFC North   | missed     | 2016 | 
| Cleveland Browns         | 1   | 15   | 0   | 0.063 | 264 | 452 | -188 | -11.8 | 1.7  | -10.1 | -5.2  | -4.9 | AFC North   | missed     | 2016 | 
| Houston Texans           | 9   | 7    | 0   | 0.563 | 279 | 328 | -49  | -3.1  | 0.4  | -2.6  | -5.3  | 2.7  | AFC South   | divwin     | 2016 | 
| Tennessee Titans         | 9   | 7    | 0   | 0.563 | 381 | 378 | 3    | 0.2   | -1.2 | -1.0  | 0.7   | -1.7 | AFC South   | missed     | 2016 | 
| Indianapolis Colts       | 8   | 8    | 0   | 0.5   | 411 | 392 | 19   | 1.2   | -0.8 | 0.4   | 3.1   | -2.7 | AFC South   | missed     | 2016 | 
| Jacksonville Jaguars     | 3   | 13   | 0   | 0.188 | 318 | 400 | -82  | -5.1  | 0.2  | -5.0  | -2.7  | -2.3 | AFC South   | missed     | 2016 | 
| Kansas City Chiefs       | 12  | 4    | 0   | 0.75  | 389 | 311 | 78   | 4.9   | 0.7  | 5.6   | 1.2   | 4.4  | AFC West    | divwin     | 2016 | 
| Oakland Raiders          | 12  | 4    | 0   | 0.75  | 416 | 385 | 31   | 1.9   | 1.3  | 3.3   | 3.5   | -0.3 | AFC West    | wildcard   | 2016 | 
| Denver Broncos           | 9   | 7    | 0   | 0.563 | 333 | 297 | 36   | 2.3   | 1.8  | 4.0   | -2.0  | 6.1  | AFC West    | missed     | 2016 | 
| San Diego Chargers       | 5   | 11   | 0   | 0.313 | 410 | 423 | -13  | -0.8  | 0.9  | 0.1   | 3.0   | -3.0 | AFC West    | missed     | 2016 | 
| Dallas Cowboys           | 13  | 3    | 0   | 0.813 | 421 | 306 | 115  | 7.2   | -0.2 | 7.0   | 4.1   | 2.9  | NFC East    | divwin     | 2016 | 
| New York Giants          | 11  | 5    | 0   | 0.688 | 310 | 284 | 26   | 1.6   | 0.5  | 2.1   | -3.2  | 5.4  | NFC East    | wildcard   | 2016 | 
| Washington Redskins      | 8   | 7    | 1   | 0.531 | 396 | 383 | 13   | 0.8   | 1.2  | 2.0   | 3.3   | -1.3 | NFC East    | missed     | 2016 | 
| Philadelphia Eagles      | 7   | 9    | 0   | 0.438 | 367 | 331 | 36   | 2.3   | 1.6  | 3.8   | 1.3   | 2.5  | NFC East    | missed     | 2016 | 
| Green Bay Packers        | 10  | 6    | 0   | 0.625 | 432 | 388 | 44   | 2.8   | 0.1  | 2.8   | 4.9   | -2.0 | NFC North   | divwin     | 2016 | 
| Detroit Lions            | 9   | 7    | 0   | 0.563 | 346 | 358 | -12  | -0.8  | -0.6 | -1.4  | -1.3  | -0.1 | NFC North   | wildcard   | 2016 | 
| Minnesota Vikings        | 8   | 8    | 0   | 0.5   | 327 | 307 | 20   | 1.3   | -0.3 | 0.9   | -2.6  | 3.6  | NFC North   | missed     | 2016 | 
| Chicago Bears            | 3   | 13   | 0   | 0.188 | 279 | 399 | -120 | -7.5  | 0.0  | -7.5  | -5.2  | -2.3 | NFC North   | missed     | 2016 | 
| Atlanta Falcons          | 11  | 5    | 0   | 0.688 | 540 | 406 | 134  | 8.4   | 0.1  | 8.5   | 10.5  | -2.0 | NFC South   | divwin     | 2016 | 
| Tampa Bay Buccaneers     | 9   | 7    | 0   | 0.563 | 354 | 369 | -15  | -0.9  | 0.7  | -0.2  | -1.5  | 1.3  | NFC South   | missed     | 2016 | 
| New Orleans Saints       | 7   | 9    | 0   | 0.438 | 469 | 454 | 15   | 0.9   | 0.6  | 1.5   | 6.8   | -5.3 | NFC South   | missed     | 2016 | 
| Carolina Panthers        | 6   | 10   | 0   | 0.375 | 369 | 402 | -33  | -2.1  | 1.1  | -1.0  | -0.2  | -0.8 | NFC South   | missed     | 2016 | 
| Seattle Seahawks         | 10  | 5    | 1   | 0.656 | 354 | 292 | 62   | 3.9   | -1.7 | 2.1   | -2.4  | 4.5  | NFC West    | divwin     | 2016 | 
| Arizona Cardinals        | 7   | 8    | 1   | 0.469 | 418 | 362 | 56   | 3.5   | -1.9 | 1.6   | 2.4   | -0.8 | NFC West    | missed     | 2016 | 
| Los Angeles Rams         | 4   | 12   | 0   | 0.25  | 224 | 394 | -170 | -10.6 | -0.5 | -11.1 | -9.5  | -1.6 | NFC West    | missed     | 2016 | 
| San Francisco 49ers      | 2   | 14   | 0   | 0.125 | 309 | 480 | -171 | -10.7 | -0.5 | -11.2 | -3.7  | -7.5 | NFC West    | missed     | 2016 | 
| New England Patriots     | 13  | 3    | 0   | 0.813 | 458 | 296 | 162  | 10.1  | -1.2 | 8.9   | 6.3   | 2.6  | AFC East    | divwin     | 2017 | 
| Buffalo Bills            | 9   | 7    | 0   | 0.563 | 302 | 359 | -57  | -3.6  | -0.5 | -4.0  | -3.0  | -1.0 | AFC East    | wildcard   | 2017 | 
| Miami Dolphins           | 6   | 10   | 0   | 0.375 | 281 | 393 | -112 | -7.0  | 0.7  | -6.3  | -3.9  | -2.4 | AFC East    | missed     | 2017 | 
| New York Jets            | 5   | 11   | 0   | 0.313 | 298 | 382 | -84  | -5.3  | 0.3  | -4.9  | -2.9  | -2.1 | AFC East    | missed     | 2017 | 
| Pittsburgh Steelers      | 13  | 3    | 0   | 0.813 | 406 | 308 | 98   | 6.1   | -1.1 | 5.0   | 3.2   | 1.8  | AFC North   | divwin     | 2017 | 
| Baltimore Ravens         | 9   | 7    | 0   | 0.563 | 395 | 303 | 92   | 5.8   | -2.4 | 3.4   | 2.2   | 1.2  | AFC North   | missed     | 2017 | 
| Cincinnati Bengals       | 7   | 9    | 0   | 0.438 | 290 | 349 | -59  | -3.7  | -1.3 | -5.0  | -4.1  | -0.9 | AFC North   | missed     | 2017 | 
| Cleveland Browns         | 0   | 16   | 0   | 0.0   | 234 | 410 | -176 | -11.0 | 0.0  | -11.0 | -6.8  | -4.1 | AFC North   | missed     | 2017 | 
| Jacksonville Jaguars     | 10  | 6    | 0   | 0.625 | 417 | 268 | 149  | 9.3   | -2.8 | 6.5   | 3.0   | 3.6  | AFC South   | divwin     | 2017 | 
| Tennessee Titans         | 9   | 7    | 0   | 0.563 | 334 | 356 | -22  | -1.4  | -2.1 | -3.5  | -2.0  | -1.5 | AFC South   | wildcard   | 2017 | 
| Indianapolis Colts       | 4   | 12   | 0   | 0.25  | 263 | 404 | -141 | -8.8  | -1.3 | -10.1 | -6.1  | -4.0 | AFC South   | missed     | 2017 | 
| Houston Texans           | 4   | 12   | 0   | 0.25  | 338 | 436 | -98  | -6.1  | -0.3 | -6.4  | -0.8  | -5.6 | AFC South   | missed     | 2017 | 
| Kansas City Chiefs       | 10  | 6    | 0   | 0.625 | 415 | 339 | 76   | 4.8   | -1.3 | 3.4   | 3.8   | -0.3 | AFC West    | divwin     | 2017 | 
| Los Angeles Chargers     | 9   | 7    | 0   | 0.563 | 355 | 272 | 83   | 5.2   | -1.5 | 3.6   | -0.3  | 4.0  | AFC West    | missed     | 2017 | 
| Oakland Raiders          | 6   | 10   | 0   | 0.375 | 301 | 373 | -72  | -4.5  | -0.2 | -4.7  | -3.0  | -1.8 | AFC West    | missed     | 2017 | 
| Denver Broncos           | 5   | 11   | 0   | 0.313 | 289 | 382 | -93  | -5.8  | -0.9 | -6.7  | -3.9  | -2.9 | AFC West    | missed     | 2017 | 
| Philadelphia Eagles      | 13  | 3    | 0   | 0.813 | 457 | 295 | 162  | 10.1  | -0.7 | 9.4   | 7.0   | 2.5  | NFC East    | divwin     | 2017 | 
| Dallas Cowboys           | 9   | 7    | 0   | 0.563 | 354 | 332 | 22   | 1.4   | 0.2  | 1.6   | 0.4   | 1.2  | NFC East    | missed     | 2017 | 
| Washington Redskins      | 7   | 9    | 0   | 0.438 | 342 | 388 | -46  | -2.9  | 1.6  | -1.3  | 0.5   | -1.8 | NFC East    | missed     | 2017 | 
| New York Giants          | 3   | 13   | 0   | 0.188 | 246 | 388 | -142 | -8.9  | 1.3  | -7.6  | -6.4  | -1.2 | NFC East    | missed     | 2017 | 
| Minnesota Vikings        | 13  | 3    | 0   | 0.813 | 382 | 252 | 130  | 8.1   | 1.0  | 9.1   | 2.3   | 6.8  | NFC North   | divwin     | 2017 | 
| Detroit Lions            | 9   | 7    | 0   | 0.563 | 410 | 376 | 34   | 2.1   | 0.6  | 2.7   | 5.2   | -2.5 | NFC North   | missed     | 2017 | 
| Green Bay Packers        | 7   | 9    | 0   | 0.438 | 320 | 384 | -64  | -4.0  | 2.1  | -1.9  | -0.3  | -1.6 | NFC North   | missed     | 2017 | 
| Chicago Bears            | 5   | 11   | 0   | 0.313 | 264 | 320 | -56  | -3.5  | 2.2  | -1.3  | -4.6  | 3.3  | NFC North   | missed     | 2017 | 
| New Orleans Saints       | 11  | 5    | 0   | 0.688 | 448 | 326 | 122  | 7.6   | 1.5  | 9.2   | 7.0   | 2.2  | NFC South   | divwin     | 2017 | 
| Carolina Panthers        | 11  | 5    | 0   | 0.688 | 363 | 327 | 36   | 2.3   | 2.1  | 4.3   | 1.7   | 2.7  | NFC South   | wildcard   | 2017 | 
| Atlanta Falcons          | 10  | 6    | 0   | 0.625 | 353 | 315 | 38   | 2.4   | 1.9  | 4.3   | 1.1   | 3.2  | NFC South   | wildcard   | 2017 | 
| Tampa Bay Buccaneers     | 5   | 11   | 0   | 0.313 | 335 | 382 | -47  | -2.9  | 1.7  | -1.3  | 0.4   | -1.7 | NFC South   | missed     | 2017 | 
| Los Angeles Rams         | 11  | 5    | 0   | 0.688 | 478 | 329 | 149  | 9.3   | -0.2 | 9.2   | 8.2   | 1.0  | NFC West    | divwin     | 2017 | 
| Seattle Seahawks         | 9   | 7    | 0   | 0.563 | 366 | 332 | 34   | 2.1   | -0.2 | 1.9   | 0.7   | 1.2  | NFC West    | missed     | 2017 | 
| Arizona Cardinals        | 8   | 8    | 0   | 0.5   | 295 | 361 | -66  | -4.1  | 0.4  | -3.7  | -4.0  | 0.2  | NFC West    | missed     | 2017 | 
| San Francisco 49ers      | 6   | 10   | 0   | 0.375 | 331 | 383 | -52  | -3.3  | 0.4  | -2.9  | -0.8  | -2.1 | NFC West    | missed     | 2017 | 
| New England Patriots     | 11  | 5    | 0   | 0.688 | 436 | 325 | 111  | 6.9   | -1.8 | 5.2   | 3.1   | 2.1  | AFC East    | divwin     | 2018 | 
| Miami Dolphins           | 7   | 9    | 0   | 0.438 | 319 | 433 | -114 | -7.1  | -1.7 | -8.8  | -3.6  | -5.2 | AFC East    | missed     | 2018 | 
| Buffalo Bills            | 6   | 10   | 0   | 0.375 | 269 | 374 | -105 | -6.6  | -0.3 | -6.9  | -6.3  | -0.6 | AFC East    | missed     | 2018 | 
| New York Jets            | 4   | 12   | 0   | 0.25  | 333 | 441 | -108 | -6.8  | -1.1 | -7.8  | -2.0  | -5.9 | AFC East    | missed     | 2018 | 
| Baltimore Ravens         | 10  | 6    | 0   | 0.625 | 389 | 287 | 102  | 6.4   | 0.6  | 7.0   | 0.6   | 6.4  | AFC North   | divwin     | 2018 | 
| Pittsburgh Steelers      | 9   | 6    | 1   | 0.594 | 428 | 360 | 68   | 4.3   | 1.3  | 5.6   | 3.9   | 1.7  | AFC North   | missed     | 2018 | 
| Cleveland Browns         | 7   | 8    | 1   | 0.469 | 359 | 392 | -33  | -2.1  | 1.7  | -0.3  | -1.0  | 0.6  | AFC North   | missed     | 2018 | 
| Cincinnati Bengals       | 6   | 10   | 0   | 0.375 | 368 | 455 | -87  | -5.4  | 2.0  | -3.4  | 0.0   | -3.4 | AFC North   | missed     | 2018 | 
| Houston Texans           | 11  | 5    | 0   | 0.688 | 402 | 316 | 86   | 5.4   | -1.5 | 3.8   | 2.4   | 1.4  | AFC South   | divwin     | 2018 | 
| Indianapolis Colts       | 10  | 6    | 0   | 0.625 | 433 | 344 | 89   | 5.6   | -2.2 | 3.4   | 3.9   | -0.6 | AFC South   | wildcard   | 2018 | 
| Tennessee Titans         | 9   | 7    | 0   | 0.563 | 310 | 303 | 7    | 0.4   | -0.2 | 0.2   | -3.2  | 3.5  | AFC South   | missed     | 2018 | 
| Jacksonville Jaguars     | 5   | 11   | 0   | 0.313 | 245 | 316 | -71  | -4.4  | 0.4  | -4.0  | -8.1  | 4.0  | AFC South   | missed     | 2018 | 
| Kansas City Chiefs       | 12  | 4    | 0   | 0.75  | 565 | 421 | 144  | 9.0   | -0.1 | 8.9   | 12.6  | -3.8 | AFC West    | divwin     | 2018 | 
| Los Angeles Chargers     | 12  | 4    | 0   | 0.75  | 428 | 329 | 99   | 6.2   | -0.2 | 6.0   | 3.0   | 2.9  | AFC West    | wildcard   | 2018 | 
| Denver Broncos           | 6   | 10   | 0   | 0.375 | 329 | 349 | -20  | -1.3  | 0.7  | -0.5  | -3.6  | 3.1  | AFC West    | missed     | 2018 | 
| Oakland Raiders          | 4   | 12   | 0   | 0.25  | 290 | 467 | -177 | -11.1 | 1.8  | -9.3  | -5.2  | -4.1 | AFC West    | missed     | 2018 | 
| Dallas Cowboys           | 10  | 6    | 0   | 0.625 | 339 | 324 | 15   | 0.9   | 0.2  | 1.1   | -1.9  | 2.9  | NFC East    | divwin     | 2018 | 
| Philadelphia Eagles      | 9   | 7    | 0   | 0.563 | 367 | 348 | 19   | 1.2   | 0.5  | 1.7   | 0.0   | 1.8  | NFC East    | wildcard   | 2018 | 
| Washington Redskins      | 7   | 9    | 0   | 0.438 | 281 | 359 | -78  | -4.9  | -0.1 | -4.9  | -5.6  | 0.6  | NFC East    | missed     | 2018 | 
| New York Giants          | 5   | 11   | 0   | 0.313 | 369 | 412 | -43  | -2.7  | 0.5  | -2.2  | 0.8   | -2.9 | NFC East    | missed     | 2018 | 
| Chicago Bears            | 12  | 4    | 0   | 0.75  | 421 | 283 | 138  | 8.6   | -2.3 | 6.3   | 1.5   | 4.8  | NFC North   | divwin     | 2018 | 
| Minnesota Vikings        | 8   | 7    | 1   | 0.531 | 360 | 341 | 19   | 1.2   | -0.6 | 0.6   | -1.2  | 1.8  | NFC North   | missed     | 2018 | 
| Green Bay Packers        | 6   | 9    | 1   | 0.406 | 376 | 400 | -24  | -1.5  | -1.2 | -2.7  | 0.0   | -2.7 | NFC North   | missed     | 2018 | 
| Detroit Lions            | 6   | 10   | 0   | 0.375 | 324 | 360 | -36  | -2.3  | -0.8 | -3.0  | -3.3  | 0.3  | NFC North   | missed     | 2018 | 
| New Orleans Saints       | 13  | 3    | 0   | 0.813 | 504 | 353 | 151  | 9.4   | 0.6  | 10.1  | 7.9   | 2.2  | NFC South   | divwin     | 2018 | 
| Atlanta Falcons          | 7   | 9    | 0   | 0.438 | 414 | 423 | -9   | -0.6  | 0.4  | -0.1  | 2.5   | -2.6 | NFC South   | missed     | 2018 | 
| Carolina Panthers        | 7   | 9    | 0   | 0.438 | 376 | 382 | -6   | -0.4  | 1.3  | 0.9   | 0.1   | 0.8  | NFC South   | missed     | 2018 | 
| Tampa Bay Buccaneers     | 5   | 11   | 0   | 0.313 | 396 | 464 | -68  | -4.3  | 1.7  | -2.6  | 2.0   | -4.6 | NFC South   | missed     | 2018 | 
| Los Angeles Rams         | 13  | 3    | 0   | 0.813 | 527 | 384 | 143  | 8.9   | -0.4 | 8.5   | 9.5   | -1.1 | NFC West    | divwin     | 2018 | 
| Seattle Seahawks         | 10  | 6    | 0   | 0.625 | 428 | 347 | 81   | 5.1   | -0.6 | 4.5   | 3.0   | 1.5  | NFC West    | wildcard   | 2018 | 
| San Francisco 49ers      | 4   | 12   | 0   | 0.25  | 342 | 435 | -93  | -5.8  | 0.3  | -5.5  | -2.5  | -3.1 | NFC West    | missed     | 2018 | 
| Arizona Cardinals        | 3   | 13   | 0   | 0.188 | 225 | 425 | -200 | -12.5 | 1.0  | -11.5 | -9.6  | -1.9 | NFC West    | missed     | 2018 | 
| New England Patriots     | 12  | 4    | 0   | 0.75  | 420 | 225 | 195  | 12.2  | -1.8 | 10.4  | 2.8   | 7.6  | AFC East    | divwin     | 2019 | 
| Buffalo Bills            | 10  | 6    | 0   | 0.625 | 314 | 259 | 55   | 3.4   | -1.3 | 2.2   | -3.5  | 5.7  | AFC East    | wildcard   | 2019 | 
| New York Jets            | 7   | 9    | 0   | 0.438 | 276 | 359 | -83  | -5.2  | -1.1 | -6.3  | -5.7  | -0.6 | AFC East    | missed     | 2019 | 
| Miami Dolphins           | 5   | 11   | 0   | 0.313 | 306 | 494 | -188 | -11.8 | 0.2  | -11.6 | -2.4  | -9.1 | AFC East    | missed     | 2019 | 
| Baltimore Ravens         | 14  | 2    | 0   | 0.875 | 531 | 282 | 249  | 15.6  | 0.1  | 15.6  | 11.0  | 4.7  | AFC North   | divwin     | 2019 | 
| Pittsburgh Steelers      | 8   | 8    | 0   | 0.5   | 289 | 303 | -14  | -0.9  | 1.2  | 0.3   | -4.3  | 4.6  | AFC North   | missed     | 2019 | 
| Cleveland Browns         | 6   | 10   | 0   | 0.375 | 335 | 393 | -58  | -3.6  | 1.7  | -1.9  | -0.4  | -1.5 | AFC North   | missed     | 2019 | 
| Cincinnati Bengals       | 2   | 14   | 0   | 0.125 | 279 | 420 | -141 | -8.8  | 1.5  | -7.3  | -4.4  | -2.9 | AFC North   | missed     | 2019 | 
| Houston Texans           | 10  | 6    | 0   | 0.625 | 378 | 385 | -7   | -0.4  | 1.0  | 0.5   | 1.0   | -0.5 | AFC South   | divwin     | 2019 | 
| Tennessee Titans         | 9   | 7    | 0   | 0.563 | 402 | 331 | 71   | 4.4   | -1.0 | 3.4   | 1.8   | 1.7  | AFC South   | wildcard   | 2019 | 
| Indianapolis Colts       | 7   | 9    | 0   | 0.438 | 361 | 373 | -12  | -0.8  | -1.1 | -1.8  | -1.0  | -0.8 | AFC South   | missed     | 2019 | 
| Jacksonville Jaguars     | 6   | 10   | 0   | 0.375 | 300 | 397 | -97  | -6.1  | -0.6 | -6.7  | -4.6  | -2.1 | AFC South   | missed     | 2019 | 
| Kansas City Chiefs       | 12  | 4    | 0   | 0.75  | 451 | 308 | 143  | 8.9   | 0.2  | 9.1   | 6.2   | 2.9  | AFC West    | divwin     | 2019 | 
| Denver Broncos           | 7   | 9    | 0   | 0.438 | 282 | 316 | -34  | -2.1  | 0.0  | -2.1  | -4.8  | 2.7  | AFC West    | missed     | 2019 | 
| Oakland Raiders          | 7   | 9    | 0   | 0.438 | 313 | 419 | -106 | -6.6  | -0.3 | -6.9  | -2.5  | -4.4 | AFC West    | missed     | 2019 | 
| Los Angeles Chargers     | 5   | 11   | 0   | 0.313 | 337 | 345 | -8   | -0.5  | -0.8 | -1.3  | -1.6  | 0.3  | AFC West    | missed     | 2019 | 
| Philadelphia Eagles      | 9   | 7    | 0   | 0.563 | 385 | 354 | 31   | 1.9   | -1.7 | 0.3   | 0.7   | -0.4 | NFC East    | divwin     | 2019 | 
| Dallas Cowboys           | 8   | 8    | 0   | 0.5   | 434 | 321 | 113  | 7.1   | -1.8 | 5.3   | 3.8   | 1.5  | NFC East    | missed     | 2019 | 
| New York Giants          | 4   | 12   | 0   | 0.25  | 341 | 451 | -110 | -6.9  | -1.0 | -7.9  | -1.8  | -6.1 | NFC East    | missed     | 2019 | 
| Washington Redskins      | 3   | 13   | 0   | 0.188 | 266 | 435 | -169 | -10.6 | -0.2 | -10.8 | -6.3  | -4.5 | NFC East    | missed     | 2019 | 
| Green Bay Packers        | 13  | 3    | 0   | 0.813 | 376 | 313 | 63   | 3.9   | -0.7 | 3.2   | 0.6   | 2.6  | NFC North   | divwin     | 2019 | 
| Minnesota Vikings        | 10  | 6    | 0   | 0.625 | 407 | 303 | 104  | 6.5   | -1.1 | 5.4   | 2.5   | 2.9  | NFC North   | wildcard   | 2019 | 
| Chicago Bears            | 8   | 8    | 0   | 0.5   | 280 | 298 | -18  | -1.1  | 0.2  | -0.9  | -5.4  | 4.5  | NFC North   | missed     | 2019 | 
| Detroit Lions            | 3   | 12   | 1   | 0.219 | 341 | 423 | -82  | -5.1  | -0.1 | -5.2  | -1.2  | -4.0 | NFC North   | missed     | 2019 | 
| New Orleans Saints       | 13  | 3    | 0   | 0.813 | 458 | 341 | 117  | 7.3   | 0.0  | 7.4   | 5.0   | 2.3  | NFC South   | divwin     | 2019 | 
| Atlanta Falcons          | 7   | 9    | 0   | 0.438 | 381 | 399 | -18  | -1.1  | 1.1  | -0.1  | 0.3   | -0.4 | NFC South   | missed     | 2019 | 
| Tampa Bay Buccaneers     | 7   | 9    | 0   | 0.438 | 458 | 449 | 9    | 0.6   | -0.2 | 0.4   | 4.9   | -4.5 | NFC South   | missed     | 2019 | 
| Carolina Panthers        | 5   | 11   | 0   | 0.313 | 340 | 470 | -130 | -8.1  | 1.1  | -7.0  | -1.9  | -5.1 | NFC South   | missed     | 2019 | 
| San Francisco 49ers      | 13  | 3    | 0   | 0.813 | 479 | 310 | 169  | 10.6  | 0.4  | 11.0  | 6.7   | 4.3  | NFC West    | divwin     | 2019 | 
| Seattle Seahawks         | 11  | 5    | 0   | 0.688 | 405 | 398 | 7    | 0.4   | 2.3  | 2.7   | 2.9   | -0.2 | NFC West    | wildcard   | 2019 | 
| Los Angeles Rams         | 9   | 7    | 0   | 0.563 | 394 | 364 | 30   | 1.9   | 2.0  | 3.9   | 2.2   | 1.7  | NFC West    | missed     | 2019 | 
| Arizona Cardinals        | 5   | 10   | 1   | 0.344 | 361 | 442 | -81  | -5.1  | 1.8  | -3.2  | -0.3  | -2.9 | NFC West    | missed     | 2019 | 
| Buffalo Bills            | 13  | 3    | 0   | 0.813 | 501 | 375 | 126  | 7.9   | -0.2 | 7.7   | 7.1   | 0.6  | AFC East    | divwin     | 2020 | 
| Miami Dolphins           | 10  | 6    | 0   | 0.625 | 404 | 338 | 66   | 4.1   | -1.2 | 3.0   | 0.3   | 2.7  | AFC East    | missed     | 2020 | 
| New England Patriots     | 7   | 9    | 0   | 0.438 | 326 | 353 | -27  | -1.7  | 0.7  | -1.0  | -4.2  | 3.2  | AFC East    | missed     | 2020 | 
| New York Jets            | 2   | 14   | 0   | 0.125 | 243 | 457 | -214 | -13.4 | 1.9  | -11.5 | -8.7  | -2.8 | AFC East    | missed     | 2020 | 
| Pittsburgh Steelers      | 12  | 4    | 0   | 0.75  | 416 | 312 | 104  | 6.5   | -1.8 | 4.7   | 0.3   | 4.4  | AFC North   | divwin     | 2020 | 
| Baltimore Ravens         | 11  | 5    | 0   | 0.688 | 468 | 303 | 165  | 10.3  | -2.0 | 8.3   | 3.9   | 4.3  | AFC North   | wildcard   | 2020 | 
| Cleveland Browns         | 11  | 5    | 0   | 0.688 | 408 | 419 | -11  | -0.7  | -1.9 | -2.6  | 0.3   | -2.8 | AFC North   | wildcard   | 2020 | 
| Cincinnati Bengals       | 4   | 11   | 1   | 0.281 | 311 | 424 | -113 | -7.1  | -0.4 | -7.5  | -5.4  | -2.1 | AFC North   | missed     | 2020 | 
| Tennessee Titans         | 11  | 5    | 0   | 0.688 | 491 | 439 | 52   | 3.3   | -1.7 | 1.6   | 4.7   | -3.1 | AFC South   | divwin     | 2020 | 
| Indianapolis Colts       | 11  | 5    | 0   | 0.688 | 451 | 362 | 89   | 5.6   | -2.8 | 2.8   | 1.2   | 1.6  | AFC South   | wildcard   | 2020 | 
| Houston Texans           | 4   | 12   | 0   | 0.25  | 384 | 464 | -80  | -5.0  | -0.5 | -5.5  | -1.4  | -4.1 | AFC South   | missed     | 2020 | 
| Jacksonville Jaguars     | 1   | 15   | 0   | 0.063 | 306 | 492 | -186 | -11.6 | -0.1 | -11.7 | -6.5  | -5.3 | AFC South   | missed     | 2020 | 
| Kansas City Chiefs       | 14  | 2    | 0   | 0.875 | 473 | 362 | 111  | 6.9   | -0.1 | 6.8   | 4.5   | 2.3  | AFC West    | divwin     | 2020 | 
| Las Vegas Raiders        | 8   | 8    | 0   | 0.5   | 434 | 478 | -44  | -2.8  | 0.8  | -2.0  | 2.9   | -4.9 | AFC West    | missed     | 2020 | 
| Los Angeles Chargers     | 7   | 9    | 0   | 0.438 | 384 | 426 | -42  | -2.6  | -0.3 | -2.9  | -1.0  | -2.0 | AFC West    | missed     | 2020 | 
| Denver Broncos           | 5   | 11   | 0   | 0.313 | 323 | 446 | -123 | -7.7  | 1.7  | -6.0  | -4.3  | -1.7 | AFC West    | missed     | 2020 | 
| Washington Football Team | 7   | 9    | 0   | 0.438 | 335 | 329 | 6    | 0.4   | -1.2 | -0.8  | -4.1  | 3.2  | NFC East    | divwin     | 2020 | 
| New York Giants          | 6   | 10   | 0   | 0.375 | 280 | 357 | -77  | -4.8  | 0.4  | -4.4  | -6.7  | 2.3  | NFC East    | missed     | 2020 | 
| Dallas Cowboys           | 6   | 10   | 0   | 0.375 | 395 | 473 | -78  | -4.9  | -0.2 | -5.1  | 1.0   | -6.1 | NFC East    | missed     | 2020 | 
| Philadelphia Eagles      | 4   | 11   | 1   | 0.281 | 334 | 418 | -84  | -5.3  | 0.8  | -4.4  | -2.8  | -1.6 | NFC East    | missed     | 2020 | 
| Green Bay Packers        | 13  | 3    | 0   | 0.813 | 509 | 369 | 140  | 8.8   | -1.1 | 7.7   | 5.9   | 1.8  | NFC North   | divwin     | 2020 | 
| Chicago Bears            | 8   | 8    | 0   | 0.5   | 372 | 370 | 2    | 0.1   | 0.1  | 0.2   | -2.2  | 2.4  | NFC North   | wildcard   | 2020 | 
| Minnesota Vikings        | 7   | 9    | 0   | 0.438 | 430 | 475 | -45  | -2.8  | 0.4  | -2.4  | 1.3   | -3.8 | NFC North   | missed     | 2020 | 
| Detroit Lions            | 5   | 11   | 0   | 0.313 | 377 | 519 | -142 | -8.9  | 1.2  | -7.7  | -1.0  | -6.7 | NFC North   | missed     | 2020 | 
| New Orleans Saints       | 12  | 4    | 0   | 0.75  | 482 | 337 | 145  | 9.1   | 0.5  | 9.6   | 5.1   | 4.5  | NFC South   | divwin     | 2020 | 
| Tampa Bay Buccaneers     | 11  | 5    | 0   | 0.688 | 492 | 355 | 137  | 8.6   | 0.8  | 9.4   | 6.5   | 2.8  | NFC South   | wildcard   | 2020 | 
| Carolina Panthers        | 5   | 11   | 0   | 0.313 | 350 | 402 | -52  | -3.3  | 2.2  | -1.1  | -2.4  | 1.3  | NFC South   | missed     | 2020 | 
| Atlanta Falcons          | 4   | 12   | 0   | 0.25  | 396 | 414 | -18  | -1.1  | 1.9  | 0.7   | -0.1  | 0.8  | NFC South   | missed     | 2020 | 
| Seattle Seahawks         | 12  | 4    | 0   | 0.75  | 459 | 371 | 88   | 5.5   | 0.0  | 5.5   | 4.8   | 0.7  | NFC West    | divwin     | 2020 | 
| Los Angeles Rams         | 10  | 6    | 0   | 0.625 | 372 | 296 | 76   | 4.8   | 0.7  | 5.4   | -0.8  | 6.2  | NFC West    | wildcard   | 2020 | 
| Arizona Cardinals        | 8   | 8    | 0   | 0.5   | 410 | 367 | 43   | 2.7   | -0.1 | 2.6   | 1.5   | 1.0  | NFC West    | missed     | 2020 | 
| San Francisco 49ers      | 6   | 10   | 0   | 0.375 | 376 | 390 | -14  | -0.9  | 1.7  | 0.8   | 0.2   | 0.7  | NFC West    | missed     | 2020 | 
| Buffalo Bills            | 11  | 6    | 0   | 0.647 | 483 | 289 | 194  | 11.4  | -1.6 | 9.8   | 5.0   | 4.8  | AFC East    | divwin     | 2021 | 
| New England Patriots     | 10  | 7    | 0   | 0.588 | 462 | 303 | 159  | 9.4   | -0.9 | 8.5   | 3.6   | 4.8  | AFC East    | wildcard   | 2021 | 
| Miami Dolphins           | 9   | 8    | 0   | 0.529 | 341 | 373 | -32  | -1.9  | -0.8 | -2.7  | -3.1  | 0.3  | AFC East    | missed     | 2021 | 
| New York Jets            | 4   | 13   | 0   | 0.235 | 310 | 504 | -194 | -11.4 | 1.0  | -10.4 | -3.6  | -6.7 | AFC East    | missed     | 2021 | 
| Cincinnati Bengals       | 10  | 7    | 0   | 0.588 | 460 | 376 | 84   | 4.9   | -1.9 | 3.1   | 3.4   | -0.3 | AFC North   | divwin     | 2021 | 
| Pittsburgh Steelers      | 9   | 7    | 1   | 0.559 | 343 | 398 | -55  | -3.2  | 0.8  | -2.5  | -2.6  | 0.1  | AFC North   | wildcard   | 2021 | 
| Cleveland Browns         | 8   | 9    | 0   | 0.471 | 349 | 371 | -22  | -1.3  | 0.0  | -1.3  | -2.7  | 1.3  | AFC North   | missed     | 2021 | 
| Baltimore Ravens         | 8   | 9    | 0   | 0.471 | 387 | 392 | -5   | -0.3  | 0.0  | -0.3  | -0.3  | 0.0  | AFC North   | missed     | 2021 | 
| Tennessee Titans         | 12  | 5    | 0   | 0.706 | 419 | 354 | 65   | 3.8   | -0.4 | 3.4   | 1.8   | 1.6  | AFC South   | divwin     | 2021 | 
| Indianapolis Colts       | 9   | 8    | 0   | 0.529 | 451 | 365 | 86   | 5.1   | -0.6 | 4.4   | 3.3   | 1.1  | AFC South   | missed     | 2021 | 
| Houston Texans           | 4   | 13   | 0   | 0.235 | 280 | 452 | -172 | -10.1 | 0.4  | -9.7  | -6.3  | -3.4 | AFC South   | missed     | 2021 | 
| Jacksonville Jaguars     | 3   | 14   | 0   | 0.176 | 253 | 457 | -204 | -12.0 | 0.6  | -11.4 | -7.7  | -3.7 | AFC South   | missed     | 2021 | 
| Kansas City Chiefs       | 12  | 5    | 0   | 0.706 | 480 | 364 | 116  | 6.8   | 0.6  | 7.4   | 5.4   | 2.0  | AFC West    | divwin     | 2021 | 
| Las Vegas Raiders        | 10  | 7    | 0   | 0.588 | 374 | 439 | -65  | -3.8  | 0.6  | -3.3  | -0.7  | -2.6 | AFC West    | wildcard   | 2021 | 
| Los Angeles Chargers     | 9   | 8    | 0   | 0.529 | 474 | 459 | 15   | 0.9   | 0.2  | 1.1   | 5.3   | -4.2 | AFC West    | missed     | 2021 | 
| Denver Broncos           | 7   | 10   | 0   | 0.412 | 335 | 322 | 13   | 0.8   | -1.3 | -0.5  | -4.7  | 4.2  | AFC West    | missed     | 2021 | 
| Dallas Cowboys           | 12  | 5    | 0   | 0.706 | 530 | 358 | 172  | 10.1  | -0.2 | 9.9   | 8.2   | 1.7  | NFC East    | divwin     | 2021 | 
| Philadelphia Eagles      | 9   | 8    | 0   | 0.529 | 444 | 385 | 59   | 3.5   | -1.0 | 2.5   | 2.6   | -0.1 | NFC East    | wildcard   | 2021 | 
| Washington Football Team | 7   | 10   | 0   | 0.412 | 335 | 434 | -99  | -5.8  | 1.6  | -4.2  | -2.7  | -1.5 | NFC East    | missed     | 2021 | 
| New York Giants          | 4   | 13   | 0   | 0.235 | 258 | 416 | -158 | -9.3  | 1.0  | -8.3  | -7.7  | -0.6 | NFC East    | missed     | 2021 | 
| Green Bay Packers        | 13  | 4    | 0   | 0.765 | 450 | 371 | 79   | 4.6   | -0.2 | 4.4   | 3.5   | 1.0  | NFC North   | divwin     | 2021 | 
| Minnesota Vikings        | 8   | 9    | 0   | 0.471 | 425 | 426 | -1   | -0.1  | 0.3  | 0.3   | 1.9   | -1.6 | NFC North   | missed     | 2021 | 
| Chicago Bears            | 6   | 11   | 0   | 0.353 | 311 | 407 | -96  | -5.6  | 0.5  | -5.2  | -4.9  | -0.3 | NFC North   | missed     | 2021 | 
| Detroit Lions            | 3   | 13   | 1   | 0.206 | 325 | 467 | -142 | -8.4  | 0.6  | -7.8  | -3.5  | -4.3 | NFC North   | missed     | 2021 | 
| Tampa Bay Buccaneers     | 13  | 4    | 0   | 0.765 | 511 | 353 | 158  | 9.3   | -0.7 | 8.6   | 7.3   | 1.3  | NFC South   | divwin     | 2021 | 
| New Orleans Saints       | 9   | 8    | 0   | 0.529 | 364 | 335 | 29   | 1.7   | 0.3  | 2.0   | -1.5  | 3.6  | NFC South   | missed     | 2021 | 
| Atlanta Falcons          | 7   | 10   | 0   | 0.412 | 313 | 459 | -146 | -8.6  | 0.1  | -8.5  | -4.2  | -4.3 | NFC South   | missed     | 2021 | 
| Carolina Panthers        | 5   | 12   | 0   | 0.294 | 304 | 404 | -100 | -5.9  | 0.4  | -5.5  | -5.0  | -0.5 | NFC South   | missed     | 2021 | 
| Los Angeles Rams         | 12  | 5    | 0   | 0.706 | 460 | 372 | 88   | 5.2   | 0.1  | 5.3   | 4.2   | 1.1  | NFC West    | divwin     | 2021 | 
| Arizona Cardinals        | 11  | 6    | 0   | 0.647 | 449 | 366 | 83   | 4.9   | 0.3  | 5.2   | 3.6   | 1.6  | NFC West    | wildcard   | 2021 | 
| San Francisco 49ers      | 10  | 7    | 0   | 0.588 | 427 | 365 | 62   | 3.6   | 0.1  | 3.8   | 1.8   | 1.9  | NFC West    | wildcard   | 2021 | 
| Seattle Seahawks         | 7   | 10   | 0   | 0.412 | 395 | 366 | 29   | 1.7   | 0.2  | 1.9   | 0.4   | 1.5  | NFC West    | missed     | 2021 | 
| Buffalo Bills            | 13  | 3    | 0   | 0.813 | 455 | 286 | 169  | 10.6  | 0.4  | 10.9  | 7.1   | 3.8  | AFC East    | divwin     | 2022 | 
| Miami Dolphins           | 9   | 8    | 0   | 0.529 | 397 | 399 | -2   | -0.1  | 2.0  | 1.8   | 2.7   | -0.9 | AFC East    | wildcard   | 2022 | 
| New England Patriots     | 8   | 9    | 0   | 0.471 | 364 | 347 | 17   | 1.0   | 1.0  | 2.0   | -0.3  | 2.3  | AFC East    | missed     | 2022 | 
| New York Jets            | 7   | 10   | 0   | 0.412 | 296 | 316 | -20  | -1.2  | 2.0  | 0.8   | -4.0  | 4.8  | AFC East    | missed     | 2022 | 
| Cincinnati Bengals       | 12  | 4    | 0   | 0.75  | 418 | 322 | 96   | 6.0   | 0.9  | 6.9   | 5.5   | 1.4  | AFC North   | divwin     | 2022 | 
| Baltimore Ravens         | 10  | 7    | 0   | 0.588 | 350 | 315 | 35   | 2.1   | 1.1  | 3.1   | -0.2  | 3.4  | AFC North   | wildcard   | 2022 | 
| Pittsburgh Steelers      | 9   | 8    | 0   | 0.529 | 308 | 346 | -38  | -2.2  | 1.5  | -0.8  | -3.0  | 2.3  | AFC North   | missed     | 2022 | 
| Cleveland Browns         | 7   | 10   | 0   | 0.412 | 361 | 381 | -20  | -1.2  | 1.1  | -0.1  | 0.7   | -0.9 | AFC North   | missed     | 2022 | 
| Jacksonville Jaguars     | 9   | 8    | 0   | 0.529 | 404 | 350 | 54   | 3.2   | -1.4 | 1.8   | 1.6   | 0.2  | AFC South   | divwin     | 2022 | 
| Tennessee Titans         | 7   | 10   | 0   | 0.412 | 298 | 359 | -61  | -3.6  | 0.0  | -3.6  | -4.7  | 1.1  | AFC South   | missed     | 2022 | 
| Indianapolis Colts       | 4   | 12   | 1   | 0.265 | 289 | 427 | -138 | -8.1  | -0.5 | -8.6  | -4.9  | -3.7 | AFC South   | missed     | 2022 | 
| Houston Texans           | 3   | 13   | 1   | 0.206 | 289 | 420 | -131 | -7.7  | -0.8 | -8.5  | -5.4  | -3.1 | AFC South   | missed     | 2022 | 
| Kansas City Chiefs       | 14  | 3    | 0   | 0.824 | 496 | 369 | 127  | 7.5   | -1.2 | 6.2   | 6.8   | -0.6 | AFC West    | divwin     | 2022 | 
| Los Angeles Chargers     | 10  | 7    | 0   | 0.588 | 391 | 384 | 7    | 0.4   | -1.3 | -0.9  | 0.1   | -1.0 | AFC West    | wildcard   | 2022 | 
| Las Vegas Raiders        | 6   | 11   | 0   | 0.353 | 395 | 418 | -23  | -1.4  | -1.1 | -2.5  | 1.2   | -3.7 | AFC West    | missed     | 2022 | 
| Denver Broncos           | 5   | 12   | 0   | 0.294 | 287 | 359 | -72  | -4.2  | -0.7 | -5.0  | -5.6  | 0.6  | AFC West    | missed     | 2022 | 
| Philadelphia Eagles      | 14  | 3    | 0   | 0.824 | 477 | 344 | 133  | 7.8   | -1.3 | 6.5   | 5.8   | 0.7  | NFC East    | divwin     | 2022 | 
| Dallas Cowboys           | 12  | 5    | 0   | 0.706 | 467 | 342 | 125  | 7.4   | -0.8 | 6.5   | 5.3   | 1.3  | NFC East    | wildcard   | 2022 | 
| New York Giants          | 9   | 7    | 1   | 0.559 | 365 | 371 | -6   | -0.4  | 0.0  | -0.4  | -0.8  | 0.4  | NFC East    | wildcard   | 2022 | 
| Washington Commanders    | 8   | 8    | 1   | 0.5   | 321 | 343 | -22  | -1.3  | 0.4  | -0.9  | -3.5  | 2.6  | NFC East    | missed     | 2022 | 
| Minnesota Vikings        | 13  | 4    | 0   | 0.765 | 424 | 427 | -3   | -0.2  | 0.1  | -0.1  | 2.8   | -2.9 | NFC North   | divwin     | 2022 | 
| Detroit Lions            | 9   | 8    | 0   | 0.529 | 453 | 427 | 26   | 1.5   | 0.7  | 2.2   | 4.7   | -2.4 | NFC North   | missed     | 2022 | 
| Green Bay Packers        | 8   | 9    | 0   | 0.471 | 370 | 371 | -1   | -0.1  | 0.4  | 0.3   | -0.3  | 0.6  | NFC North   | missed     | 2022 | 
| Chicago Bears            | 3   | 14   | 0   | 0.176 | 326 | 463 | -137 | -8.1  | 1.6  | -6.4  | -2.5  | -4.0 | NFC North   | missed     | 2022 | 
| Tampa Bay Buccaneers     | 8   | 9    | 0   | 0.471 | 313 | 358 | -45  | -2.6  | 0.4  | -2.3  | -3.3  | 1.1  | NFC South   | divwin     | 2022 | 
| Carolina Panthers        | 7   | 10   | 0   | 0.412 | 347 | 374 | -27  | -1.6  | -0.6 | -2.2  | -1.3  | -0.9 | NFC South   | missed     | 2022 | 
| New Orleans Saints       | 7   | 10   | 0   | 0.412 | 330 | 345 | -15  | -0.9  | -0.3 | -1.2  | -2.8  | 1.7  | NFC South   | missed     | 2022 | 
| Atlanta Falcons          | 7   | 10   | 0   | 0.412 | 365 | 386 | -21  | -1.2  | -0.9 | -2.1  | -0.1  | -2.0 | NFC South   | missed     | 2022 | 
| San Francisco 49ers      | 13  | 4    | 0   | 0.765 | 450 | 277 | 173  | 10.2  | -2.3 | 7.9   | 3.3   | 4.6  | NFC West    | divwin     | 2022 | 
| Seattle Seahawks         | 9   | 8    | 0   | 0.529 | 407 | 401 | 6    | 0.4   | -0.8 | -0.5  | 1.9   | -2.4 | NFC West    | wildcard   | 2022 | 
| Los Angeles Rams         | 5   | 12   | 0   | 0.294 | 307 | 384 | -77  | -4.5  | 0.5  | -4.0  | -4.1  | 0.0  | NFC West    | missed     | 2022 | 
| Arizona Cardinals        | 4   | 13   | 0   | 0.235 | 340 | 449 | -109 | -6.4  | 0.2  | -6.2  | -1.9  | -4.3 | NFC West    | missed     | 2022 | 

</details>

