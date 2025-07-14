from pathlib import Path
import re
import os
import shutil
import sys
import argparse
import networkx


class MarkdownFile:
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.forward_links = {}   # {linked_file_name: linked_file_path}
        self.backlinks = {}       # {linked_file_name: linked_file_path}
        self.resources = {}       # {linked_file_name: linked_file_path}

    def add_forward_link(self, linked_file, location):
        if linked_file not in self.forward_links:
            self.forward_links[linked_file] = os.path.relpath(location, self.file_path.parent)

    def add_backlink(self, linking_file, location):
        if linking_file not in self.backlinks:
            self.backlinks[linking_file] = os.path.relpath(location, self.file_path.parent)

    def add_resource(self, resource_name, resource_path):
        if resource_name not in self.resources:
            self.resources[resource_name] = os.path.relpath(resource_path, self.file_path.parent)


    def get_forward_links(self):
        return self.forward_links

    def get_backlinks(self):
        return self.backlinks
    
    def get_backlink_list(self):
        return list(self.backlinks.keys())

    def get_resources(self):
        return self.resources
    
    def get_file_name(self):
        return self.file_name
    def get_file_path(self):
        return self.file_path


class resourceFile:
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = self.file_path.suffix.lower() 
        self.backlinks = {}  # {linked_file_name: linked_file_path}

    def get_file_name(self):
        return self.file_name

    def get_file_path(self):
        return self.file_path
    
    def get_file_type(self):
        return self.file_type
    
    def add_backlink(self, linking_file, location):
        if linking_file not in self.backlinks:
            self.backlinks[linking_file] = os.path.relpath(location, self.file_path.parent)
    
    def get_backlinks(self):
        return self.backlinks
    
    def get_backlink_list(self):
        return list(self.backlinks.keys())