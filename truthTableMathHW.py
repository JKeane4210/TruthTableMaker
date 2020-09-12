'''
objectives
	for every operation chracter, letter (boolean representation) in input string
	
		# 		0:3 -> 1
		# 		0:1, 4:5 -> 1
		# 		0, 2, 4, 6 -> 1

		# 		0 -> 1,1,1
		# 		1 -> 1,1,0
		# 		2 -> 1,0,1
		# 		3 -> 1,0,0
		
	*probably want to has my values that are split by spaces
'''

from prettytable import PrettyTable
import argparse

DENIAL_SYMBOL  = "~"
SYMBOLS        = ["&", "|", "(+)", "<->", "->"]
BOOL_VARS_DICT = {}
bool_vars      = []

def bit_combos(bits):
	change_intervals = [int(2 ** bits / 2 ** i) for i in range(0, bits)]
	changes_indices = [change_point for change_point in change_intervals]
	rows = []
	for i in range(0, int(2 ** bits)):
		rows.append([int((i) % change_interval >= change_interval // 2) for change_interval in change_intervals]) #appending the correct value
	return rows

def bool_var_ind(string, bool_var):
	bool_var_count = 0
	for c in string:
		if c == bool_var:
			return bool_var_count
		if c.isalpha():
			bool_var_count += 1

def comparison(a, b, operation):
	comp_and           = lambda x, y: x and y
	comp_or            = lambda x, y: x or y
	comp_xor           = lambda x, y: x != y
	comp_biconditional = lambda x, y: x == y
	comp_mc            = lambda x, y: 1 if x else y

	comparators = {
				   "&"   : comp_and, 
				   "|"   : comp_or, 
				   "(+)" : comp_xor, 
				   "<->" : comp_biconditional,
				   "->"	 : comp_mc
				  }
	func = comparators[operation]
	return func(a, b)

def bool_vars_to_compare(args, index, regard_parentheses : bool = False):
	try:
		b1 = args[index - 1]
		b2 = args[index + 1]
		if regard_parentheses == True:
			if b1 == ")":
				new_b1 = ""
				j = 2
				while args[index - j] != "(":
					new_b1 = args[index - j] + new_b1
					j += 1
					if args[index - j] != "(": new_b1 = " " + new_b1
				b1 = new_b1
			if b2 == "(":
				new_b2 = ""
				j = 2
				while args[index + j] != ")":
					new_b2 += args[index + j]
					j += 1
					if args[index + j] != ")": new_b2 += " "

				b2 = new_b2
		return b1, b2
	except:
		print(f"ERROR: NO TWO COMMANDS TO CONDUCT OPERATION ON FOR OPERATION '{bool_var}'")
		exit()

if "__main__" == __name__:
	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--string", help="string to be converted into truth table")
	args = vars(ap.parse_args())

	if args["string"] != None:
		ARG_STRING     = args["string"]
		bits           = 0
		#BIT FINDING LOOP
		for i, c in enumerate(ARG_STRING):
			if c.isalpha() and c not in bool_vars:
				bits += 1
				bool_vars.append(c)
		# BIT COLUMNS LOOP
		for i, bool_var in enumerate(bool_vars):
			BOOL_VARS_DICT[bool_var] = [bit_combo[i] for bit_combo in bit_combos(bits)]
		ARG_STRING_SPLITS = ARG_STRING.split(" ")
		# DENIAL LOOP
		for i, bool_var in enumerate(ARG_STRING_SPLITS):
			if bool_var.find(DENIAL_SYMBOL) != -1:
				BOOL_VARS_DICT[bool_var] = [int(value == 0) for value in BOOL_VARS_DICT[bool_var[-1]]]
		# GENERAL COMPARISON OPERATOR LOOP
		for i, bool_var in enumerate(ARG_STRING_SPLITS):
			if bool_var in SYMBOLS:
				b1, b2 = bool_vars_to_compare(ARG_STRING_SPLITS, i)
				if b1 != ")" and b2 != "(":
					first_bool_var_column = BOOL_VARS_DICT[b1]
					second_bool_var_column = BOOL_VARS_DICT[b2]
					BOOL_VARS_DICT[f"{b1} {bool_var} {b2}"] = [int(comparison(first_bool_var_column[j], second_bool_var_column[j], bool_var)) for j in range(0, int(2 ** bits))]
		# COMPOUND STATEMENTS LOOP
		for i, bool_var in enumerate(ARG_STRING_SPLITS):
			if bool_var in SYMBOLS:
				b1, b2 = bool_vars_to_compare(ARG_STRING_SPLITS, i, regard_parentheses = True)
				first_bool_var_column = BOOL_VARS_DICT[b1]
				second_bool_var_column = BOOL_VARS_DICT[b2]
				if BOOL_VARS_DICT.get(f"{b1} {bool_var} {b2}") == None:
					BOOL_VARS_DICT[f"({b1}) {bool_var} ({b2})"] = [int(comparison(first_bool_var_column[j], second_bool_var_column[j], bool_var)) for j in range(0, int(2 ** bits))]

		# print(BOOL_VARS_DICT)

		t = PrettyTable()
		for bool_var in BOOL_VARS_DICT:
			t.add_column(bool_var, BOOL_VARS_DICT[bool_var])
		print(t)

# -----------------------------------------------------------------------------------
	# CONJUNCTION_SYMBOL = "&"
	# DYSJUNCTION_SYMBOL = "|"
	# EXCLUSIVE_OR_SYMBOL = "(+)"
	# BICONDITIONAL_SYMBOL = "<->"	
	# ----------------------------
	# if bool_var == CONJUNCTION_SYMBOL:
	# 	first_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i - 1]]
	# 	second_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i + 1]]
	# 	BOOL_VARS_DICT[f"{ARG_STRING_SPLITS[i-1]}&{ARG_STRING_SPLITS[i+1]}"] = [int(first_bool_var_column[j] and second_bool_var_column[j]) for j in range(0, int(2 ** bits))]
	# if bool_var == DYSJUNCTION_SYMBOL:
	# 	first_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i - 1]]
	# 	second_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i + 1]]
	# 	BOOL_VARS_DICT[f"{ARG_STRING_SPLITS[i-1]}|{ARG_STRING_SPLITS[i+1]}"] = [int(first_bool_var_column[j] or second_bool_var_column[j]) for j in range(0, int(2 ** bits))]
	# if bool_var == EXCLUSIVE_OR_SYMBOL:
	# 	first_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i - 1]]
	# 	second_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i + 1]]
	# 	BOOL_VARS_DICT[f"{ARG_STRING_SPLITS[i-1]}(+){ARG_STRING_SPLITS[i+1]}"] = [int(first_bool_var_column[j] != second_bool_var_column[j]) for j in range(0, int(2 ** bits))]
	# if bool_var == BICONDITIONAL_SYMBOL:
	# 	first_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i - 1]]
	# 	second_bool_var_column = BOOL_VARS_DICT[ARG_STRING_SPLITS[i + 1]]
	# 	BOOL_VARS_DICT[f"{ARG_STRING_SPLITS[i-1]}<->{ARG_STRING_SPLITS[i+1]}"] = [int(first_bool_var_column[j] == second_bool_var_column[j]) for j in range(0, int(2 ** bits))]

