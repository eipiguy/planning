import os
from datetime import datetime
from os import path
import shutil
from src.collector import *

this_dir = path.dirname( path.realpath( __file__ ) )
project_dir = path.join( this_dir, '..', '..' )

project_collector = DocumentationCollector( project_dir )

readme_dest = path.join( this_dir, 'readmes' )
default_header_path = path.join( this_dir, 'default_header_info.json' )
os.mkdir( readme_dest )
for project in project_collector.project_dirs:
	header_info = {}
	header_info[ 'project' ] = project
	header_info[ 'title' ] = project
	date_time = datetime.fromtimestamp( path.getmtime( project_collector.project_dirs[ project ] ) )
	header_info[ 'date' ] = str( date_time ).split()[0]

	print( f"{ project }: { project_collector.project_dirs[ project ] }" )
	destination_path = path.join( readme_dest, f"{project}.md" )
	shutil.copy2(
		path.join(
			project_collector.project_dirs[ project ],
			project_collector.readme_name ),
		destination_path )
	write_header_from_json( default_header_path, destination_path )
	write_header_values( destination_path, header_info )
