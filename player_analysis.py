#!/usr/bin/env python3
import io, sys
import pandas as pd
# import matplotlib.pyplot as plt

# Input file should be stored in ./input/ as 'players_all.rtf'
INPUT_FILENAME = './input/player_search.rtf'

TECHNICAL_ATTRIBUTES = ['Cor', 'Cro', 'Dri', 'Fin', 'Fir', 'Fre', 'Hea', 'Lon', 'L Th', 'Mar', 'Pas', 'Pen', 'Tck', 'Tec']
MENTAL_ATTRIBUTES 	 = ['Agg', 'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec', 'Det', 'Fla', 'Ldr', 'OtB', 'Pos', 'Tea', 'Vis', 'Wor']
PHYSICAL_ATTRIBUTES  = ['Acc', 'Agi', 'Bal', 'Jum', 'Nat', 'Pac', 'Sta', 'Str']
GK_ATTRIBUTES 		 = ['Aer', 'Cmd', 'Com', 'Ecc', 'Han', 'Kic', '1v1', 'Pun', 'Ref', 'TRO', 'Thr']
ALL_ATTRIBUTES		 = TECHNICAL_ATTRIBUTES + MENTAL_ATTRIBUTES + PHYSICAL_ATTRIBUTES + GK_ATTRIBUTES

def load_all_players():

	try:
		with open(INPUT_FILENAME) as input_file:
			raw_input = input_file.read()
	except:
		print('Error: failed to open input file: \'./{}\''.format(INPUT_FILENAME))
		sys.exit(1)

	input_string = ''

	# Converts FM's custom .rtf formatting into string of comma-separated-values so that we
	# can use pandas.read_csv() to do all the work for us
	for line in raw_input.split('\n'):
		# FM uses the opening and closing tags of |c:disabled| and |/c| to designate
		# italics when exporting to the .rtf format
		# In order to properly split the line based on the '|' character, those tags must be cleaned
		line = line.replace('|c:disabled|', '').replace('|/c|','')
		line_object = [item.strip() for item in line.split('|')[1:-1]]

		if len(line_object) <= 1:
			# Empty or dashed-only line
			continue
		else:
			for item in line_object:
				# .replace(',', '') removes commas from certain features (e.g. salary, secondary positions)
				# without this cleaning, read_csv can't properly read our input string
				input_string += item.replace(',', '') + ','
			# Cleans up extra comma left at the end of rows
			input_string = input_string[:-1]
			input_string += '\n'

	# Cleans up extra newline char left at the end of input string
	input_string = input_string[:-1]

	# io.StringIO() allows pandas.read_csv() to read the string input as though
	# it were a filestream
	return pd.read_csv(io.StringIO(input_string))

def preprocessing(df):

	# Non-GK players have a value of '-' for all GK-related attributes, while
	# GKs have a value of '-' for all technical attributes. Replacing that '-' value w/
	# zero is necessary for future arithmetic operations on those columns
	df[GK_ATTRIBUTES + TECHNICAL_ATTRIBUTES] = df[GK_ATTRIBUTES + TECHNICAL_ATTRIBUTES].replace('-', '0')

	# Check if any of the scouting of any inputted players is incomplete
	# (i.e., attributes represented as a range, and not a single value)
	if min(int(knowledge_lvl[:-1]) for knowledge_lvl in df['Know. Lvl']) <= 75:
		df = clean_incomplete_scouting(df)

	for attribute in ALL_ATTRIBUTES:
		df[attribute] = pd.to_numeric(df[attribute])

	return df

def clean_incomplete_scouting(df):

	for index, row in df.iterrows():
		# If Know. Lvl <= 75% for a given player, some attributes may be represented 
		# as a range instead of a single value (e.g. Pac: 10-15). In order to perform
		# future arithmetic operations on these columns, we'll need to convert those 
		# ranges into a single, mean value (rounding down)
		if int(row['Know. Lvl'][:-1]) <= 75:
			for attribute in ALL_ATTRIBUTES:
				if not row[attribute].isdigit() and len(row[attribute].split('-')) == 2:
					range_mean = int(sum(int(_) for _ in row[attribute].split('-')) / 2)
					df.at[index, attribute] = range_mean

	# 	for attribute in ALL_ATTRIBUTES:
	# 		# For GKs, all technical skills are respresented as a '-'
	# 		# For Outfield players, all GK skills are represented as a '-'
	# 		# For later mathematical operations, we want to replace this '-' with a 0
	# 		if row[attribute] == '-':
	# 			print('Changing attribute to 0')
	# 			row[attribute] = 0
	# 		# If scouting on the player is incomplete, the attribute is given as a range (e.g. 7-13)
	# 		# For later mathematical operations, we want to replace this range with a single value
	# 		elif '-' in row[attribute]:
	# 			attribute_range = [int(_) for _ in row[attribute].split('-')]
	# 			row[attribute] = sum(attribute_range)/len(attribute_range)

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
