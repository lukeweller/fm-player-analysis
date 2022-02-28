# fm-player-analysis

### Usage:
1. Import custom view file (`./views/Player Search.fmf`) into the 'Player Search' page while in FM
2. Copy all view data (ctrl-A, ctrl-P) and save data as a text file to `./input/player_search.rtf`
3. Use `./player_analysis.py` to analyze players and print top canidates

### Options:
```
-i, --input
	Specify the name of the input file; e.g., ./player_analysis.py -i [filename]
	Use -i multiple times to load multiple inputs;
	e.g. ./player_analysis -i input/rtf/player_search.rtf -i input/rtf/squad.rtf
-c, --caching
	Enables caching; When enabled, the script will first attempt to load player
	data from an exisiting, cleaned .csv that corresponds to the given input .rtf
	e.g., ./input/rtf/player_search.rtf -> ./input/csv/player_search_cleaned.csv
	If the script does not find a cleaned .csv, it will process the .rtf normally
	and save the clean df into a new .csv file in the ./input/csv/ folder;
	Enabling caching allows for quicker processing times on subsequent runs
-n, --new
	Used in conjunction with caching (-c); After exporting a new .rtf input from FM,
	use this flag to ignore the existing, cleaned .csv file and instead process
	the .rtf as though caching was disabled
	e.g. ./player_analyis.py -c -n -i ./input/rtf/player_search.rtf
-l, --length
	specify the length of the output (i.e., the number of analyzed players to print)
	e.g., ./player_analyis.py -l 50
-h, --help
	print this message
```