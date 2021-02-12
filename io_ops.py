#### Standard Library Imports
import os
import json
import re

#### Library imports

#### Local imports


def load_json( json_filepath ):
	assert( os.path.exists( json_filepath )), "{} does not exist".format( json_filepath )
	with open( json_filepath, "r" ) as json_file: 
		return json.load( json_file )

def write_json( json_filepath, input_dict ):
	assert(isinstance(input_dict, dict)), "write_json only works if the input_dict is of type dict"
	with open(json_filepath, 'w') as output_file: 
		json.dump(input_dict, output_file, indent=4)

def simple_grep( filepath, str_to_search, n_lines=1 ):
	'''
		Search text file and return the first n_lines containing that string
		If the line contains the string multiple times, it is only counted as a single line 
	'''
	assert(os.path.exists(filepath)), "{} does not exist".format(filepath)
	assert(n_lines >= 0), "n_lines needs to be a non-negative integer".format(filepath)
	f = open(filepath, "r")
	lines_with_str = []
	n_lines_found = 0
	for line in f:
		if(n_lines_found == n_lines): return lines_with_str
		if re.search(str_to_search, line):
			n_lines_found += 1
			lines_with_str.append(line.split('\n')[0]) # Remove the new line characted if there is any
	return lines_with_str
