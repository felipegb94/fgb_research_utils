#### Standard Library Imports
import os
import json
import re
import pickle

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

def save_object(obj, filepath):
	with open(filepath, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filepath): 
	with open(filepath, 'rb') as input_pickle_file:
		return pickle.load(input_pickle_file)

def simple_grep( filepath, str_to_search, n_lines=-1 ):
	'''
		Search text file and return the first n_lines containing that string
		If the line contains the string multiple times, it is only counted as a single line 
	'''
	assert(os.path.exists(filepath)), "{} does not exist".format(filepath)
	assert(n_lines >= -1), "n_lines needs to be -1 OR a non-negative integer. If it is -1 then we return all lines".format(filepath)
	f = open(filepath, "r")
	lines_with_str = []
	n_lines_found = 0
	for line in f:
		# Return if we found all lines asked to. If n_lines ==-1 then we just continue searching for all lines
		if((n_lines_found >= n_lines) and (n_lines >= 0)): return lines_with_str
		# search if line contains string, and save the line if it does
		if re.search(str_to_search, line):
			n_lines_found += 1
			lines_with_str.append(line.split('\n')[0]) # Remove the new line characted if there is any
	return lines_with_str

def get_dirnames_in_dir(dirpath, str_in_dirname=None):
	'''
		Output all the dirnames inside of dirpath.
		If str_in_dirname is given, only return the dirnames containing that string
	'''
	assert(os.path.exists(dirpath)), "Input dirpath does not exist"
	all_dirnames = next(os.walk(dirpath))[1]
	# If no string pattern is given return all dirnames
	if(str_in_dirname is None): return all_dirnames
	filtered_dirnames = []
	for curr_dirname in all_dirnames:
		if(str_in_dirname in curr_dirname):
			filtered_dirnames.append(curr_dirname)
	return filtered_dirnames