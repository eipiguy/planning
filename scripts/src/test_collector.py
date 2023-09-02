import unittest, json
from shutil import copy2
from os import path
from filecmp import cmp

from collector import *
from tools import *

class TestCollectionMethods( unittest.TestCase ):

	def setUp(self):
		assets_dir_name = 'assets'
		projects_dir_name = 'test_projects'
		project_name = 'test_project_a'
		readme_name = 'README.md'

		this_dir = path.dirname( path.realpath( __file__ ) )
		self.test_dir = path.join( this_dir, assets_dir_name )

		test_project_dir = path.join( self.test_dir, projects_dir_name )
		self.test_readme_path = path.join( test_project_dir, project_name, readme_name )

		self.doc_collector = DocumentationCollector( test_project_dir, readme_name )

	def baseline( self, test_name, extension = 'json' ):
		return path.join( self.test_dir, 'baseline', test_name + '.' + extension )

	def test_asset_dir_exists( self ):
		self.assertTrue( path.isdir( self.doc_collector.project_root_dir ) )

	def test_asset_readme_exists( self ):
		self.assertTrue( path.isfile( self.test_readme_path ) )

	def test_finds_readme( self ):
		# doc collector should find the assets folder as a project directory
		test_project_name = 'test_project_a'
		self.assertIn( test_project_name, self.doc_collector.find_readme_dirs() )

	def test_parse_header_from_readme( self ):
		test_header_info = parse_header( self.test_readme_path )

		with open( self.baseline( 'test_parse_header_from_readme' ) ) as file:
			baseline_header_info = json.load( file )

		self.assertEqual( test_header_info, baseline_header_info )

	def test_writes_header_to_json( self ):
		# write readme header info to temp json
		temp_file_path = self.baseline( 'test_writes_header_to_json_temp' )
		write_header_to_json( self.test_readme_path, temp_file_path )

		# read written data and compare to baseline
		with open( temp_file_path ) as file:
			test_header_info = json.load( file )
		os.remove( temp_file_path )

		with open( self.baseline( 'test_writes_header_to_json' ) ) as file:
			baseline_header_info = json.load( file )

		self.assertEqual( test_header_info, baseline_header_info )

	def test_writes_header_from_json( self ):
		# json data to write to temp readme test file
		json_header_path = self.baseline( 'test_writes_header_from_json' )
		
		# test readme to compare to written result
		temp_file_path = self.baseline( 'test_writes_header_from_json_temp', 'md' )
		write_json_to_header( json_header_path, temp_file_path )

		# compare written data to baseline
		baseline_file_path = self.baseline( 'test_writes_header_from_json', 'md' )
		self.assertTrue( cmp_lines( temp_file_path, baseline_file_path ) )

		# delete temp file
		os.remove( temp_file_path )

	def test_parses_readme_main_hash_title( self ):
		main_hash_title = parse_main_hash_title( self.test_readme_path )
		self.assertEqual( main_hash_title, 'Title Header' )

	def test_writes_hash_title_to_header( self ):
		#copy test readme to avoid overwriting the baseline
		test_copy_path = path.join( self.test_dir, 'test_readme.md' )
		copy2( self.test_readme_path, test_copy_path )

		init_header_info = parse_header( test_copy_path )
		main_hash_title = parse_main_hash_title( test_copy_path )
		self.assertNotEqual( init_header_info['title'], main_hash_title )

		write_hash_title_to_header( test_copy_path )
		final_header_info = parse_header( test_copy_path )
		self.assertEqual( final_header_info['title'], main_hash_title )

		# delete temp file
		os.remove( test_copy_path )

	def test_write_header_from_dict( self ):
		test_readme_path = self.baseline( 'test_write_header_from_dict_test', 'md' )
		copy2( self.baseline( 'test_write_header_from_dict_init', 'md' ), test_readme_path )

		test_header_content = {}
		test_header_content[ 'test' ] = 'overwriting content'
		test_header_content[ 'new' ] = 'are new values being added?'

		write_header_from_dict( test_header_content, test_readme_path )
		self.assertTrue( cmp_lines( test_readme_path, self.baseline( 'test_write_header_from_dict_final', 'md' ) ) )

		# delete temp file
		os.remove( test_readme_path )

	def test_markdown_to_dict_depth( self ):
		test_readme_path = self.baseline( 'test_markdown_to_dict_depth', 'md' )
		test_dict = markdown_to_dict( test_readme_path )
		baseline_dict = {
			'Heading 2': {
				'content': 'Content for heading 2\n',
				'children': {
					'Subheading 2.1': {
						'content': 'Content for subheading 2.1\n'
					}
				}
			},
			'Heading 1': {
				'content': 'Content for heading 1\n',
				'children': {
					'Subheading 1.1': {
						'content': 'Content for subheading 1.1\n\n'
					}
				}
			}
		}
		self.assertDictEqual( test_dict, baseline_dict )

	def test_markdown_to_dict_nohash( self ):
		test_readme_path = self.baseline( 'test_markdown_to_dict_nohash', 'md' )
		test_dict = markdown_to_dict( test_readme_path )
		baseline_dict = {}
		self.assertDictEqual( test_dict, baseline_dict )

	def test_markdown_to_dict_nokey( self ):
		test_readme_path = self.baseline( 'test_markdown_to_dict_nokey', 'md' )
		test_dict = markdown_to_dict( test_readme_path )
		baseline_dict = {}
		self.assertDictEqual( test_dict, baseline_dict )

	def test_markdown_to_dict_multiline( self ):
		test_readme_path = self.baseline( 'test_markdown_to_dict_multiline', 'md' )
		test_dict = markdown_to_dict( test_readme_path )
		baseline_dict = {
			'Heading 1': {
				'content': '\nContent for heading 1\n\n'
			},
			'Subheading 1.1': {
				'content': '\nContent for subheading 1.1\n\n'
			}
		}
		self.assertDictEqual( test_dict, baseline_dict )

	def test_markdown_to_dict_hashcontent( self ):
		test_readme_path = self.baseline( 'test_markdown_to_dict_hashcontent', 'md' )
		test_dict = markdown_to_dict( test_readme_path )
		baseline_dict = {
			'Heading 1': {
				'content': 'Content for #heading 1\n'
			},
			'Subheading 1.1': {
				'content': 'Content for subheading 1.1 with #\n'
			},
			'Heading 2': {
				'content': 'Content for heading 2\n\n'
			}
		}
		self.assertDictEqual( test_dict, baseline_dict )

class TestDictToMarkdown(unittest.TestCase):

	def test_empty_dict(self):
		nested_dict = {}
		expected_markdown = ""
		self.assertEqual(dict_to_markdown(nested_dict), expected_markdown)

	def test_single_section(self):
		nested_dict = {'Section 1': {'content': 'Content for section 1\n'}}
		expected_markdown = "# Section 1\nContent for section 1\n\n"
		self.assertEqual(dict_to_markdown(nested_dict), expected_markdown)

	def test_nested_sections(self):
		nested_dict = {
			'Section 1': {'content': 'Content for section 1\n'},
			'Section 2': {
				'content': 'Content for section 2\n',
				'children': {
					'Subsection 1': {'content': 'Content for subsection 1\n'},
					'Subsection 2': {'content': 'Content for subsection 2\n'}
				}
			}
		}
		expected_markdown = (
			"# Section 1\nContent for section 1\n\n"
			"# Section 2\nContent for section 2\n\n"
			"## Subsection 1\nContent for subsection 1\n\n"
			"## Subsection 2\nContent for subsection 2\n\n"
		)
		self.assertEqual(dict_to_markdown(nested_dict), expected_markdown)

	def test_consecutive_newlines(self):
		nested_dict = {'Section 1': {'content': 'Line 1\n\nLine 2\n'}}
		expected_markdown = "# Section 1\nLine 1\n\nLine 2\n\n"
		self.assertEqual(dict_to_markdown(nested_dict), expected_markdown)

	def test_deeply_nested_sections(self):
		nested_dict = {'Section 1': {
			'content': 'Content for section 1\n',
			'children': {'Subsection 1': {
				'content': 'Content for subsection 1\n',
				'children': {'Subsubsection 1': {'content': 'Content for subsubsection 1\n'}}
			}}
		}}
		expected_markdown = (
			"# Section 1\nContent for section 1\n\n"
			"## Subsection 1\nContent for subsection 1\n\n"
			"### Subsubsection 1\nContent for subsubsection 1\n\n"
		)
		self.assertEqual(dict_to_markdown(nested_dict), expected_markdown)


if __name__ == '__main__':
	unittest.main()