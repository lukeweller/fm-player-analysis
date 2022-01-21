# fm-player-analysis

### Usage:
1. Import custom view file (`./views/Player Search.fmf`) into the 'Player Search' page while in FM
2. Copy all view data (ctrl-A, ctrl-P) and save data as a text file to `./input/player_search.rtf`
3. Use `./player_analysis.py` to analyze players and print top canidates

### Options:
-i, --input
	specify the name of the input file;
	e.g., ./player_analysis.py -i [filename]
-c, --cache
	enables caching; when enabled, the script will first attempt to load player data from an exisiting, cleaned .csv that corresponds to the given input .rtf
	e.g., ./input/rtf/player_search.rtf -> ./input/csv/player_search_cleaned.csv
	if the script does not find a cleaned .csv, it will process the .rtf normally and save the clean df into a new .csv file in the ./input/csv/ folder;
	enabling caching allows for quicker processing times on subsequent runs
-n, --number
	specify the number of analyzed players to print; 
	e.g., ./player_analyis.py -n 25\
-h, --help
	print this message
