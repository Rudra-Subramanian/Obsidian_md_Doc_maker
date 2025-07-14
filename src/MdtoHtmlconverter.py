from pathlib import Path
import re
import os
import shutil
import sys
import argparse
import networkx
from python_scripts.HtmlMaker import HTMLMaker, FileHTMLMaker
from python_scripts.GraphFiles import MarkdownFile, resourceFile
from python_scripts.FileGraph import MarkdownTree
from mkdocs.commands import serve

def startMkdocsServer(directory):
    directory = Path(directory)
    os.chdir(directory)
    print(f"Starting MkDocs server in {os.getcwd()}")
    serve.serve()
    return

def create_html_from_folder(root_folder, output_folder, site_name, site_url, logo_path=None):
    html_maker = HTMLMaker(root_folder, output_folder)
    html_maker.MakeHTML()
    html_maker.Makeymlfile(site_name, site_url, logo_path)

def create_html_from_mdfile(md_file, output_folder, site_name, site_url, logo_path=None):
    html_maker = FileHTMLMaker(md_file, output_folder)
    html_maker.MakeHTML()
    html_maker.Makeymlfile(site_name, site_url, logo_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 MdtoHtmlconverter.py --root_folder <root_folder> --output_folder <output_folder> --site_name <site_name> --site_url <url of site> --logo <logo_path is optional>")
        sys.exit(1)


    parser = argparse.ArgumentParser(description="Convert Markdown files to HTML with additional site options.")
    parser.add_argument('--root_folder', required=False, help='Root folder containing markdown files with index.md')
    parser.add_argument('--root_md', required=False, help='Root markdown file to convert into index.md')
    parser.add_argument('--output_folder', required=True, help='Output folder for generated HTML files')
    parser.add_argument('--logo', required=False, help='Path to the site logo')
    parser.add_argument('--site_name', required=True, help='Name of the site')
    parser.add_argument('--site_url', required=True, help='URL of the site')
    '''
    ADD build argument and make everything else not necessary to be true then add if statements to check and give statements on what is wrong
    '''

    args = parser.parse_args()

    root_folder = args.root_folder
    root_file = args.root_md
    if root_file and root_folder:
        print("Error: Please provide either --root_folder or --root_md, not both.")
        raise ValueError("Please provide either --root_folder or --root_md, not both.")
    output_folder = args.output_folder
    logo_path = args.logo
    site_name = args.site_name
    site_url = args.site_url
    if logo_path:
        logo_path = Path(logo_path)
    print(f"Root folder: {root_folder}"
          f"\nOutput folder: {output_folder}"
          f"\nLogo: {logo_path}"
          f"\nSite name: {site_name}"
          f"\nSite URL: {site_url}")
    if root_folder:
        create_html_from_folder(root_folder, output_folder, site_name, site_url, logo_path)
    if root_file:
        create_html_from_mdfile(root_file, output_folder, site_name, site_url, logo_path)
    startMkdocsServer(output_folder)

    '''
    ADD A Graph builder as well and see how that works.
    '''



