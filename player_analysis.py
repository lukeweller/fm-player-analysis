#!/usr/bin/env python3
import sys, time
import pandas as pd
# import matplotlib.pyplot as plt

# Input file should be stored in ./input/ as 'players_all.rtf'
INPUT_FILENAME = './input/player_search.rtf'

TECHNICAL_ATTRIBUTES = ['Cor', 'Cro', 'Dri', 'Fin', 'Fir', 'Fre', 'Hea', 'Lon', 'L Th', 'Mar', 'Pas', 'Pen', 'Tck', 'Tec']
MENTAL_ATTRIBUTES 	 = ['Agg', 'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec', 'Det', 'Fla', 'Ldr', 'OtB', 'Pos', 'Tea', 'Vis', 'Wor']
PHYSICAL_ATTRIBUTES  = ['Acc', 'Agi', 'Bal', 'Jum', 'Nat', 'Pac', 'Sta', 'Str']
GK_ATTRIBUTES 		 = ['Aer', 'Cmd', 'Com', 'Ecc', 'Han', 'Kic', '1v1', 'Pun', 'Ref', 'TRO', 'Thr']
ALL_ATTRIBUTES		 = TECHNICAL_ATTRIBUTES + MENTAL_ATTRIBUTES + PHYSICAL_ATTRIBUTES + GK_ATTRIBUTES

# Helper function for skiprows parameter in pandas.read_csv()
# Returns True for all lines numbers to read & returns False for all line numbers to skip
def skip_rows(x):
	if x < 9:
		return False
	if x % 2 == 0:
		return False
	else:
		return True

def load_all_players(input_filename):

	load_rtf_start_time = time.time()

	try:
		df = pd.read_csv(input_filename, sep = '|', skiprows=lambda x: skip_rows(x), skipinitialspace=True)

		print('time to load rtf into dataframe: {:.3f}s'.format(time.time() - load_rtf_start_time))
	
	except:
		print('error: failed to load input file \'./{}\' into the df'.format(INPUT_FILENAME))
		
		sys.exit(1)

	return df

def preprocessing(df, cache_filename):

	preprocessing_start_time = time.time()

	# In its current state, read_csv() includes two extra, unnamed columns
	# before and after all of the real columns (i.e., at index 0 & -1)
	df = df.iloc[:, 1:-1]

	# Removes whitespace from column headers
	df = df.rename(columns=lambda x: x.strip())

	# Removes whitespace from body (all values)
	df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

	# FM uses the abbreviation 'Nat' for both 'Nationality' and 'Natural Fitness'
	# If both features appear in the same input, read_csv() will create two columns with the column name 'Nat'
	# Duplicate column names will cause signifcant problems during later data analysis
	# To solve this, we'll rename the first 'Nat' column to 'Nationality'
	# The remaining, single 'Nat' column should now correspond only to 'Natural Fitness'
	found_nationality = False
	new_cols = []

	if len(df.columns) != len(set(df.columns)):
		for col in df.columns:
			if col == 'Nat' and found_nationality == False:
					new_cols.append('Nationality')
					found_nationality = True
			else:
				new_cols.append(col)

	df.columns = new_cols

	# Here we replace any missing values ('-') in the df with '0':
	# 	1. Non-GK players have a value of '-' for all GK-related attributes, while
	# 	   GKs have a value of '-' for all technical attributes. Replacing that '-' value w/
	# 	   zero is necessary for future arithmetic operations on those columns
	# 	2. It's also possible for incompletely scouted players to have '-' for any attribute
	df[ALL_ATTRIBUTES] = df[ALL_ATTRIBUTES].replace('-', '0')

	# Check if any of the scouting of any inputted players is incomplete
	# (i.e., attributes represented as a range, and not a single value)
	# Incomplete can occur iff a player's knowledge level is <= 76%
	if min(int(knowledge_lvl[:-1]) for knowledge_lvl in df['Know. Lvl']) <= 76:
		# If attribute ranges are found, we use clean_incomplete_scouting to replace those
		# those ranges w/ a single, mean value
		df = clean_incomplete_scouting(df)

	for attribute in ALL_ATTRIBUTES:
		df[attribute] = pd.to_numeric(df[attribute])

	print('preprocessing time: {:.3f}s'.format(time.time() - preprocessing_start_time))

	return df

def clean_incomplete_scouting(df):

	clean_incomplete_scouting_start_time = time.time()

	for index, row in df.iterrows():
		# If Know. Lvl <= 75% for a given player, some attributes may be represented 
		# as a range instead of a single value (e.g. Pac: 10-15). In order to perform
		# future arithmetic operations on these columns, we'll need to convert those 
		# ranges into a single, mean value (rounding down)
		if int(row['Know. Lvl'][:-1]) <= 76:
			for attribute in ALL_ATTRIBUTES:
				if not row[attribute].isdigit() and len(row[attribute].split('-')) == 2:
					range_mean = int(sum(int(_) for _ in row[attribute].split('-')) / 2)
					df.at[index, attribute] = range_mean

	print('time to clean incomplete scouting: {:.3f}s'.format(time.time() - clean_incomplete_scouting_start_time))

	return df

def player_analyis(df):

	df['technical_sum'] = sum(df[attribute] for attribute in TECHNICAL_ATTRIBUTES)
	df['mental_sum'] 	= sum(df[attribute] for attribute in MENTAL_ATTRIBUTES)
	df['physical_sum'] 	= sum(df[attribute] for attribute in PHYSICAL_ATTRIBUTES)
	df['gk_sum']		= sum(df[attribute] for attribute in GK_ATTRIBUTES)
	df['attribute_sum'] = sum(df[_] for _ in ['technical_sum', 'mental_sum', 'physical_sum', 'gk_sum'])

	df['technical_score'] = df['technical_sum'] / (len(TECHNICAL_ATTRIBUTES) * 20)
	df['mental_score']	  = df['mental_sum'] / (len(MENTAL_ATTRIBUTES) * 20)
	df['physical_score']  = df['physical_sum'] / (len(PHYSICAL_ATTRIBUTES) * 20)
	df['gk_score']		  = df['gk_sum'] / (len(GK_ATTRIBUTES) * 20)
	df['attribute_score'] = df['attribute_sum'] / (len(ALL_ATTRIBUTES) * 20)

	df = relative_score(df)

	df = df.sort_values(by='relative_score', ascending=False)

	return df

# Scales the attribute_sum from 0 to 100 (range_min to range_max), w/
# 100.0 representing the player w/ the highest attribute sum and 0.00 
# representing the player w/ the loweset total attribute sum
# Derived from SO solution here: https://stats.stackexchange.com/a/281165
def relative_score(df, range_min=0, range_max=100):
	
	min_attribute_sum = min(df['attribute_sum'])
	max_attribute_sum = max(df['attribute_sum'])

	df['relative_score'] = (range_max - range_min) * ((df['attribute_sum'] - min_attribute_sum) / (max_attribute_sum - min_attribute_sum)) + range_min

	return df

def print_help_msg():
	
	print('Usage:\n'
		  '	1. Import custom view file (`./views/Player Search.fmf`) into the \'Player Search\' page while in FM\n'
		  '	2. Copy all view data (ctrl-A, ctrl-P) and save data as a text file to `./input/player_search.rtf`\n'
		  '	3. Use `./player_analysis.py` to analyze players and print top canidates\n'
		  'Options:\n'
		  '	-i, --input\n'
		  '		specify the name of the input file; e.g., ./player_analysis.py -i [filename]\n'
		  ' -c, --cache\n'
		  '		save the cleaned dataframe into a new file in order to limit processing time on future runs;\n'
		  '		e.g., ./player_analysis -c [filename]\n'
		  '	-h, --help\n'
		  '		print this message')

if __name__ == '__main__':

	args = sys.argv[1:]

	input_filename = ''
	cache_filename = ''

	# Iterate through args
	while len(args) > 0:
		arg = args.pop(0)
		if arg == '-h' or arg == '--help':
			print_help_msg()
			exit(0)
		elif arg == '-i' or arg == '--input':
			input_filename = args.pop(0)
		elif arg == '-c' or arg == '--cache':
			cache_filename = args.pop(0)
		else:
			print('error: failed to recognize argument \'{}\' while parsing command-line arguments'.format(arg))
			exit(1)

	if input_filename == '':
		input_filename = INPUT_FILENAME

	df = load_all_players(input_filename)

	df = preprocessing(df, cache_filename)

	df = player_analyis(df)

	print(df[['relative_score', 'Age', 'Name']].head(50))
