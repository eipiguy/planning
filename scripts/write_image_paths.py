import os
from os import path

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico'}

this_dir = path.dirname(path.realpath(__file__))
output_file = path.join(this_dir, 'file_paths.txt')

def find_relative_paths(directory=this_dir, ):
	relative_paths = []
	for root, dirs, files in os.walk(directory):
		for name in files:
			if path.splitext(name)[1].lower() in IMAGE_EXTENSIONS:
				relative_paths.append(os.path.relpath(os.path.join(root, name), directory))
	return relative_paths

if __name__ == '__main__':
	relative_paths = find_relative_paths()
	with open(output_file, 'w') as f:
		for file_path in relative_paths:
			f.write(f"{file_path}\n")
