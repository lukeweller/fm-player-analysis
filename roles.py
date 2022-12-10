#!/usr/bin/env python3

ROLES = {

# Goalkeeper Roles
'Goalkeeper':     [{'Defend':  [['Aerial Reach', 'Command of Area', 'Communication', 'Handling', 'Kicking', 'Reflexes', 'Concentration', 'Positioning', 'Agility'], 
				                ['One On Ones', 'Throwing', 'Anticipation', 'Decisions']]}],
'Sweeper Keeper': [{'Defend':  [['Command of Area', 'Kicking', 'One On Ones', 'Reflexes', 'Anticipation', 'Concentration', 'Positioning', 'Agility'],
							    ['Aerial Reach', 'Communication', 'First Touch', 'Handling', 'Passing', 'Rushing Out (Tendency)', 'Throwing', 'Composure', 'Decisions', 'Vision', 'Acceleration']]}, 
				   {'Support': [['Command of Area', 'Kicking', 'One On Ones', 'Reflexes', 'Rushing Out (Tendency)', 'Anticipation', 'Composure', 'Concentration', 'Positioning', 'Agility'],
							    ['Aerial Reach', 'Communication', 'First Touch', 'Handling', 'Passing', 'Throwing', 'Decisions', 'Vision', 'Acceleration']]}, 
				   {'Attack':  [['Command of Area', 'Kicking', 'One On Ones', 'Reflexes', 'Rushing Out (Tendency)', 'Anticipation', 'Composure', 'Concentration', 'Positioning', 'Agility'],
							    ['Aerial Reach', 'Communication', 'Eccentricity', 'First Touch', 'Handling', 'Passing', 'Throwing', 'Decisions', 'Vision', 'Acceleration']]}],

# Defending Roles
'Wide Centre-Back':        [{'Defend':  [['Crossing', 'Heading', 'Marking', 'Tackling', 'Positioning', 'Jumping Reach', 'Stamina', 'Strength'], 
										 ['Dribbling', 'Agression', 'Anticipation', 'Bravery', 'Composure', 'Concentration', 'Decisions', 'Work Rate', 'Pace']]}, 
							{'Support': [['Crossing', 'Dribbling', 'Heading', 'Marking', 'Tackling', 'Positioning', 'Jumping Reach', 'Pace', 'Stamina', 'Strength'], 
										 ['Agression', 'Anticipation', 'Bravery', 'Composure', 'Concentration', 'Decisions', 'Off The Ball', 'Work Rate']]}, 
							{'Attack':  [['Crossing', 'Dribbling', 'Heading', 'Marking', 'Tackling', 'Off The Ball', 'Jumping Reach', 'Pace', 'Stamina', 'Strength'], 
										 ['Agression', 'Anticipation','Bravery', 'Composure', 'Concentration', 'Decisions', 'Positioning', 'Work Rate']]}],
'Central Defender':        [{'Defend':  [['Heading', 'Marking', 'Tackling', 'Positioning', 'Jumping Reach', 'Strength'],
										 ['Agression', 'Anticipation', 'Bravery', 'Composure', 'Concentration', 'Decisions', 'Pace']]}, 
							{'Stopper': [['Heading', 'Tackling', 'Agression', 'Bravery', 'Decisions', 'Positioning', 'Jumping Reach', 'Strength'],
										 ['Marking', 'Anticipation', 'Composure', 'Concentration']]},
							{'Cover':   [['Marking', 'Tackling', 'Anticipation', 'Concentration', 'Decisions', 'Positioning', 'Pace'],
										 ['Heading', 'Bravery', 'Composure', 'Jumping Reach', 'Strength']]}],
'Libero':                  [{'Support': [['First Touch', 'Marking', 'Passing', 'Tackling', 'Anticipation', 'Composure', 'Concentration', 'Decisions', 'Positioning', 'Teamwork', 'Vision', 'Pace'],
										 ['Dribbling', 'Heading', 'Technique', 'Bravery', 'Flair', 'Agility', 'Balance', 'Jumping Reach', 'Stamina', 'Strength']]}, 
							{'Attack':  [['Dribbling', 'First Touch', 'Marking', 'Passing', 'Tackling', 'Anticipation', 'Composure', 'Concentration', 'Decisions', 'Flair', 'Positioning', 'Teamwork', 'Vision', 'Pace'],
										 ['Heading', 'Long Shots', 'Technique', 'Bravery', 'Acceleration', 'Agility', 'Balance', 'Jumping Reach', 'Stamina', 'Strength']]}],
'Ball Playing Defender':   [{'Defend':  [['Heading', 'Marking', 'Passing', 'Tackling', 'Composure', 'Positioning', 'Jumping Reach', 'Strength'],
										 ['First Touch', 'Technique', 'Agression', 'Anticipation', 'Bravery', 'Concentration', 'Decisions', 'Vision', 'Pace']]}, 
							{'Stopper': [['Heading', 'Passing', 'Tackling', 'Agression', 'Bravery', 'Composure', 'Decisions', 'Positioning', 'Jumping Reach', 'Strength'],
										 ['First Touch', 'Marking', 'Technique', 'Anticipation', 'Concentration', 'Vision']]},
							{'Cover':   [['Marking', 'Passing', 'Tackling', 'Anticipation', 'Composure', 'Concentration', 'Decisions', 'Positioning', 'Pace'],
										 ['First Touch', 'Heading', 'Technique', 'Bravery', 'Vision', 'Jumping Reach', 'Strength']]}],
'No-Nonsense Centre-Back': [{'Defend':  [['Heading', 'Marking', 'Tackling', 'Positioning', 'Jumping Reach', 'Strength'],
										 ['Agression', 'Anticipation', 'Bravery', 'Concentration', 'Pace']]},
						    {'Stopper': [['Heading', 'Tackling', 'Agression', 'Bravery', 'Positioning', 'Jumping Reach', 'Strength'],
										 ['Marking', 'Anticipation', 'Concentration']]},
						    {'Cover':   [['Marking', 'Tackling', 'Anticipation', 'Concentration', 'Positioning', 'Pace'],
										 ['Heading', 'Bravery', 'Jumping Reach', 'Strength']]}],

# Midfield Roles
# 'Defensive Midfielder':    [{'Defend':  [[],
# 										 []]}, 
# 							{'Support': [[],
# 										 []]}],
# 'Deep Lying Playmaker':    [{'Defend':  [[],
# 										 []]}, 
# 							{'Support': [[],
# 										 []]}],
# 'Ball Winning Midfielder': [{'Defend':  [[],
# 										 []]}, 
# 							{'Support': [[],
# 										 []]}],
# 'Anchor Man':              [{'Defend':  [[],
# 										 []]}],
# 'Half Back':               [{'Defend':  [[],
# 										 []]}],
'Regista':                 [{'Support': [['First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Flair', 'Off The Ball', 'Teamwork', 'Vision'],
										 ['Dribbling', 'Long Shots', 'Anticipation', 'Balance']]}],
'Roaming Playmaker':       [{'Support': [['First Touch', 'Passing', 'Technique', 'Anticipation', 'Composure', 'Decisions', 'Off The Ball', 'Teamwork', 'Vision', 'Work Rate', 'Acceleration', 'Stamina'],
										 ['Dribbling', 'Long Shots', 'Concentration', 'Positioning', 'Agility']]}], 
# 'Segundo Volante':         [{'Support': [[],
# 										 []]}, 
# 							{'Attack':  [[],
# 										 []]}],
# 'Central Midfielder':      [{'Defend':  [[],
# 										 []]},
# 							{'Support': [[],
# 										 []]},
# 							{'Attack':  [[],
# 										 []]}],
# 'Box-to-Box Midfielder':   [{'Support': [[],
# 										 []]}],
# 'Mezzala':                 [{'Support': [[],
# 										 []]}, 
# 							{'Attack':  [[],
# 										 []]}],
# 'Carrilero':               [{'Support': [[],
# 										 []]}],

# Flank Roles
'Full Back':             [{'Defend':  [['Marking', 'Tackling', 'Anticipation', 'Concentration', 'Positioning'],
									   ['Crossing', 'Passing', 'Composure', 'Decisions', 'Teamwork', 'Pace', 'Stamina']]}, 
						  {'Support': [['Marking', 'Tackling', 'Anticipation', 'Concentration', 'Positioning', 'Teamwork', 'Work Rate'],
						  			   ['Crossing', 'Dribbling', 'Passing', 'Technique', 'Composure', 'Decisions', 'Pace', 'Stamina']]},
						  {'Attack':  [['Crossing', 'Tackling', 'Anticipation', 'Positioning', 'Teamwork', 'Work Rate', 'Pace', 'Stamina'],
						  			   ['Dribbling', 'First Touch', 'Marking', 'Passing', 'Technique', 'Composure', 'Concentration', 'Decisions', 'Off The Ball', 'Acceleration', 'Agility']]}],
'Wing Back':             [{'Defend':  [['Marking', 'Tackling', 'Anticipation', 'Positioning', 'Teamwork', 'Work Rate', 'Acceleration', 'Stamina'],
									   ['Crossing', 'Dribbling', 'First Touch', 'Passing', 'Technique', 'Concentration', 'Decisions', 'Off The Ball', 'Agility', 'Pace']]}, 
						  {'Support': [['Crossing', 'Dribbling', 'Marking', 'Tackling', 'Off The Ball', 'Teamwork', 'Work Rate', 'Acceleration', 'Stamina'],
						  			   ['First Touch', 'Passing', 'Technique', 'Anticipation', 'Concentration', 'Decisions', 'Positioning', 'Agility', 'Pace']]},
						  {'Attack':  [['Crossing', 'Dribbling', 'Tackling', 'Technique', 'Off The Ball', 'Teamwork', 'Work Rate', 'Acceleration', 'Pace', 'Stamina'],
						  			   ['First Touch', 'Marking', 'Passing', 'Anticipation', 'Concentration', 'Decisions', 'Flair', 'Positioning', 'Agility']]}],
'No-Nonsense Full Back': [{'Defend':  [['Marking', 'Tackling', 'Anticipation', 'Positioning', 'Strength'],
									   ['Heading', 'Agression', 'Bravery', 'Concentration', 'Teamwork']]}],
'Complete Wing Back':    [{'Support': [['Crossing', 'Dribbling', 'First Touch', 'Passing', 'Technique', 'Decisions', 'Off The Ball', 'Teamwork', 'Work Rate', 'Acceleration', 'Pace', 'Stamina'],
									   ['Tackling', 'Anticipation', 'Composure', 'Flair', 'Agility', 'Balance']]}, 
						  {'Attack':  [['Crossing', 'Dribbling', 'First Touch', 'Passing', 'Technique', 'Decisions', 'Flair', 'Off The Ball', 'Teamwork', 'Work Rate', 'Acceleration', 'Pace', 'Stamina'],
									   ['Tackling', 'Anticipation', 'Composure', 'Agility','Balance']]}],
'Inverted Wing Back':    [{'Defend':  [['Marking', 'Passing', 'Tackling', 'Anticipation', 'Decisions', 'Positioning', 'Teamwork', 'Work Rate'],
									   ['Dribbling', 'First Touch', 'Technique', 'Concentration', 'Off The Ball', 'Acceleration', 'Agility', 'Stamina']]}, 
						  {'Support': [['Marking', 'Passing', 'Tackling', 'Decisions', 'Off The Ball', 'Teamwork', 'Work Rate', 'Stamina'],
						  			   ['Dribbling', 'First Touch', 'Technique', 'Anticipation', 'Composure', 'Concentration', 'Positioning', 'Acceleration', 'Agility']]},
						  {'Attack':  [['Dribbling', 'Marking', 'Passing', 'Tackling', 'Technique', 'Decisions', 'Off The Ball', 'Teamwork', 'Work Rate', 'Anticipation', 'Stamina'],
						  			   ['First Touch', 'Long Shots', 'Anticipation', 'Composure', 'Concentration', 'Flair', 'Positioning', 'Agility', 'Pace']]}],
'Wide Midfielder':       [{'Defend':  [['Passing', 'Tackling', 'Concentration', 'Decisions', 'Positioning', 'Teamwork', 'Work Rate'],
									   ['Crossing', 'First Touch', 'Marking', 'Technique', 'Anticipation', 'Composure', 'Stamina']]}, 
						  {'Support': [['Passing', 'Tackling', 'Decisions', 'Teamwork', 'Work Rate', 'Stamina'],
						  			   ['Crossing', 'First Touch', 'Technique', 'Anticipation', 'Composure', 'Concentration', 'Off The Ball', 'Positioning', 'Vision']]},
						  {'Attack':  [['Crossing', 'First Touch', 'Passing', 'Decisions', 'Teamwork', 'Work Rate', 'Stamina'],
						  			   ['Tackling', 'Technique', 'Anticipation', 'Composure', 'Off The Ball', 'Vision']]}],
'Winger':                [{'Support': [['Crossing', 'Dribbling', 'Technique', 'Off The Ball', 'Acceleration', 'Pace'],
									   ['First Touch', 'Passing', 'Work Rate', 'Agility', 'Stamina']]}, 
						  {'Attack':  [['Crossing', 'Dribbling', 'Technique', 'Off The Ball', 'Acceleration', 'Pace'],
									   ['First Touch', 'Passing', 'Anticipation', 'Flair', 'Agility']]}],
'Defensive Winger':      [{'Defend':  [['Technique', 'Anticipation', 'Off The Ball', 'Positioning', 'Teamwork', 'Work Rate', 'Stamina'],
									   ['Crossing', 'Dribbling', 'First Touch', 'Marking', 'Tackling', 'Agression', 'Concentration', 'Decisions', 'Acceleration']]}, 
						  {'Support': [['Crossing', 'Technique', 'Off The Ball', 'Teamwork', 'Work Rate', 'Stamina'],
									   ['Dribbling', 'First Touch', 'Marking', 'Passing', 'Tackling', 'Agression', 'Anticipation', 'Composure', 'Concentration', 'Decisions', 'Positioning', 'Acceleration']]}],
'Wide Playmaker':        [{'Support': [['First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Teamwork', 'Vision'],
									   ['Dribbling', 'Off The Ball', 'Agility']]}, 
						  {'Attack':  [['Dribbling', 'First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Off The Ball', 'Teamwork', 'Vision'],
									   ['Anticipation', 'Flair', 'Acceleration', 'Agility']]}],
'Inverted Winger':       [{'Support': [['Dribbling', 'Passing', 'Technique', 'Off The Ball', 'Acceleration'],
									   ['Crossing', 'First Touch', 'Long Shots', 'Composure', 'Decisions', 'Vision', 'Work Rate', 'Agility', 'Pace', 'Stamina']]}, 
						  {'Attack':  [['Dribbling', 'Passing', 'Technique', 'Off The Ball', 'Acceleration', 'Agility'],
									   ['Crossing', 'First Touch', 'Long Shots', 'Anticipation', 'Composure', 'Decisions', 'Flair', 'Vision', 'Pace']]}],								   
'Wide Target Forward':  [{'Support':  [['Heading', 'Bravery', 'Teamwork', 'Jumping Reach', 'Strength'],
									   ['Crossing', 'First Touch', 'Anticipation', 'Off The Ball', 'Work Rate', 'Balance', 'Stamina']]}, 
						 {'Attack':   [['Heading', 'Bravery', 'Off The Ball', 'Jumping Reach', 'Strength'],
									   ['Crossing', 'Finishing', 'First Touch', 'Anticipation', 'Teamwork', 'Work Rate', 'Balance', 'Stamina']]}],
'Raumdeuter':  			[{'Attack':   [['Finishing', 'Anticipation', 'Composure', 'Concentration', 'Decisions', 'Off The Ball', 'Balance'],
									   ['First Touch', 'Technique', 'Work Rate', 'Acceleration', 'Stamina']]}],							  
'Inside Forward':  		[{'Support':  [['Dribbling', 'First Touch', 'Passing', 'Technique', 'Off The Ball', 'Acceleration', 'Agility', 'Balance'],
									   ['Finishing', 'Long Shots', 'Anticipation', 'Composure', 'Flair', 'Vision', 'Pace']]}, 
						 {'Attack':   [['Dribbling', 'Finishing', 'First Touch', 'Technique', 'Off The Ball', 'Acceleration', 'Agility', 'Balance'],
									   ['Long Shots', 'Passing', 'Anticipation', 'Composure', 'Flair', 'Pace']]}],

# Attacking Roles
'Shadow Striker': 		[{'Attack':  [['Dribbling', 'Finishing', 'First Touch', 'Anticipation', 'Composure', 'Off The Ball', 'Acceleration'],
							    	  ['Passing', 'Technique', 'Concentration', 'Decisions', 'Work Rate', 'Agility', 'Balance', 'Pace', 'Stamina']]}],
'Trequarista':    		[{'Attack':  [['Dribbling', 'First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Flair', 'Off The Ball', 'Vision', 'Acceleration'],
									  ['Finishing', 'Anticipation', 'Agility', 'Balance']]}], 
'Enganche':    	  		[{'Support': [['First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Vision'],
							    	  ['Dribbling', 'Anticipation', 'Flair', 'Off The Ball', 'Teamwork', 'Agility']]}], 
'Attacking Midfielder': [{'Support': [['First Touch', 'Long Shots', 'Passing', 'Technique', 'Anticipation', 'Decisions', 'Flair', 'Off The Ball'],
									  ['Dribbling', 'Composure', 'Vision', 'Agility']]}, 
						 {'Attack':  [['Dribbling', 'First Touch', 'Long Shots', 'Passing', 'Technique', 'Anticipation', 'Decisions', 'Flair', 'Off The Ball'],
									  ['Finishing', 'Composure', 'Vision', 'Agility']]}],							   
'Advanced Playmaker':   [{'Support': [['First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Off The Ball', 'Teamwork', 'Vision'],
									  ['Dribbling', 'Anticipation', 'Flair', 'Agility']]}, 
						 {'Attack':  [['Dribbling', 'First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Off The Ball', 'Teamwork', 'Vision'],
									  ['Anticipation', 'Flair', 'Acceleration', 'Agility']]}],
'Complete Forward':   	[{'Support': [['Dribbling', 'First Touch', 'Heading', 'Long Shots', 'Passing', 'Technique', 'Anticipation', 'Composure', 'Decisions', 'Off The Ball', 'Vision', 'Acceleration', 'Agility', 'Strength'],
									  ['Finishing', 'Teamwork', 'Work Rate', 'Balance', 'Jumping Reach', 'Pace', 'Stamina']]}, 
						 {'Attack':  [['Dribbling', 'Finishing', 'First Touch', 'Heading', 'Technique', 'Anticipation', 'Composure', 'Off The Ball', 'Acceleration', 'Agility', 'Strength'],
									  ['Long Shots', 'Passing', 'Decisions', 'Teamwork', 'Vision', 'Work Rate', 'Balance', 'Jumping Reach', 'Pace', 'Stamina']]}],
'Poacher':  			[{'Attack':  [['Finishing', 'Anticipation', 'Composure', 'Off The Ball'],
									  ['First Touch', 'Heading', 'Technique', 'Decisions', 'Acceleration']]}],
'False Nine':  			[{'Support': [['Dribbling', 'First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Off The Ball', 'Vision', 'Acceleration', 'Agility'],
									  ['Finishing', 'Anticipation', 'Flair', 'Teamwork', 'Balance']]}],
'Deep Lying Forward':   [{'Support': [['First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Off The Ball', 'Teamwork'],
									  ['Finishing', 'Anticipation', 'Flair', 'Vision', 'Balance', 'Strength']]}, 
						 {'Attack':  [['First Touch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Off The Ball', 'Teamwork'],
									  ['Dribbling', 'Finishing', 'Anticipation', 'Flair', 'Vision', 'Balance', 'Strength']]}],
'Pressing Forward':     [{'Defend':  [['Agression', 'Anticipation', 'Bravery', 'Decisions', 'Teamwork', 'Work Rate', 'Acceleration', 'Pace', 'Stamina'],
									  ['First Touch', 'Composure', 'Concentration', 'Agility', 'Balance', 'Strength']]},
						 {'Support': [['Agression', 'Anticipation', 'Bravery', 'Decisions', 'Teamwork', 'Work Rate', 'Acceleration', 'Pace', 'Stamina'],
									  ['First Touch', 'Passing', 'Composure', 'Concentration', 'Off The Ball', 'Agility', 'Balance', 'Strength']]},
						 {'Attack':  [['Agression', 'Anticipation', 'Bravery', 'Off The Ball', 'Teamwork', 'Work Rate', 'Acceleration', 'Pace', 'Stamina'],
									  ['Finishing', 'First Touch', 'Composure', 'Concentration', 'Decisions', 'Agility', 'Balance', 'Strength']]}],
'Advanced Forward':  	[{'Attack':  [['Dribbling', 'Finishing', 'First Touch', 'Technique', 'Composure', 'Off The Ball', 'Acceleration'],
									  ['Passing', 'Anticipation', 'Decisions', 'Work Rate', 'Agility', 'Balance', 'Pace', 'Stamina']]}],
# 'Target Forward':       [{'Defend':  [[],
# 									  []]},
# 						 {'Support': [[],
# 									  []]},
# 						 {'Attack':  [[],
# 									  []]}],

}

ABBRV_MAP = {'Corners': 'Cor',
			 'Crossing': 'Cro',
			 'Dribbling': 'Dri',
			 'Finishing': 'Fin',
			 'First Touch': 'Fir',
			 'Free Kick Tacking': 'Fre',
			 'Heading': 'Hea',
			 'Long Shots': 'Lon',
			 'Long Throws': 'L Th',
			 'Marking': 'Mar',
			 'Passing': 'Pas',
			 'Penalty Taking': 'Pen',
			 'Tackling': 'Tck',
			 'Technique': 'Tec',
			 'Agression': 'Agg',
			 'Anticipation': 'Ant',
			 'Bravery': 'Bra',
			 'Composure': 'Cmp',
			 'Concentration': 'Cnt',
			 'Decisions': 'Dec',
			 'Determination': 'Det',
			 'Flair': 'Fla',
			 'Leadership': 'Ldr',
			 'Off The Ball': 'OtB',
			 'Positioning': 'Pos',
			 'Teamwork': 'Tea',
			 'Vision': 'Vis',
			 'Work Rate': 'Wor',
			 'Acceleration': 'Acc',
			 'Agility': 'Agi',
			 'Balance': 'Bal',
			 'Jumping Reach': 'Jum',
			 'Natural Fitness': 'Nat',
			 'Pace': 'Pac',
			 'Stamina': 'Sta',
			 'Strength': 'Str',
			 'Aerial Reach': 'Aer',
			 'Command of Area': 'Cmd',
			 'Communication': 'Com',
			 'Eccentricity': 'Ecc',
			 'Handling': 'Han',
			 'Kicking': 'Kic',
			 'One On Ones': '1v1',
			 'Punching (Tendency)': 'Pun',
			 'Reflexes': 'Ref',
			 'Rushing Out (Tendency)': 'TRO',
			 'Throwing': 'Thr'	
}

 

if __name__ == '__main__':

	print(ROLES)