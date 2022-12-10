#!/usr/bin/env python3
import os, sys, time
import pandas as pd
# import matplotlib.pyplot as plt
import roles as player_roles

DEFAULT_INPUT_FILENAME = './input/rtf/player_search.rtf'
DEFAULT_PRINT_NO = 50
DEFAULT_SORT_BY = 'attribute_sum'

TECHNICAL_ATTRIBUTES = ['Cor', 'Cro', 'Dri', 'Fin', 'Fir', 'Fre', 'Hea', 'Lon', 'L Th', 'Mar', 'Pas', 'Pen', 'Tck', 'Tec']
MENTAL_ATTRIBUTES 	 = ['Agg', 'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec', 'Det', 'Fla', 'Ldr', 'OtB', 'Pos', 'Tea', 'Vis', 'Wor']
PHYSICAL_ATTRIBUTES  = ['Acc', 'Agi', 'Bal', 'Jum', 'Nat', 'Pac', 'Sta', 'Str']
GK_ATTRIBUTES 		 = ['Aer', 'Cmd', 'Com', 'Ecc', 'Han', 'Kic', '1v1', 'Pun', 'Ref', 'TRO', 'Thr']
ALL_ATTRIBUTES		 = TECHNICAL_ATTRIBUTES + MENTAL_ATTRIBUTES + PHYSICAL_ATTRIBUTES + GK_ATTRIBUTES

# Helper function for skiprows parameter in pandas.read_csv()
# Returns True for all lines numbers to read & returns False for all line numbers to skip
def skip_rows(x):
	if x < 9 or x % 2 == 0:
		return False
	else:
		return True

# Simple wrapper function that calls load_all_players_rtf() or load_all_players_csv(), depending on state
def load_players(input_filename, caching, new_input):

	cache_filename = './input/csv/' + input_filename.split('/')[-1][:-4] + '_cleaned.csv'

	if caching and os.path.exists(cache_filename) and new_input == False:
		df = load_players_csv(cache_filename)
	else:
		df = load_players_rtf(input_filename)
		df = preprocessing(df)
		if caching:
			write_df_to_csv(df, cache_filename)

	return df

def load_players_rtf(input_filename):

	load_rtf_start_time = time.time()

	try:
		df = pd.read_csv(input_filename, sep = '|', skiprows=lambda x: skip_rows(x), skipinitialspace=True)

		print('time to load \'{}\' into dataframe: {:.3f}s'.format(input_filename, time.time() - load_rtf_start_time))
	
	except:
		print('error: failed to load input file \'{}\' into the df'.format(INPUT_FILENAME))
		
		sys.exit(1)

	return df

def load_players_csv(input_filename):

	load_csv_start_time = time.time()

	try:
		df = pd.read_csv(input_filename)

		print('time to load \'{}\' into dataframe: {:.3f}s'.format(input_filename, time.time() - load_csv_start_time))
	
	except:
		print('error: failed to load input file \'./{}\' into the df'.format(input_filename))
		
		sys.exit(1)

	return df

def preprocessing(df):

	preprocessing_start_time = time.time()

	# In its current state, read_csv() includes two extra, unnamed columns
	# before and after all of the real columns (i.e., at index 0 & -1)
	df = df.iloc[:, 1:-1]

	# Removes whitespace from column headers
	df = df.rename(columns=lambda x: x.strip())

	# Removes whitespace from body (all values)
	df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

	# FM uses the abbreviation 'Nat' for both 'Nationality' and 'Natural Fitness'
	# In its current state, read_csv() behaves differently based on the view used to create the input
	# 	- for './views/Player Search.fmf':
	# 		If both features appear in the same input, read_csv() will create two columns with the column name 'Nat'
	# 		Duplicate column names will cause signifcant problems during later data analysis
	# 		To solve this, we'll rename the first 'Nat' column to 'Nationality'
	# 		The remaining, single 'Nat' column should now correspond only to 'Natural Fitness'
	if len(df.columns) != len(set(df.columns)):
		found_nationality = False
		new_cols = []
		
		for col in df.columns:
			if col == 'Nat' and found_nationality == False:
					new_cols.append('Nationality')
					found_nationality = True
			else:
				new_cols.append(col)

		df.columns = new_cols
	# 	- for './view/Squad.fmf':
	# 		If both features appear in the same input, read_csv() will auto-rename the second 'Nat' in df.columns to 'Nat .1'
	#		Since 'Natural Fitness' should come after 'Nationality', we end up with 'Nat' == Nationality and 'Nat .1' == Natural Fitness
	#		NOTE: Bc/ of this assumption, 'Natural Fitness' must(!) come after 'Nationality' in the input
	else:
		read_csv_recognized_duplicate = False
		
		for col in df.columns:
			if col + ' .1' in df.columns:
				read_csv_recognized_duplicate = True

		if read_csv_recognized_duplicate:	
			new_cols = []
		
			for col in df.columns:
				if col == 'Nat':
					new_cols.append('Nationality')
				elif col == 'Nat .1':
					new_cols.append('Nat')
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

	print('total preprocessing time: {:.3f}s'.format(time.time() - preprocessing_start_time))

	return df

def clean_incomplete_scouting(df):

	clean_incomplete_scouting_start_time = time.time()

	for index, row in df.iterrows():
		# If Know. Lvl <= 75% for a given player, some attributes may be represented 
		# as a range instead of a single value (e.g. Pac: 10-15). In order to perform
		# future arithmetic operations on these columns, we'll need to convert those 
		# ranges into a single, mean value (rounding down)
		if int(row['Know. Lvl'][:-1]) <= 77:
			for attribute in ALL_ATTRIBUTES:
				if not row[attribute].isdigit() and len(row[attribute].split('-')) == 2:
					range_mean = int(sum(int(_) for _ in row[attribute].split('-')) / 2)
					df.at[index, attribute] = range_mean

	print('time to clean incomplete scouting: {:.3f}s'.format(time.time() - clean_incomplete_scouting_start_time))

	return df

def write_df_to_csv(df, cache_filename):

	write_df_to_csv_start_time = time.time()

	df.to_csv(cache_filename, index=False)

	print('time to write cleaned data to file: {:.3f}s'.format(time.time() - write_df_to_csv_start_time))

def player_analyis(df, sort_by):

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
	df = set_pieces(df)
	df = total_cost(df)
	df = attributes_per_dollar(df)
	df = role_scores(df)

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

def set_pieces(df):

	df['set_pieces'] = 2 * df['Cor'] + 2 * df['Fre'] + df['Cro'] + df['Tec'] + df['Fla'] + df['Vis']

	return df

def convert_multipliers(value):
	# No multiplier found, strip '$' and return value as a float
	if value[-1].isdigit():
		return float(value[1:].replace(',',''))

	else:
		base = float(value[1:-1].replace(',',''))
		multiplier = value[-1]

		if multiplier == 'M':
			return base * 1000000
		elif multiplier == 'K':
			return base * 10000
		else:
			print('error: unable to parse multiplier in value: {}'.format(value))
			exit(1)

# Helper function for lambda function in total_cost()
def total_cost_helper(transfer_value, min_wage_demands, max_wage_demands):
	# Transfer value is 'Not for Sale' or 'Unknown'
	if transfer_value == 'Not for Sale' or transfer_value == 'Unknown':
		return 'N/A'

	# Transfer value listed as a range
	elif '-' in transfer_value:
		min_transfer_value = convert_multipliers(transfer_value.split('-')[0].strip())
		max_transfer_value = convert_multipliers(transfer_value.split('-')[1].strip())

		transfer_value = (min_transfer_value + max_transfer_value) / 2

	# Transfer value is single number
	else:
		transfer_value = convert_multipliers(transfer_value)

	# Player is not interested in signing
	if min_wage_demands == 'N/A' and max_wage_demands == 'N/A':
		return 'N/A'

	else:
		min_wage_demands = convert_multipliers(min_wage_demands.split(' ')[0])
		max_wage_demands = convert_multipliers(max_wage_demands.split(' ')[0])

		wage_demands = (min_wage_demands + max_wage_demands) / 2
		# Total cost of wages for 5-year contract
		total_wage_cost = wage_demands * 52 * 5

	return "${:,}M".format((transfer_value + total_wage_cost) / 1000000)

def total_cost(df):

	df['total_cost'] = df.apply(lambda x: total_cost_helper(x['Transfer Value'], x['Min WD'], x['Max WD']), axis = 1)

	return df

def attributes_per_dollar(df):

	df['attributes_per_dollar'] = df.apply(lambda x: 'N/A' if x['total_cost'] == 'N/A' else 100000 * (x['attribute_sum'] / convert_multipliers(x['total_cost'])), axis = 1)

	return df

# Helper function for lambda function in role_scores()
def role_scores_helper(player, primary_attributes, secondary_attributes):

	# Multiplier controls how much more the primary attributes should contribute
	# to the role_score (as compared to the secondary attributes)
	primary_attributes_multiplier = 2
	relevant_attributes_sum = 0

	for attribute in primary_attributes:
		relevant_attributes_sum += primary_attributes_multiplier * player[player_roles.ABBRV_MAP[attribute]]

	for attribute in secondary_attributes:
		relevant_attributes_sum += player[player_roles.ABBRV_MAP[attribute]]

	return relevant_attributes_sum

def role_scores(df):

	for role in player_roles.ROLES:
		# The duty is the main modifier for a given role (e.g. Attack, Support, etc.)
		
		# Returns a list where each item is a possible duty for that role
		# For example, while iterating over the 'Inverted Winger' role, this call will
		# return a list with two elements: one for an 'Inverted Winger' in 'Attack', and
		# one for an 'Inverted Winger' in 'Support'
		role_duties_list = player_roles.ROLES[role]
		
		# Iterates through the list of available duties for the given role
		for role_duty in role_duties_list:
			# role_duty is stored as a dict with one key and one value
			# The key will be the current duty, and the value will be a list of the 
			# relevant attributes for that duty
			# For example, while iterating over the 'Attack' duty for the 'Inverted Winger'
			# role, role_duty will be equal to this dict:
			# 	{'Attack': [['Dribbling', 'Passing', 'Technique', 'Off The Ball', 'Acceleration', 'Agility'],
			#				['Crossing', 'First Touch', 'Long Shots', 'Anticipation', 'Composure', 'Decisions', 'Flair', 'Vision', 'Pace']]}
			
			# We're not actually iterating here. Since the duty name (e.g. 'Attack')
			# will always be the only key in the role_duty dict, we're using a 
			# for loop to grab that duty name
			for duty in role_duty:
				
				# role_plus_duty is a string representing a role & duty (e.g. 'Inverted Winger_Attack')
				role_plus_duty = '{}_{}'.format(role, duty)
				
				# role_plus_duty_list is a list containing two smaller lists representing the
				# primary and secondary relevant attributes for that role & duty
				# For example, the role_plus_duty_list for 'Inverted Winger_Attack' is equal to:
				# 	[['Dribbling', 'Passing', 'Technique', 'Off The Ball', 'Acceleration', 'Agility'],
				#	 ['Crossing', 'First Touch', 'Long Shots', 'Anticipation', 'Composure', 'Decisions', 'Flair', 'Vision', 'Pace']]
				role_plus_duty_list = role_duty[duty]
				
				primary_attributes = role_plus_duty_list[0]
				secondary_attributes = role_plus_duty_list[1]

				df[role_plus_duty] = df.apply(lambda x: role_scores_helper(x, primary_attributes, secondary_attributes), axis=1)
				
	return df

def build_html(df, print_no):

	build_html_start_time = time.time()

	with open('./web-output/out.txt', 'w') as web_output:

		web_output.write('<table>\n<tr>\n')
		for column in df.columns:
			web_output.write('<th>{}</th>\n'.format(column))
		web_output.write('</tr>\n')
		
		for index, row in df.head(print_no).iterrows():
			web_output.write('<tr>\n')
			for feature in df.columns:		
				web_output.write('<td>{}</td>\n'.format(row[feature]))
			web_output.write('</tr>\n')

		web_output.write('</table>\n')

	print('time to build html: {:.3f}s'.format(time.time() - build_html_start_time))

def print_players(df, features, print_no):
	# Overrides the default table break for pandas
	pd.set_option('display.expand_frame_repr', False)

	# pd.set_option('display.max_columns', None)

	print(df[features].head(print_no))

def print_help_msg(exit_status):
	
	print('Usage:\n'
		  '	1. Import custom view file (`./views/Player Search.fmf`) into the \'Player Search\' page\n'
		  '	2. Copy all view data (ctrl-A, ctrl-P) and save data as a text file to `./input/player_search.rtf`\n'
		  '	3. Use `./player_analysis.py` to analyze players and print top canidates\n'
		  'Options:\n'
		  '	-i, --input\n'
		  '		Specify the name of the input file; e.g., ./player_analysis.py -i [filename]\n'
		  '		Use -i multiple times to load multiple inputs;\n'
		  '		e.g. ./player_analysis -i input/rtf/player_search.rtf -i input/rtf/squad.rtf\n'
		  '	-c, --caching\n'
		  '		Enables caching; When enabled, the script will first attempt to load player\n'
		  '		data from an exisiting, cleaned .csv that corresponds to the given input .rtf\n'
		  '		e.g., ./input/rtf/player_search.rtf -> ./input/csv/player_search_cleaned.csv\n'
		  '		If the script does not find a cleaned .csv, it will process the .rtf normally\n'
		  '		and save the clean df into a new .csv file in the ./input/csv/ folder;\n'
		  '		Enabling caching allows for quicker processing times on subsequent runs\n'
		  '	-n, --new\n'
		  '		Used in conjunction with caching (-c); After exporting a new .rtf input from FM,\n'
		  '		use this flag to ignore the existing, cleaned .csv file and instead process\n'
		  '		the .rtf as though caching was disabled\n'
		  '		e.g. ./player_analyis.py -c -n -i ./input/rtf/player_search.rtf\n'
		  '	-l, --length\n'
		  '		specify the length of the output (i.e., the number of analyzed players to print)\n'
		  '		e.g., ./player_analyis.py -l 50\n'
		  '	-h, --help\n'
		  '		print this message')

	exit(exit_status)

if __name__ == '__main__':

	args = sys.argv[1:]

	caching 		  = False
	new_input		  = False
	hide_goalkeepers  = False
	hide_uninterested = False
	build_webpage	  = False

	input_filename_list = []
	print_no 			= DEFAULT_PRINT_NO
	sort_by 			= DEFAULT_SORT_BY

	# Iterate through args
	while len(args) > 0:
		arg = args.pop(0)
		if arg == '-h' or arg == '--help':
			print_help_msg(0)
		elif arg == '-i' or arg == '--input':
			input_filename_list.append(args.pop(0))
		elif arg == '-c' or arg == '--cache':
			caching = True
		elif arg == '-n' or arg == '--new':
			new_input = True
		elif arg == '-l' or arg == '--length':
			print_no = int(args.pop(0))
		elif arg == '-gk' or arg == '--hide-goalkeepers':
			hide_goalkeepers = True
		elif arg == '-s' or arg == '--sort':
			sort_by = args.pop(0)
		elif arg == '-u' or arg == '--uninterested':
			hide_uninterested = True
		elif arg == '-w' or arg == '--web':
			build_webpage = True
		else:
			print('error: failed to recognize argument \'{}\' while parsing command-line arguments'.format(arg))
			print_help_msg(1)

	if len(input_filename_list) == 0:
		input_filename_list.append(DEFAULT_INPUT_FILENAME)

	df = load_players(input_filename_list[0], caching, new_input)

	for input_filename in input_filename_list[1:]:
		new_df = load_players(input_filename, caching, new_input)
		df = pd.concat([df, new_df])

	if hide_goalkeepers:
		df = df[df['Position'] != 'GK']

	df = player_analyis(df, sort_by)

	if hide_uninterested:
		df = df[df['total_cost'] != 'N/A']

	if build_webpage:
		build_html(df, print_no)

	df = df.sort_values(by=sort_by, ascending=False)

	print_players(df, ['attribute_sum', 'Age', 'Name', 'total_cost', 'Advanced Forward_Attack'], print_no)
