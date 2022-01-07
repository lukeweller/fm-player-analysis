#!/usr/bin/env python3
import io, sys, time
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

def load_all_players():

	load_rtf_start_time = time.time()

	try:
		# index_col remove
		df = pd.read_csv(INPUT_FILENAME, sep = '|', skiprows=lambda x: skip_rows(x))
		
		# In its current state, read_csv() includes an extra column with label ' ' and NaN for all values
		df.drop([' '], axis=1)

		print('time to load rtf into dataframe: {:.3f}s'.format(time.time() - load_rtf_start_time))
	
	except:
		print('Error: failed to load input file \'./{}\' into the df'.format(INPUT_FILENAME))
		
		sys.exit(1)

	print(df[0])

	return df

def preprocessing(df):

	preprocessing_start_time = time.time()

	print('here 0')

	print(df.columns)

	# Non-GK players have a value of '-' for all GK-related attributes, while
	# GKs have a value of '-' for all technical attributes. Replacing that '-' value w/
	# zero is necessary for future arithmetic operations on those columns
	df[GK_ATTRIBUTES + TECHNICAL_ATTRIBUTES] = df[GK_ATTRIBUTES + TECHNICAL_ATTRIBUTES].replace('-', '0')

	print('making it here')

	# Check if any of the scouting of any inputted players is incomplete
	# (i.e., attributes represented as a range, and not a single value)
	if min(int(knowledge_lvl[:-1]) for knowledge_lvl in df['Know. Lvl']) <= 75:
		df = clean_incomplete_scouting(df)

	for attribute in ALL_ATTRIBUTES:
		df[attribute] = pd.to_numeric(df[attribute])

	print('time to load rtf into dataframe: {:.2f}s'.format(time.time() - load_rtf_start_time))

	return df

def clean_incomplete_scouting(df):

	clean_incomplete_scouting_start_time = time.time()

	for index, row in df.iterrows():
		# If Know. Lvl <= 75% for a given player, some attributes may be represented 
		# as a range instead of a single value (e.g. Pac: 10-15). In order to perform
		# future arithmetic operations on these columns, we'll need to convert those 
		# ranges into a single, mean value (rounding down)
		if int(row['Know. Lvl'][:-1]) <= 75:
			for attribute in ALL_ATTRIBUTES:
				if not row[attribute].isdigit() and len(row[attribute].split('-')) == 2:
					print(row[attribute])
					range_mean = int(sum(int(_) for _ in row[attribute].split('-')) / 2)
					df.at[index, attribute] = range_mean
					print(range_mean)

	print('time to load rtf into dataframe: {:.2f}s'.format(time.time() - load_rtf_start_time))

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
		  '	1. Import custom view file (`./views/All.fmf`) into the \'Staff Search\' page while in FM\n'
		  '	2. Copy all view data (ctrl-A, ctrl-P) and save data as a text file to `./input/All.rtf`\n'
		  '	3. Use `./player_analysis.py` to analyze players and print top canidates\n'
		  'Options:\n'
		  '	-i, --input\n'
		  '		specify the name of the input file; e.g., ./player_analysis.py -i [filename]\n'
		  '	-h, --help\n'
		  '		print this message')

if __name__ == '__main__':

	df = load_all_players()

	df = preprocessing(df)

	df = player_analyis(df)

	print(df[['technical_sum', 'mental_sum', 'physical_sum', 'relative_score', 'Age', 'Name']].head(50))
