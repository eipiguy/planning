import os, json
from os import path

class DocumentationCollector:

	def __init__( self, project_root_dir = 'portfolio', readme_name = 'README.md' ):
		self.project_root_dir = project_root_dir
		self.readme_name = readme_name
		self.project_dirs = self.find_readme_dirs()

	def find_readme_dirs( self ):
		readme_paths = {}
		for root_dir in os.listdir( self.project_root_dir ):
			# look for readme files
			# saves simple folder name paired with full dir
			project_dir = path.join( self.project_root_dir, root_dir )
			if path.isdir( project_dir ):
				for item in os.listdir( project_dir ):
					if self.readme_name in item:
						readme_paths[ root_dir ] = project_dir
		return readme_paths

def parse_main_hash_title( readme_path ):
	with open( readme_path, 'r' ) as file:
		for line in file:
			if line[:2] == '# ':
				return line[2:].strip()

def parse_header_from_readme( readme_path ):
	header_info = {}
	with open( readme_path, 'r' ) as file:
		read_header = False
		for line in file:
			# any line with the first three characters as dashes triggers the "header" metadata block
			if line[0:3] == '---':
				read_header = not read_header
			elif read_header and line[0:3] != '---':
				# does not support multi-line entries,
				# and you currently cannot include a colon at the end of a word in the key or data
				line_key_pair = line.strip().split( ': ', 1 )
				header_info[ line_key_pair[0] ] = line_key_pair[1]
	return header_info

def write_header_to_json( readme_path, json_path ):
	header_info = parse_header_from_readme( readme_path )
	with open( json_path, 'w+' ) as file:
		json.dump(header_info, file)

def write_header_values( file_path, header_dict ):
	lines = []
	has_header = False
	if path.isfile( file_path ):
		with open( file_path, 'r' ) as file:
			lines = file.readlines()
	with open( file_path, 'w+' ) as file:
		is_header = False
		used_keys = set()
		for line in lines:
			# any line with the first three characters as dashes triggers the "header" metadata block
			if line[0:3] == '---' and not is_header:
				has_header = True
				is_header = True
				file.write( line )
			elif is_header and line[0:3] != '---':
				line_key_pair = line.strip().split( ': ', 1 )
				if not ( line_key_pair[0] in header_dict.keys() ):
					file.write( line )
				else:
					file.write( f"{ line_key_pair[0] }: { header_dict[ line_key_pair[0] ] }\n" )
					used_keys.add( line_key_pair[0] )
			elif line[0:3] == '---' and is_header:
				if len(used_keys) < len(header_dict):
					# we need to write new data to the header
					unused_keys = header_dict.keys() - used_keys
					for key in unused_keys:
						file.write( f"{ key }: { header_dict[ key ] }\n" )
				file.write( line )
			elif not is_header:
				file.write( line )
	
	if not has_header:
		with open( file_path, 'w+' ) as file:
			file.write( '---\n' )
			for key in header_dict:
				file.write( f"{ key }: { header_dict[ key ] }\n" )
			file.write( '---\n' )
			file.writelines( lines )

def write_header_from_json( json_path, readme_path ):
	with open( json_path ) as file:
		header_info = json.load( file )
	write_header_values( readme_path, header_info )

def write_hash_title_to_header( file_path ):
	hash_title = parse_main_hash_title( file_path )
	write_header_values( file_path, { 'title': hash_title } )