import os, json
from os import path

README_NAME = 'README.md'

class DocumentationCollector:

	def __init__( self, project_root_dir = 'portfolio', readme_name = README_NAME ):
		self.this_dir = path.dirname( path.realpath( __file__ ) )
		self.template_dir = path.join( self.this_dir, '..', '..', 'templates' )

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

	def parse_headers( self ):
		self.headers = {}
		for project in self.project_dirs:
			self.headers[project] = parse_header( self.get_readme_path(project) )

	def get_readme_path( self, project ):
		return path.join( self.project_dirs[project], self.readme_name )
	
	def get_readme_data( self, project ):
		return markdown_to_dict( self.get_readme_path( project ) )

	def get_template_data( self, template = README_NAME ):
		template_path = path.join( self.template_dir, template )
		return markdown_to_dict( template_path )

	def update_readmes( self ):
		template_data = self.get_template_data()
		for project in self.project_dirs:
			readme_data = self.get_readme_data( project )

			# Update readme to match template:

			# For each template section,
			# search for the corresponding readme section
			# and move it to the correct order and depth
			cur_order = 0
			new_sections = 0
			updated_data = {}
			for template_section in template_data:
				if ( template_section in readme_data ):
					template_section_data = template_data[ template_section ]
					updated_data[ template_section ] = [
						template_section_data[0],
						template_section_data[1],
						readme_data[ template_section ] ]


			# If the section doesn't exist,
			# add it in the correct place with default data
			
			# Any "extra" sections that aren't in the template
			# should be moved with their parent section if it is moved
			# and otherwise left where they are

def parse_main_hash_title( file_path ):
	with open( file_path, 'r' ) as file:
		for line in file:
			if line[:2] == '# ':
				return line[2:].strip()

def num_initial_hashes( string ):
	num_hashes = 0
	for letter in string:
		if letter == '#':
			num_hashes += 1
		else:
			break
	return num_hashes

def markdown_to_dict( file_path ):
	section_list = get_section_list( file_path )

	# work from max depth backwards to build nested list
	nesting_level = calculate_max_depth( section_list )
	while nesting_level > 0:
		# look through list for any sections at the current nesting level
		for i,section in enumerate(section_list):
			if( not 'children' in section_list[i] ):
				section_list[i]['children'] = {}
			if( section['depth'] == nesting_level ):
				parent_id = find_parent( section_list, i, section['depth'] )

				if ( parent_id >= 0 ):
					# move the child to the parent in the section list
					section_list[parent_id]['children'][ section['key'] ] = {
						'content': section['content']
					}
					if( section['children'] != {} ):
						section_list[parent_id]['children'][ section['key'] ]['children'] = section['children'].copy()
					del section_list[i]

		# decrease the nesting level
		nesting_level -= 1

	nested_dict = {}
	for section in section_list:
		nested_dict[ section['key'] ] = {
			'content': section['content'],
		}
		if( section['children'] != {} ):
			nested_dict[ section['key'] ]['children'] = section['children'].copy()
	return nested_dict

def find_parent( section_list, order, depth ):
	max_parent_depth = 0
	parent_id = -1
	for i in reversed(range(order)):
		cur_depth = section_list[i]['depth']
		if( cur_depth < depth ):
			parent_id = i
			break
	return parent_id

def calculate_max_depth( section_list ):
	max_depth = 0
	for section in section_list:
		if section['depth'] > max_depth:
			max_depth = section['depth']
	return max_depth

def calculate_num_children( section_list ):
	num_children = []
	# Check number of children for each section
	for i,section in enumerate(section_list):
		for j,next_section in enumerate(section_list[i+1:]):
			if( next_section['depth'] > section['depth'] ):
				num_children.append(j + 1)
			else:
				break
	return num_children

def get_section_list( file_path ):
	section_list = []
	key = ""
	content = ""
	depth = 0
	with open( file_path, 'r' ) as file:
		for line in file:
			if line[0] == '#':
				if key != "":
					section_list.append( {
						'depth': depth,
						'key': key,
						'content': content
					} )

				depth = num_initial_hashes( line )
				key = line[depth:].strip()
				content = ""
			else:
				content += line
		content += '\n'
		if key != "":
			section_list.append( {
				'depth': depth,
				'key': key,
				'content': content
			} )
	return section_list

def parse_header( file_path ):
	header_info = {}
	with open( file_path, 'r' ) as file:
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

def write_header_to_json( file_path, json_path ):
	header_info = parse_header( file_path )
	with open( json_path, 'w+' ) as file:
		json.dump(header_info, file)

def write_header_from_dict( header_dict, file_path ):
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

def write_json_to_header( json_path, file_path ):
	with open( json_path ) as file:
		header_info = json.load( file )
	write_header_from_dict( header_info, file_path )

def write_hash_title_to_header( file_path ):
	hash_title = parse_main_hash_title( file_path )
	write_header_from_dict( { 'title': hash_title }, file_path )