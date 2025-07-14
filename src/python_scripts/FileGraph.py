from python_scripts.GraphFiles import MarkdownFile, resourceFile
from pathlib import Path
import re
import os
import sys
import argparse
import networkx
import pyvis.network


class MarkdownTree:
    def __init__(self, root_file: MarkdownFile):
        self.file = root_file
        self.markdown_files = set()
        self.markdown_files.add(root_file)
        self.resource_files = set()
        self.graph = networkx.DiGraph()
        # Setting network settings for visualization
        self.network_output = pyvis.network.Network(width='100%', height='100%', directed=True, notebook=False)
        self.network_output.toggle_physics(True)

    def add_markdown_file(self, markdown_file: MarkdownFile, group_name=None):
        file_name = markdown_file.get_file_name()
        self.markdown_files.add(file_name)
        title_text = 'backlinks:<br>'
        backlink_list = markdown_file.get_backlink_list()
        title_text += f'<br>'.join(backlink_list)
        if group_name:
            self.graph.add_node(markdown_file, size = len(markdown_file.get_forward_links()), title=title_text, group=group_name)
        else:
            self.graph.add_node(markdown_file, size = len(markdown_file.get_forward_links()), title=title_text)

    def add_resource_file(self, resource_file: resourceFile, group_name=None):
        file_name = resource_file.get_file_name()
        self.resource_files.add(file_name)
        title_text = 'backlinks:<br>'
        backlink_list = resource_file.get_backlink_list()
        title_text += f'<br>'.join(backlink_list)
        if group_name:
            self.graph.add_node(resource_file, type='resource', title=title_text, group=group_name, size=1)
        else:
            self.graph.add_node(resource_file, type='resource', title=title_text, size=1)

    def create_html(self, output_name: str):
        self.network_output.from_nx(self.graph)
        self.network_output.show(output_name, notebook=False)
        print(f"HTML file created: {output_name}")
        return output_name
    






