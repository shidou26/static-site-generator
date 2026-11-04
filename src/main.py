import os
import shutil
import re
from markdown import markdown_to_html_node

def copy_dir(curr: str, dest: str) -> None:
    os.makedirs(dest, exist_ok=True)
    for name in os.listdir(curr):
        source = os.path.join(curr, name)
        destination = os.path.join(dest, name)
        if os.path.isdir(source): copy_dir(source, destination)
        else: shutil.copy2(source, destination)

def extract_title(markdown: str) -> str:
    match = re.search(r"^# (.+)$", markdown, re.MULTILINE)
    if match is None: 
        raise Exception("no title")
    return match[0][2:]

def generate_path(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as stream: markdown = stream.read()
    with open(template_path, "r") as stream: template = stream.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown)
    content = html.to_html()
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as stream:
        stream.write(full_html)

def generate_path_recursive(dir_path_content, template_path, dest_dir_path) -> None:
    print(dir_path_content)
    print(dest_dir_path)
    for content in os.listdir(dir_path_content): 
        if os.path.isfile(os.path.join(dir_path_content, content)): 
            generate_path(os.path.join(dir_path_content, content), template_path, os.path.join(dest_dir_path, content).replace(".md", ".html"))
        else: 
            generate_path_recursive(os.path.join(dir_path_content, content), template_path, os.path.join(dest_dir_path, content))

def main():
    #Clear the public folder making way for static folder
    working_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_folder = os.path.join(working_folder, "public")
    static_folder = os.path.join(working_folder, "static")

    if os.path.isdir(public_folder): 
        shutil.rmtree(public_folder)
    os.makedirs(public_folder)

    copy_dir(static_folder, public_folder)

    #Generate contents
    generate_path_recursive(os.path.join(working_folder, "content"), os.path.join(working_folder, "template.html"), os.path.join(working_folder, "public"))

if __name__ == "__main__":
    main()