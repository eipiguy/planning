import os, shutil
from os import path
from datetime import datetime

from src.collector import *

this_dir = path.dirname( path.realpath( __file__ ) )
portfolio_dir = path.join( this_dir, '..', '..' )
template_dir = path.join( this_dir, '..', 'templates' )
data_dir = path.join( this_dir, '..', 'data' )

project_collector = DocumentationCollector( portfolio_dir )

readme_dest = path.join( data_dir, 'readmes' )
os.mkdir( readme_dest )

default_header_path = path.join( template_dir, 'default_header_info.json' )
for project in project_collector.project_dirs:
	print( f"{ project }: { project_collector.project_dirs[ project ] }" )
	destination_path = path.join( readme_dest, f"{project}.md" )
	shutil.copy2(
		path.join(
			project_collector.project_dirs[ project ],
			project_collector.readme_name ),
		destination_path )

	header_info = {}
	header_info[ 'dir_name' ] = project
	header_info[ 'title' ] = parse_main_hash_title( destination_path )
	date_time = datetime.fromtimestamp( path.getmtime( project_collector.project_dirs[ project ] ) )
	header_info[ 'date' ] = str( date_time ).split()[0]

	write_json_to_header( default_header_path, destination_path )
	write_header_from_dict( header_info, destination_path )
