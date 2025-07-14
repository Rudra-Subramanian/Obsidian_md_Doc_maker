from pathlib import Path
import re
import os
import shutil
import sys
import argparse
import networkx
from mkdocs.commands import serve


class HTMLMaker:
    def __init__(self, root_folder, output_folder):
        self.root_directory = Path(root_folder)
        self.output_directory = Path(output_folder)
        if self.output_directory.joinpath('mkdocs.yml').is_file():
            os.remove(self.output_directory.joinpath('mkdocs.yml'))
        self.all_files = {}
        self.written_files = set()
        self.found_files = set()
        #Fill self.all_files
        self.make_dir_and_set_output_directory()
        self.get_all_files_in_dir(self.root_directory)
        print(f"Found files: {self.all_files}")
        if 'index.md' not in self.all_files.values():
            raise FileNotFoundError(f"index file not found in {self.root_directory}. Please ensure an index.md file exists.")
        self.found_files.add('index')
        #Create output directory if it does not exist
        try:
            if not self.output_directory.is_dir():
                self.output_directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error creating output directory: {e}")
            raise e
        
        
    def make_dir_and_set_output_directory(self):
        if not self.output_directory.joinpath('docs/').is_dir():
            self.output_directory.joinpath('docs/').mkdir(parents=True, exist_ok=True)
        self.output_directory = self.output_directory.joinpath('docs/')


    def MakeHTML(self):
        absolute_index_file_path = self.root_directory.joinpath(Path(self.all_files['index']))
        output_index_file_path = self.output_directory.joinpath(Path(self.all_files['index']))
        file_text = open(absolute_index_file_path, 'r').read()
        new_file_text, unique_matches = self.replace_file_links(file_text, absolute_index_file_path)
        self.found_files.update(unique_matches)
        with open(output_index_file_path, 'w') as output_file:
            output_file.write(new_file_text)
        self.written_files.add('index')
        self.create_output_files()


    def create_output_files(self):
        file_difference = self.found_files.difference(self.written_files)
        while( len(file_difference) > 0):
            for file_name in file_difference:
                if file_name in self.all_files:
                    #is it and md file?
                    if self.all_files[file_name].endswith('.md'):
                        absolute_file_path = self.root_directory.joinpath(Path(self.all_files[file_name]))
                        output_file_path = self.output_directory.joinpath(Path(self.all_files[file_name]))
                        file_text = open(absolute_file_path, 'r').read()
                        new_file_text, unique_matches = self.annotate_images(file_text, absolute_file_path)
                        self.found_files.update(unique_matches)
                        final_file_text, unique_matches = self.replace_file_links(new_file_text, absolute_file_path)

                        #Create output directory if it does not exist
                        if not output_file_path.parent.is_dir():
                            output_file_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_file_path, 'w') as output_file:
                            output_file.write(final_file_text)
                        self.found_files.update(unique_matches)
                    else:
                        absolute_file_path = self.root_directory.joinpath(Path(self.all_files[file_name]))
                        output_file_path = self.output_directory.joinpath(Path(self.all_files[file_name]))
                        if not output_file_path.parent.is_dir():
                            output_file_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy(absolute_file_path, output_file_path)
                self.written_files.add(file_name)
            file_difference = self.found_files.difference(self.written_files)



    def replace_file_links(self, text, file_dir):
        pattern = re.compile(r"\[\[([^]]+)\]\]")
        matches = pattern.findall(text)
        for match in matches:
            if match in self.all_files:
                path_to_file = Path(self.all_files[match])
                path_to_file = self.root_directory.joinpath(path_to_file)
                relative_path = os.path.relpath(path_to_file, file_dir.parent)
                all_file_match = relative_path.replace(' ', '%20')
                text = text.replace(f'[[{match}]]', f'[{match}]({all_file_match})', 1)
        unique_matches = set(matches)
        return text, unique_matches   
    
    def annotate_images(self, text, file_path):
        pattern = re.compile(r'\(([^)]+\.(?:png|jpg|jpeg|gif|bmp|svg|mp4|mov|wav))\)', re.IGNORECASE)
        matches = pattern.findall(text)
        for match in matches:
            path_to_file = Path(self.all_files[match])
            path_to_file = self.root_directory.joinpath(path_to_file)
            # FINDING RELATIVE FILE PATH
            relative_path = os.path.relpath(path_to_file, file_path.parent)
            all_file_match = relative_path.replace(' ', '%20')
            annotation_text = f'\n1. ![{match}]({all_file_match}) \n\n'
            text = text.replace(f'({match})', f'(1) \n {{ .annotate }} \n {annotation_text}', 1)
        unique_matches = set(matches)
        return text, unique_matches 


    def get_all_files_in_dir(self, current_dir):
        for path in Path(current_dir).rglob('*'):
            if path.is_file():
                relative_path_string = str(path.relative_to(self.root_directory))
                #relative_path_string = relative_path_string.replace(' ', '\ ')
                if path.suffix == '.md':
                    self.all_files[path.stem] = relative_path_string
                else:
                    self.all_files[path.name] = relative_path_string
            if path.is_dir():
                self.get_all_files_in_dir(path)

    def get_folder_structure(self, current_dir):
        folder_structure = []
        for path in Path(current_dir).rglob('*'):
            if path.is_dir():
                relative_path_string = str(path.relative_to(self.root_directory))
                folder_structure.append(relative_path_string)
        return folder_structure


    def build_folder_dict(self, folder_structure):
        folder_dict = {}
        # First, build the folder tree
        for folder in folder_structure:
            parts = folder.split('/')
            current = folder_dict
            for i, part in enumerate(parts):
                if part not in current:
                    current[part] = {}
                current = current[part]
        # Now, place files into the correct folders
        for file_name, rel_path in self.all_files.items():
            file_parts = Path(rel_path).parts
            # Only consider files in the folder_structure
            if len(file_parts) > 1:
                current = folder_dict
                for part in file_parts[:-1]:
                    if part in current:
                        current = current[part]
                    else:
                        current[part] = {}
                        current = current[part]
                current[file_name] = rel_path
            else:
                # Top-level files
                folder_dict[file_name] = rel_path
        return folder_dict

    def make_nav_text(self, folder_dict, nav_string, indents):
        indent = '  ' * indents
        for folder in folder_dict:
            if isinstance(folder_dict[folder], dict) and folder_dict[folder] != {} and folder != 'index':  # Check if it's a non-empty dictionary
                nav_string =  f'{nav_string}\n{indent}- {folder}:'
                nav_string = self.make_nav_text(folder_dict[folder], nav_string, indents + 1)
            elif folder_dict[folder] != {}:
                nav_string = f'{nav_string}\n{indent}- {folder}: {folder_dict[folder]}'
        return nav_string


    def Makeymlfile(self, site_name, site_url, logo_path='None'):
        #Get folders properly
        folder_structure = self.get_folder_structure(self.root_directory)
        self.folder_dict = self.build_folder_dict(folder_structure)
        output_file_path = self.output_directory.joinpath(Path('images/logo.png'))
        if not output_file_path.parent.is_dir():
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
        if logo_path:
            shutil.copy(logo_path, output_file_path)
        yml_string = f'''site_name: {site_name} 
        \nsite_url:  {site_url}
        \ntheme:
        \n  logo: images/logo.png 
        \n  name: material
        \n  features: 
        \n    - navigation.instant
        \n    - navigation.instant.prefetch
        \n    - navigation.path
        \n    - navigation.indexes
        \n    - navigation.expand
        \n    - toc.follow
        \n    - navigation.top
        \n\nplugins:
        \n  - offline
        \nmarkdown_extensions:
        \n  - abbr
        \n  - md_in_html
        \n  - admonition
        \n  - attr_list
        \n  - pymdownx.details
        \n  - pymdownx.highlight
        \n  - pymdownx.superfences
        \n  - pymdownx.emoji:
        \n      emoji_index: !!python/name:material.extensions.emoji.twemoji
        \n      emoji_generator: !!python/name:material.extensions.emoji.to_svg
        \n  - pymdownx.inlinehilite
        \n\n'''
        output_file_path = self.output_directory.joinpath('../mkdocs.yml')

        nav_string = 'nav:\n'
        nav_string += '  - Home: index.md'
        nav_string = self.make_nav_text(self.folder_dict, nav_string, 1)
        yml_string += nav_string + '\n\n'
        with open(output_file_path, 'w') as output_file:
            output_file.write(yml_string)
        return yml_string


'''
Making the html website for a specific markdown file. 
It will make the specified file the new index file and create a directory structure based on the markdown files and their links.
'''
class FileHTMLMaker:
    def __init__(self, root_file, output_folder):
        self.root_file = Path(root_file)
        self.root_file_name = self.root_file.stem
        self.root_directory = self.root_file.parent
        self.output_directory = Path(output_folder)
        self.all_files = {}
        self.written_files = set()
        self.found_files = set()
        #Fill self.all_files
        self.create_new_file_structure()
        


    def create_new_file_structure(self):
        try:
            if not self.output_directory.is_dir():
                self.output_directory.mkdir(parents=True, exist_ok=True)
            if not self.output_directory.joinpath('temp_folder').is_dir():
                self.output_directory.joinpath('temp_folder').mkdir(parents=True, exist_ok=True)
            self.output_test = self.output_directory.joinpath('temp_folder')
            
            shutil.copytree(self.root_directory, self.output_test, dirs_exist_ok=True)
            os.rename(self.output_test.joinpath(self.root_file_name + '.md'), self.output_test.joinpath('index.md'))
            self.root_file = self.output_test.joinpath('index.md')
            self.root_file_name = self.root_file.stem
            self.root_directory = self.root_file.parent
            self.found_files.add(self.root_file)


        except Exception as e:
            print(f"Error creating output directory: {e}")
            raise e
        

    
    def MakeAll(self, site_name, site_url, logo_path='None'):
        self.MakeHTML()
        self.Makeymlfile(site_name, site_url, logo_path)
        shutil.rmtree(self.output_test)

    def MakeHTML(self):
        self.website_maker = HTMLMaker(self.root_directory, self.output_directory)
        self.website_maker.MakeHTML()

    
    def Makeymlfile(self, site_name, site_url, logo_path='None'):
        self.website_maker.Makeymlfile(site_name, site_url, logo_path)